#!/usr/bin/env python3
"""Regenerates the package from the OpenAPI spec.

The low-level client (src/socialapihq: api/, models/, api_client.py…) comes from
OpenAPI Generator; then `SocialAPI` on top of it (src/socialapihq/client.py), the
README's method tables and the endpoint tests.

    python scripts/generate.py                 # the live spec
    SPEC=../socialapi/api/openapi/public.json python scripts/generate.py
    python scripts/generate.py --version 0.1.3 # the version baked into the package
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "socialapihq"


def current_version() -> str:
    match = re.search(r'^version = "([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M)
    if not match:
        sys.exit("pyproject.toml has no version.")
    return match.group(1)


def generator() -> list[str]:
    # The generator's version is pinned in openapitools.json, read by the npm wrapper.
    executable = shutil.which("npx")
    if not executable:
        sys.exit("npx is needed to run OpenAPI Generator (it pins the version in openapitools.json).")
    return [executable, "--yes", "@openapitools/openapi-generator-cli"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=None)
    args = parser.parse_args()
    spec = os.environ.get("SPEC", "https://api.socialapi.sh/openapi.json")
    version = args.version or current_version()

    with tempfile.TemporaryDirectory() as scratch:
        subprocess.run(
            [
                *generator(),
                "generate",
                "-i",
                spec,
                "-g",
                "python",
                "-o",
                scratch,
                "-p",
                f"packageName={PACKAGE},projectName={PACKAGE},packageVersion={version}",
            ],
            check=True,
            cwd=ROOT,
        )
        target = ROOT / "src" / PACKAGE
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(Path(scratch) / PACKAGE, target)

    for script in ("generate_client.py", "generate_api_reference.py", "generate_endpoint_tests.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), "--spec", spec], check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
