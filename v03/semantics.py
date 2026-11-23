"""Natural-language control set. All determinate meanings are authored denotations."""
import argparse,csv,json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from privtrace03.language import MASK,wording,dictionary,literal


def corpus():
    for split,styles in [("development",(0,1)),("validation",(2,)),("test",(3,4,5))]:
        for style in styles:
            for label in [*MASK,"uncertain"]:
                for wrap in (range(3) if label in ("north","south","coast","inland") else range(1)):
                    sentence=wording(label,style,wrap)
                    yield dict(split=split,style=style,label=label,text=sentence,meaning=MASK.get(label))


def main(out):
    samples=list(corpus())
    train={r["text"]:r["meaning"] for r in samples if r["split"]=="development" and r["meaning"] is not None}
    learner=make_pipeline(TfidfVectorizer(analyzer="char",ngram_range=(2,5)),
                          LogisticRegression(max_iter=500,random_state=303))
    learner.fit(list(train),list(train.values()))
    rows=[]
    for s in samples:
        pred=int(learner.predict([s["text"]])[0])
        for prior in (15,3,12,5,10):
            gold=s["meaning"]
            if gold is not None and not prior&gold:
                continue
            flag=None if gold is None else (prior&gold).bit_count()==1
            for name,obs in (("literal",literal(s["text"])),("dictionary",dictionary(s["text"])),("char_model",pred)):
                # Contradiction is insufficient for an inference and gets abstention.
                guess=None if obs is None or not prior&obs else (prior&obs).bit_count()==1
                rows.append(dict(**s,prior=prior,method=name,pred_mask=obs,
                                 gold_flag=flag,pred_flag=guess))
    with (out/"language.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0])
        w.writeheader()
        w.writerows(rows)
    (out/"language_corpus.jsonl").write_text("".join(json.dumps(r)+"\n" for r in samples))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    main(p.parse_args().out)
