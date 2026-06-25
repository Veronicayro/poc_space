#!/usr/bin/env python
"""
Extract a structured operation/schema index from a cached BIAN OAS3 Service Domain YAML.

Why this exists
---------------
Downstream phases (notably Phase 7 backend-contract-design) previously re-parsed large
BIAN OAS3 YAMLs using ad-hoc shell/python one-liners, creating token-heavy dumps and
fragile $ref escaping issues.

This script provides a permanent, reusable extractor that:
- Reads a cached Service Domain OAS3 YAML from architecture/cache/bian/release{release}/oas3/yamls/
- Resolves internal $ref safely (no shell escaping concerns)
- Produces a compact JSON index per operation including:
  - operationId, HTTP method, path
  - inferred BIAN operation type (Initiate/Retrieve/Control/Execute/Update/Exchange/Query/Register/Request/Notify)
  - request/response schema names and flattened properties (one-level, plus required list)
  - associated Control Record (best-effort inference)

The output is cached at:
  architecture/cache/bian/release{release}/index/<ServiceDomain>.json

Idempotency:
- If the cache exists, the script exits successfully without regenerating unless --force is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml


BIAN_OPERATION_ORDER = [
    ("Initiate", re.compile(r"^initiate", re.IGNORECASE)),
    ("Retrieve", re.compile(r"^retrieve", re.IGNORECASE)),
    ("Control", re.compile(r"^control", re.IGNORECASE)),
    ("Execute", re.compile(r"^execute", re.IGNORECASE)),
    ("Update", re.compile(r"^update", re.IGNORECASE)),
    ("Exchange", re.compile(r"^exchange", re.IGNORECASE)),
    ("Query", re.compile(r"^(query|list|search|evaluate)", re.IGNORECASE)),
    ("Register", re.compile(r"^register", re.IGNORECASE)),
    ("Request", re.compile(r"^request", re.IGNORECASE)),
    ("Notify", re.compile(r"^notify", re.IGNORECASE)),
]


HTTP_METHODS = {"get", "put", "post", "delete", "patch", "options", "head"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"OAS3 root is not a mapping: {path}")
    return data


def _json_dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=False, ensure_ascii=False)
        f.write("\n")


def _infer_bian_operation(operation_id: str | None, summary: str | None, method: str) -> str | None:
    candidates: List[str] = []
    for source in (operation_id or "", summary or ""):
        for name, rx in BIAN_OPERATION_ORDER:
            if rx.search(source.strip()):
                candidates.append(name)
    if candidates:
        return candidates[0]

    # Fallback heuristics if operationId/summary absent
    if method.lower() == "get":
        return "Retrieve"
    if method.lower() in {"post", "put", "patch"}:
        return "Update"
    return None


def _pointer_unescape(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def _resolve_json_pointer(doc: Dict[str, Any], pointer: str) -> Any:
    if not pointer.startswith("#/"):
        raise ValueError(f"Only internal $ref pointers supported, got: {pointer}")
    cur: Any = doc
    for raw in pointer[2:].split("/"):
        key = _pointer_unescape(raw)
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            raise KeyError(f"Pointer segment not found: {key} in {pointer}")
    return cur


def _resolve_ref(doc: Dict[str, Any], node: Any, seen: Optional[Set[str]] = None) -> Any:
    """
    Resolve internal $ref recursively. Only supports local refs (#/...) which is what the
    cached BIAN OAS3 YAMLs use in this repo.
    """
    if seen is None:
        seen = set()

    if isinstance(node, dict) and "$ref" in node and isinstance(node["$ref"], str):
        ref = node["$ref"]
        if ref in seen:
            # circular; stop
            return {"$ref": ref}
        seen.add(ref)
        resolved = _resolve_json_pointer(doc, ref)
        return _resolve_ref(doc, resolved, seen)

    if isinstance(node, dict):
        return {k: _resolve_ref(doc, v, seen.copy()) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve_ref(doc, v, seen.copy()) for v in node]
    return node


def _schema_name_from_ref(ref: str | None) -> str | None:
    if not ref:
        return None
    if not ref.startswith("#/components/schemas/"):
        return None
    return ref.split("/")[-1]


def _extract_properties(doc: Dict[str, Any], schema_node: Any) -> Dict[str, Any]:
    """
    Extract a one-level property map from a schema, resolving $ref on the schema itself.
    For properties that are $ref, we keep their ref name (do not inline whole deep trees
    to keep the index compact).
    """
    schema = _resolve_ref(doc, schema_node)
    if not isinstance(schema, dict):
        return {}

    # Handle allOf/oneOf by shallow merge where possible
    if "allOf" in schema and isinstance(schema["allOf"], list):
        merged: Dict[str, Any] = {"type": schema.get("type", "object"), "properties": {}, "required": []}
        required: List[str] = []
        props: Dict[str, Any] = {}
        for part in schema["allOf"]:
            part_res = _resolve_ref(doc, part)
            if isinstance(part_res, dict):
                part_props = part_res.get("properties")
                if isinstance(part_props, dict):
                    props.update(part_props)
                part_req = part_res.get("required")
                if isinstance(part_req, list):
                    required.extend([r for r in part_req if isinstance(r, str)])
        merged["properties"] = props
        merged["required"] = sorted(set(required))
        schema = merged

    props_node = schema.get("properties")
    if not isinstance(props_node, dict):
        return {}

    out: Dict[str, Any] = {}
    for prop_name, prop_schema in props_node.items():
        if not isinstance(prop_name, str):
            continue
        if isinstance(prop_schema, dict) and "$ref" in prop_schema:
            out[prop_name] = {"$ref_schema": _schema_name_from_ref(prop_schema.get("$ref")) or prop_schema.get("$ref")}
            continue

        resolved = _resolve_ref(doc, prop_schema)
        if isinstance(resolved, dict):
            entry: Dict[str, Any] = {}
            for k in ("type", "format", "description", "enum", "items", "nullable", "example"):
                if k in resolved:
                    entry[k] = resolved[k]
            if "$ref" in resolved:
                entry["$ref_schema"] = _schema_name_from_ref(resolved.get("$ref")) or resolved.get("$ref")
            out[prop_name] = entry if entry else {"type": resolved.get("type")}
        else:
            out[prop_name] = {"type": None}
    return out


def _pick_request_schema(doc: Dict[str, Any], op: Dict[str, Any]) -> Tuple[str | None, Dict[str, Any]]:
    rb = op.get("requestBody")
    if not isinstance(rb, dict):
        return None, {}
    rb = _resolve_ref(doc, rb)
    content = rb.get("content")
    if not isinstance(content, dict):
        return None, {}
    app_json = content.get("application/json") or next(iter(content.values()), None)
    if not isinstance(app_json, dict):
        return None, {}
    schema = app_json.get("schema")
    if schema is None:
        return None, {}
    if isinstance(schema, dict) and "$ref" in schema:
        name = _schema_name_from_ref(schema.get("$ref"))
        resolved_schema = _resolve_ref(doc, schema)
        props = _extract_properties(doc, resolved_schema)
        required = []
        if isinstance(resolved_schema, dict) and isinstance(resolved_schema.get("required"), list):
            required = [r for r in resolved_schema["required"] if isinstance(r, str)]
        return name, {"properties": props, "required": required}
    # inline schema
    props = _extract_properties(doc, schema)
    required = []
    resolved_schema = _resolve_ref(doc, schema)
    if isinstance(resolved_schema, dict) and isinstance(resolved_schema.get("required"), list):
        required = [r for r in resolved_schema["required"] if isinstance(r, str)]
    return None, {"properties": props, "required": required}


def _pick_response_schema(doc: Dict[str, Any], op: Dict[str, Any]) -> Tuple[str | None, Dict[str, Any]]:
    responses = op.get("responses")
    if not isinstance(responses, dict):
        return None, {}
    responses = _resolve_ref(doc, responses)

    # Prefer 200, then 201, then first 2xx, then default
    candidates = []
    for k, v in responses.items():
        if isinstance(k, str):
            candidates.append((k, v))
    preferred_keys = ["200", "201"]
    for key in preferred_keys:
        if key in responses:
            candidates = [(key, responses[key])]
            break
    else:
        two_xx = [kv for kv in candidates if kv[0].startswith("2")]
        if two_xx:
            candidates = [two_xx[0]]
        elif "default" in responses:
            candidates = [("default", responses["default"])]

    if not candidates:
        return None, {}

    _, resp = candidates[0]
    if not isinstance(resp, dict):
        return None, {}
    resp = _resolve_ref(doc, resp)
    content = resp.get("content")
    if not isinstance(content, dict):
        return None, {}
    app_json = content.get("application/json") or next(iter(content.values()), None)
    if not isinstance(app_json, dict):
        return None, {}
    schema = app_json.get("schema")
    if schema is None:
        return None, {}
    if isinstance(schema, dict) and "$ref" in schema:
        name = _schema_name_from_ref(schema.get("$ref"))
        resolved_schema = _resolve_ref(doc, schema)
        props = _extract_properties(doc, resolved_schema)
        required = []
        if isinstance(resolved_schema, dict) and isinstance(resolved_schema.get("required"), list):
            required = [r for r in resolved_schema["required"] if isinstance(r, str)]
        return name, {"properties": props, "required": required}
    props = _extract_properties(doc, schema)
    required = []
    resolved_schema = _resolve_ref(doc, schema)
    if isinstance(resolved_schema, dict) and isinstance(resolved_schema.get("required"), list):
        required = [r for r in resolved_schema["required"] if isinstance(r, str)]
    return None, {"properties": props, "required": required}


def _infer_control_record(doc: Dict[str, Any], service_domain: str) -> str | None:
    """
    Best-effort CR inference:
    - If x-bian-controlrecord exists in info, use it.
    - Else: use first tag name in paths operations.
    - Else: try to infer from schema names containing 'ControlRecord' patterns.
    """
    info = doc.get("info")
    if isinstance(info, dict):
        for key in ("x-bian-controlrecord", "x-bian-control-record", "x_bian_control_record"):
            val = info.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()

    paths = doc.get("paths")
    if isinstance(paths, dict):
        for _, item in paths.items():
            if isinstance(item, dict):
                for m, op in item.items():
                    if m.lower() not in HTTP_METHODS or not isinstance(op, dict):
                        continue
                    tags = op.get("tags")
                    if isinstance(tags, list) and tags and isinstance(tags[0], str) and tags[0].strip():
                        return tags[0].strip()

    schemas = (((doc.get("components") or {}).get("schemas")) if isinstance(doc.get("components"), dict) else None)
    if isinstance(schemas, dict):
        # Heuristic: pick the most frequent prefix before "Request"/"Response"
        prefixes: Dict[str, int] = {}
        for name in schemas.keys():
            if not isinstance(name, str):
                continue
            m = re.match(r"^(.*?)(Request|Response|Retrieve|Initiate|Update|Execute|Exchange)", name)
            if m:
                prefixes[m.group(1)] = prefixes.get(m.group(1), 0) + 1
        if prefixes:
            return max(prefixes.items(), key=lambda kv: kv[1])[0] or service_domain

    return service_domain


def extract_service_domain(service_domain: str, release: str, cache_root: Path) -> Dict[str, Any]:
    oas_path = cache_root / f"release{release}" / "oas3" / "yamls" / f"{service_domain}.yaml"
    if not oas_path.exists():
        raise FileNotFoundError(f"Cached OAS3 YAML not found: {oas_path}")

    doc = _read_yaml(oas_path)

    control_record = _infer_control_record(doc, service_domain)

    operations: List[Dict[str, Any]] = []
    paths = doc.get("paths")
    if not isinstance(paths, dict):
        paths = {}

    for path, item in paths.items():
        if not isinstance(path, str) or not isinstance(item, dict):
            continue
        for method, op in item.items():
            if not isinstance(method, str) or method.lower() not in HTTP_METHODS:
                continue
            if not isinstance(op, dict):
                continue

            op_resolved = _resolve_ref(doc, op)
            operation_id = op_resolved.get("operationId") if isinstance(op_resolved.get("operationId"), str) else None
            summary = op_resolved.get("summary") if isinstance(op_resolved.get("summary"), str) else None
            bian_type = _infer_bian_operation(operation_id, summary, method)

            req_schema_name, req_schema = _pick_request_schema(doc, op_resolved)
            resp_schema_name, resp_schema = _pick_response_schema(doc, op_resolved)

            operations.append(
                {
                    "path": path,
                    "method": method.lower(),
                    "operationId": operation_id,
                    "summary": summary,
                    "bian_operation": bian_type,
                    "control_record": control_record,
                    "request": {
                        "schema_name": req_schema_name,
                        **req_schema,
                    },
                    "response": {
                        "schema_name": resp_schema_name,
                        **resp_schema,
                    },
                }
            )

    payload = {
        "service_domain": service_domain,
        "bian_release": release,
        "source_oas3_path": str(oas_path).replace("\\", "/"),
        "generated_at": _now_iso(),
        "control_record": control_record,
        "operations": operations,
    }
    return payload


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bian_extract_service_domain",
        description="Extract an operation/schema index from a cached BIAN OAS3 Service Domain YAML and cache it as JSON.",
    )
    parser.add_argument("--service-domain", required=True, help="BIAN Service Domain name, e.g. PartyLifecycleManagement")
    parser.add_argument("--release", required=True, help="BIAN release, e.g. 14.0.0")
    parser.add_argument(
        "--cache-root",
        default="architecture/cache/bian",
        help="Root cache folder that contains release{release}/...",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate JSON cache even if it already exists.",
    )
    args = parser.parse_args(argv)

    service_domain = args.service_domain.strip()
    release = args.release.strip()
    cache_root = Path(args.cache_root)

    out_path = cache_root / f"release{release}" / "index" / f"{service_domain}.json"

    if out_path.exists() and not args.force:
        # Idempotent no-op
        return 0

    payload = extract_service_domain(service_domain, release, cache_root)
    _json_dump(out_path, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
