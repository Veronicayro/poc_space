from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def load_index(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Lookup BIAN Service Domains in local cached indexes without loading full YAML bodies. "
            "Designed to support token-efficient phase execution (read only needed items)."
        )
    )
    ap.add_argument(
        "--spec",
        choices=["oas3", "asyncapi-3.x"],
        default="oas3",
        help="Which index to query.",
    )
    ap.add_argument(
        "--name",
        action="append",
        default=[],
        help="Exact Service Domain name to return. Can be provided multiple times.",
    )
    ap.add_argument(
        "--contains",
        action="append",
        default=[],
        help="Case-insensitive substring filter on Service Domain name. Can be provided multiple times.",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Limit number of returned items (after filtering).",
    )

    args = ap.parse_args()

    index_path = (
        Path("architecture/context/bian-spec-index-oas3.yaml")
        if args.spec == "oas3"
        else Path("architecture/context/bian-spec-index-asyncapi.yaml")
    )

    idx = load_index(index_path)
    items = idx.get("items") or []

    names = set(args.name)
    contains = [c.lower() for c in args.contains]

    def match(it: dict) -> bool:
        n = (it.get("name") or "")
        if names and n not in names:
            return False
        if contains:
            nl = n.lower()
            if not any(c in nl for c in contains):
                return False
        return True

    out_items = [it for it in items if match(it)][: args.limit]

    # Return small YAML payload (easy to paste into prompts / phase context)
    payload = {
        "domain_standard": idx.get("domain_standard"),
        "release": idx.get("release"),
        "spec_type": idx.get("spec_type"),
        "query": {
            "name": args.name,
            "contains": args.contains,
            "limit": args.limit,
        },
        "count": len(out_items),
        "items": out_items,
    }

    print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=140))


if __name__ == "__main__":
    main()

