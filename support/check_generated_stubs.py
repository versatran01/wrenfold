"""Check that generated Python stubs match the committed files."""

import subprocess
import sys
from pathlib import Path

STUBS_DIR = Path("components/wrapper/stubs")


def main() -> int:
    result = subprocess.run(
        [
            "git",
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--",
            str(STUBS_DIR),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print("Generated Python stubs differ from the committed files:", file=sys.stderr)
        print(result.stdout, end="", file=sys.stderr)
        print("Regenerate the stubs and commit the results.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
