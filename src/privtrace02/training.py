from collections import Counter


def fit(development):
    counts={k:Counter(A=1,B=1) for k in ("early","late","pooled")}
    for case in development:
        if case["split"]!="development":
            raise ValueError("fit accepts historical development jobs only")
        # Both/none outcomes cancel between actions on empty recipient histories.
        if case["ticket"] in ("A","B"):
            for key in (case["cue"],"pooled"):
                counts[key][case["ticket"]]+=1
    return {k:dict(v) for k,v in counts.items()}
