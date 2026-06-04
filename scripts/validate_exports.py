#!/usr/bin/env python3
# Validates every directory under exports/<YYYY-MM-DD>/ contains the
# three required JSON artifacts (manifest, dashboard, runs), parses
# cleanly, and that runs length matches manifest.attemptsTotal.
#
# Exit codes:
#   0  every export is well-formed
#   1  one or more exports failed validation
#
# Usage: python3 scripts/validate_exports.py [<root>]
# Default root is ./exports relative to the current working directory.

import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED_MANIFEST_KEYS = {
    "datasetVersion",
    "runDate",
    "harnessRepo",
    "harnessSha",
    "zeroVersion",
    "models",
    "tasks",
    "languages",
    "mode",
    "attemptsTotal",
    "passedTotal",
    "passRate",
}

REQUIRED_RUN_KEYS = {
    "model",
    "task",
    "lang",
    "passed",
    "numCases",
    "numPassed",
    "passRate",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_export(export_dir: Path) -> list[str]:
    errors: list[str] = []
    name = export_dir.name

    manifest_path = export_dir / "manifest.json"
    dashboard_path = export_dir / "dashboard.json"
    runs_path = export_dir / "runs.json"

    for required in (manifest_path, dashboard_path, runs_path):
        if not required.is_file():
            errors.append(f"{name}: missing {required.name}")

    if errors:
        return errors

    try:
        manifest = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        errors.append(f"{name}/manifest.json: invalid JSON ({exc})")
        manifest = None

    try:
        load_json(dashboard_path)
    except json.JSONDecodeError as exc:
        errors.append(f"{name}/dashboard.json: invalid JSON ({exc})")

    try:
        runs = load_json(runs_path)
    except json.JSONDecodeError as exc:
        errors.append(f"{name}/runs.json: invalid JSON ({exc})")
        runs = None

    if isinstance(manifest, dict):
        missing = REQUIRED_MANIFEST_KEYS - set(manifest.keys())
        if missing:
            errors.append(
                f"{name}/manifest.json: missing keys {sorted(missing)}"
            )
        if manifest.get("runDate") != name:
            errors.append(
                f"{name}/manifest.json: runDate {manifest.get('runDate')!r} "
                f"does not match directory name"
            )

    if isinstance(runs, list) and isinstance(manifest, dict):
        expected = manifest.get("attemptsTotal")
        if isinstance(expected, int) and len(runs) != expected:
            errors.append(
                f"{name}/runs.json: length {len(runs)} != "
                f"manifest.attemptsTotal {expected}"
            )
        for idx, run in enumerate(runs):
            if not isinstance(run, dict):
                errors.append(f"{name}/runs.json[{idx}]: not an object")
                continue
            missing = REQUIRED_RUN_KEYS - set(run.keys())
            if missing:
                errors.append(
                    f"{name}/runs.json[{idx}]: missing keys {sorted(missing)}"
                )
                break

    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("exports")
    if not root.is_dir():
        print(f"validate_exports: {root} is not a directory", file=sys.stderr)
        return 1

    export_dirs = sorted(
        p for p in root.iterdir() if p.is_dir() and DATE_RE.match(p.name)
    )

    if not export_dirs:
        print(f"validate_exports: no dated export dirs under {root}")
        return 0

    all_errors: list[str] = []
    for export_dir in export_dirs:
        errors = validate_export(export_dir)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"ok  {export_dir.name}")

    if all_errors:
        print("", file=sys.stderr)
        for err in all_errors:
            print(f"FAIL {err}", file=sys.stderr)
        print(
            f"\nvalidate_exports: {len(all_errors)} error(s) across "
            f"{len(export_dirs)} export(s)",
            file=sys.stderr,
        )
        return 1

    print(f"\nvalidate_exports: {len(export_dirs)} export(s) clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
