STAFF = frozenset(("preparer", "review", "desk", "left", "right", "reporter", "vault"))
PUBLIC = frozenset(("client", "calculator", "archive"))
KINDS = frozenset(("task", "a", "b", "raw", "digest"))


def adjudicate(kind, recipient, purpose, version, seen, *, restricted_ancestor=None, lineage=True, history=True):
    """Trusted structured input. Digest is the sole transform with a restricted ancestor."""
    if recipient not in STAFF | PUBLIC or kind not in KINDS or purpose not in ("service", "extra"):
        return "unknown"
    if restricted_ancestor is None:
        restricted_ancestor = kind == "digest"
    restricted = kind == "raw" or (lineage and restricted_ancestor)
    if restricted and version == 2:
        return "withdrawn"
    if restricted and recipient not in STAFF:
        return "scope"
    if kind != "task" and purpose != "service":
        return "purpose"
    if history and kind in ("a", "b") and recipient in PUBLIC:
        if ("a" if kind == "b" else "b") in seen:
            return "combination"
    return "allow"
