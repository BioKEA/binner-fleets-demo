#!/usr/bin/env python3
"""Validate every tools/<tool>/spec.yaml against tools/_schema.json."""
import json
import sys
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "tools" / "_schema.json").read_text())


def main() -> int:
    errors = 0
    for spec_path in sorted((ROOT / "tools").glob("*/spec.yaml")):
        try:
            data = yaml.safe_load(spec_path.read_text())
            validate(data, SCHEMA)
            print(f"OK   {spec_path.relative_to(ROOT)}")
        except (ValidationError, yaml.YAMLError) as e:
            print(f"FAIL {spec_path.relative_to(ROOT)}: {e}")
            errors += 1
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
