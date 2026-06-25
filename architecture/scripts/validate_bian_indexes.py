from __future__ import annotations

from pathlib import Path

import yaml


def check(path: str, expected_substr: str, expected_type: str) -> int:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))

    spec = data.get("spec_type")
    count = data.get("count")
    items = data.get("items") or []

    bad = []
    for i, it in enumerate(items):
        link = (it.get("link") or "")
        t = (it.get("type") or "")
        if expected_substr not in link or t != expected_type:
            bad.append((i, it.get("name"), t, link))

    print(
        path,
        "spec_type=",
        spec,
        "count=",
        count,
        "items=",
        len(items),
        "bad=",
        len(bad),
    )

    if bad[:10]:
        print("first_bad:")
        for row in bad[:10]:
            print(" ", row)

    return len(bad)


def main() -> None:
    bad1 = check(
        "architecture/context/bian-spec-index-oas3.yaml",
        "/oas3/yamls/",
        "oas3",
    )
    bad2 = check(
        "architecture/context/bian-spec-index-asyncapi.yaml",
        "/asyncapi-3.x/yamls/",
        "asyncapi-3.x",
    )

    if bad1 or bad2:
        raise SystemExit(1)

    print("OK")


if __name__ == "__main__":
    main()

