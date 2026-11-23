import argparse,gzip
from pathlib import Path


def normalized(path):
    data=path.read_bytes()
    if path.suffix==".gz":
        data=gzip.decompress(data)
    return data.replace(b"\r\n",b"\n")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("reference",type=Path)
    p.add_argument("replay",type=Path)
    a=p.parse_args()
    files="cases.jsonl scores.csv traces.jsonl.gz language.csv language_corpus.jsonl summary.csv strata.csv effects.csv semantics_summary.csv ceiling.csv".split()
    for name in files:
        if normalized(a.reference/name)!=normalized(a.replay/name):
            raise SystemExit(f"Mismatch: {name}")
    print(f"Matched {len(files)} scientific artifacts")
