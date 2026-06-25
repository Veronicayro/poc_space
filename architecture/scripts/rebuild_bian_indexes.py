from __future__ import annotations

from pathlib import Path

import yaml


def _safe_str(v) -> str:
    return (v or "").strip() if isinstance(v, str) else ""


def load_description(yaml_path: Path) -> str:
    """Extracts info.description from an OpenAPI/AsyncAPI YAML file.

    If parsing fails or the field is absent, returns empty string.
    """

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        info = data.get("info") or {}
        return _safe_str(info.get("description"))
    except Exception:
        return ""


def build_index(cache_dir: Path, out_path: Path, spec_type: str) -> dict:
    items = []

    for p in sorted(cache_dir.glob("*.y*ml")):
        items.append(
            {
                "name": p.stem,
                "description": load_description(p),
                "link": str(p).replace("\\", "/"),
                "type": spec_type,
            }
        )

    payload = {
        "domain_standard": "BIAN",
        "release": "14.0.0",
        "spec_type": spec_type,
        "count": len(items),
        "items": items,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=140),
        encoding="utf-8",
        newline="\n",
    )

    return payload


def main() -> None:
    base = Path("architecture/cache/bian/release14.0.0")

    oas3_cache = base / "oas3" / "yamls"
    async_cache = base / "asyncapi-3.x" / "yamls"

    if not oas3_cache.exists():
        raise SystemExit(f"Missing cache directory: {oas3_cache}")
    if not async_cache.exists():
        raise SystemExit(f"Missing cache directory: {async_cache}")

    oas3_out = Path("architecture/context/bian-spec-index-oas3.yaml")
    async_out = Path("architecture/context/bian-spec-index-asyncapi.yaml")

    oas3_payload = build_index(oas3_cache, oas3_out, "oas3")
    async_payload = build_index(async_cache, async_out, "asyncapi-3.x")

    print(f"Wrote {oas3_out} items={oas3_payload['count']}")
    print(f"Wrote {async_out} items={async_payload['count']}")


if __name__ == "__main__":
    main()

