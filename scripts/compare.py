from pathlib import Path
import argparse
import gzip
import hashlib


def digest(path):
    op=gzip.open if path.suffix==".gz" else open
    with op(path,"rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("reference",type=Path)
    p.add_argument("replay",type=Path)
    args=p.parse_args()
    for filename in ("scores.csv","traces.jsonl.gz"):
        a,b=[digest(root/filename) for root in (args.reference,args.replay)]
        if a!=b:
            raise SystemExit(f"{filename} mismatch")
        print(filename,a)
