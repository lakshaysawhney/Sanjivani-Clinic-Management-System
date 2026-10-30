"""Run commands with private local development configuration, never pilot credentials."""

import json
import os
from pathlib import Path
import secrets
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
private = root / ".private"
private.mkdir(exist_ok=True)
config_file = private / "dev.json"
if not config_file.exists():
    config_file.write_text(
        json.dumps(
            {
                "DJANGO_SECRET_KEY": secrets.token_urlsafe(60),
                "DEBUG": "1",
                "DATABASE_URL": (private / "dev-db-url").read_text().strip(),
                "ACCOUNTING_START_DATE": "2026-10-01",
            }
        )
    )
config = json.loads(config_file.read_text())
os.environ.update(config)
os.environ.setdefault("APP_ORIGIN", "http://localhost:5173")
os.environ.setdefault("TOKEN_ENCRYPTION_KEY", "")
command = [sys.executable, *sys.argv[1:]]
sys.exit(subprocess.call(command, cwd=root / "backend", env=os.environ))
