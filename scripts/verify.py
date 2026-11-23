from pathlib import Path
import hashlib

root=Path(__file__).resolve().parents[1]
entries=(root/"SHA256SUMS").read_text().splitlines()
for entry in entries:
    expected,path=entry.split("  ",1)
    with (root/path).open("rb") as f:
        actual=hashlib.file_digest(f,"sha256").hexdigest()
    if expected!=actual:
        raise SystemExit(f"checksum mismatch: {path}")
print(f"Verified {len(entries)} release artifacts.")
