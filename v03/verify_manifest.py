import hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
entries=(root/"SHA256SUMS").read_text().splitlines()
for line in entries:
    h,name=line.split("  ",1)
    with (root/name).open("rb") as f:
        if hashlib.file_digest(f,"sha256").hexdigest()!=h:
            raise SystemExit(f"Mismatch: {name}")
print(f"Verified {len(entries)} artifacts")
