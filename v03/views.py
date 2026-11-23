"""Forward only observation fields to an isolated replay interpreter."""
import gzip,json,shutil,subprocess,sys,tempfile
from pathlib import Path

def replay(root):
    observations=[]
    expected=[]
    with gzip.open(root/"traces.jsonl.gz","rt") as f:
        for line in f:
            x=json.loads(line)
            observations.append(json.dumps([x["method"],x["opening"],[e["view"] for e in x["events"]]]))
            expected.append([x["order"],[[e["sent"],e["reason"]] for e in x["events"]]])
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp)
        for package,files in {"privtrace02":["__init__.py","legacy/__init__.py","legacy/rules.py","planning.py"],
                              "privtrace03":["__init__.py","language.py","controls.py"]}.items():
            for file in files:
                dest=d/package/file
                dest.parent.mkdir(exist_ok=True,parents=True)
                shutil.copyfile(Path("src")/package/file,dest)
        shutil.copyfile("data/table.json",d/"table.json")
        (d/"check.py").write_text("""import sys,json,os
sys.path.insert(0,os.getcwd())
from privtrace03.controls import schedule,decide,Opening,Offer
table=json.load(open('table.json'))
for line in sys.stdin:
    m,opening,events=json.loads(line)
    print(json.dumps([schedule(m,Opening(**opening),table),[decide(m,Offer(**e)) for e in events]]))
""")
        p=subprocess.run([sys.executable,"-I","check.py"],cwd=d,input="\n".join(observations),text=True,capture_output=True,check=True)
    if expected!=[json.loads(line) for line in p.stdout.splitlines()]:
        raise RuntimeError("Observation-only replay disagreed")
    print(f"{len(expected)} opening orders and {sum(len(x[1]) for x in expected)} delivery decisions matched.")

if __name__=="__main__":
    replay(Path("v03/results/main"))
