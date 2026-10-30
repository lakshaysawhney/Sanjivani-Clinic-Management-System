"""Run local Playwright using ignored development credentials, without printing them."""

import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
config = json.loads((root / ".private" / "dev.json").read_text())
os.environ.update(config)
sys.exit(
    subprocess.call(
        ["npm.cmd" if os.name == "nt" else "npm", "run", "test:e2e", "--", *sys.argv[1:]],
        cwd=root / "frontend",
        env=os.environ,
    )
)
