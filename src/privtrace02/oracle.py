"""Privileged comparator, isolated from the online implementation.
Enumerate optional delivery subsets in descending task feasibility. For equal exact utility
prefer the smallest number of deliveries; never allow a policy violation.
"""
from itertools import combinations


def best(case,candidates):
    owner=case["target"]
    other="archive" if owner=="client" else "client"
    for n in range(len(candidates)+1):
        for subset in combinations(range(len(candidates)),n):
            holdings={owner:set(case["prior_target"].lower()),other:set(case["prior_other"].lower()),"desk":set()}
            for idx in subset:
                e=candidates[idx]
                who,kind=e["who"],e["kind"]
                if kind=="digest" and case["restricted"] and (who!="desk" or
                    case["withdraw"] is not None and case["withdraw"]<=e["tick"]):
                    break
                holdings[who].add(kind)
                if who!="desk" and {"a","b"}<=holdings[who]:
                    break
            else:
                if set(case["ticket"].lower())<=holdings[owner] and (not case["staff_required"] or "digest" in holdings["desk"]):
                    return set(subset)
    return set()
