"""Check tracked source for secrets and private attachment leakage without printing matches."""

import re
import subprocess
from pathlib import Path

files = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
patterns = [
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY",
    r"gh[pousr]_[A-Za-z0-9]{30,}",
    r"postgres(?:ql)?://[^\s:]+:(?!local-development-only|synthetic-ci-only)[^\s@]+@",
    r"[\w.+-]+@gmail\.com",
]
failures = []
for name in filter(None, files):
    path = Path(name)
    if not path.is_file() or path.suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        if path.suffix in {".png", ".jpg", ".jpeg"}:
            failures.append(name)
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    if any(re.search(pattern, text) for pattern in patterns):
        failures.append(name)
if failures:
    raise SystemExit("Potential private material in: " + ", ".join(failures))
print("Public source scan passed.")
