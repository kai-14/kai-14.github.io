#!/usr/bin/env python3
"""Validates res/raw/watchface.xml against Google's Watch Face Format XSD (needs `pip install xmlschema`).

Usage: python3 tools/validate.py <path to watchface/third_party/wff/specification/documents/2/watchface.xsd>
"""
import pathlib
import sys

import xmlschema

face = pathlib.Path(__file__).resolve().parent.parent / "app/src/main/res/raw/watchface.xml"
errors = list(xmlschema.XMLSchema11(sys.argv[1]).iter_errors(str(face)))
for e in errors:
    print(f"{e.path}: {e.reason}")
print("VALID" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
