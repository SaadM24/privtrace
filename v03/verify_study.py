"""Independent standard-library scoring of complete logs. No project imports."""
import argparse,csv,gzip,json
from pathlib import Path


def verify(out):
    cases={s["id"]:s for s in map(json.loads,(out/"cases.jsonl").read_text().splitlines())}
    cfg=json.loads(Path("v03/config.json").read_text())
    assert len(cases)==sum(len(cfg[k]) for k in ("development","validation","test"))*cfg["jobs_per_seed"]
    count=event_count=0
    keys=set()
    valid={"north":{0,1},"south":{2,3},"coast":{0,2},"inland":{1,3},"neutral":set(range(4))}
    with gzip.open(out/"traces.jsonl.gz","rt") as tr,(out/"scores.csv").open() as f:
        for row,line in zip(csv.DictReader(f),tr,strict=True):
            x=json.loads(line)
            key=tuple(x[k] for k in ("job","method","condition"))
            assert key not in keys and key==tuple(row[k] for k in ("job","method","condition"))
            keys.add(key)
            s=cases[x["job"]]
            assert [e["role"] for e in x["events"] if e["phase"]=="certify"]==s["later"]
            assert sorted(e["role"] for e in x["events"] if e["phase"]=="vote")==[0,1,2]
            witnesses=[]
            holdings={}
            votes=set()
            cert=set()
            staff=False
            expired=ids=denials=sent=0
            for i,e in enumerate(x["events"]):
                phase=e["phase"]
                who={"prior":s["prior"][0],"memo":"staff","copy":s["after"][0]}.get(phase)
                if who is None:
                    who=(s["mail"] if phase=="vote" else s["after"])[e["role"]]
                assert who==e["who"]
                label={"prior":s["prior"][1],"memo":"neutral","vote":s["early"],"certify":s["late"],"copy":s["late"]}[phase]
                den=valid[label]
                assert s["site"] in den and sum(2**j for j in den)==e["truth"]
                old=holdings.get(who,set(range(4)))
                new=old&den
                identified=who!="staff" and len(new)==1 and len(old)>1
                restricted=s["restricted"] and phase in ("memo","copy")
                stale=restricted and s["withdraw"] is not None and s["withdraw"]<=e["t"]
                bad=identified or stale or restricted and who!="staff" or phase=="copy" and s["editorial"]!="service"
                if not e["sent"]:
                    denials+=not bad
                    continue
                holdings[who]=new
                sent+=phase!="prior"
                if bad:
                    witnesses.append(i)
                ids+=identified
                expired+=stale
                if phase=="vote":
                    votes.add(e["role"])
                if phase=="certify":
                    cert.add(e["role"])
                staff|=phase=="memo"
            exact=len(votes)>=s["quota"] and cert==set(s["later"]) and (staff or not s["requires_doc"])
            checks=dict(exact=exact,safe=exact and not witnesses,exposure=bool(witnesses),post=bool(expired),
                        identified=ids,allowed_blocks=denials,delivered=sent)
            assert all(int(row[k])==int(v) for k,v in checks.items())
            assert [i for i,_ in x["evidence"]]==witnesses
            count+=1
            event_count+=len(x["events"])
    assert count==len(cases)*len(cfg["methods"])*len(cfg["conditions"])
    print(f"Independent replay matched {count} scores, {event_count} event records and all violation indices.")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    verify(p.parse_args().out)
