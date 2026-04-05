from __future__ import annotations

import argparse
from pathlib import Path

from autopaper.spec import parse_spec, write_spec_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse PROJECT_SPEC.md into structured JSON.")
    parser.add_argument("--spec", default="PROJECT_SPEC.md", help="Path to the controlling spec file.")
    parser.add_argument("--output", default="build/spec.json", help="Where to write the parsed spec JSON.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    spec_path = (repo_root / args.spec).resolve()
    output_path = (repo_root / args.output).resolve()

    spec = parse_spec(spec_path, repo_root)
    write_spec_json(spec, output_path)
    print(f"Wrote parsed spec to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
