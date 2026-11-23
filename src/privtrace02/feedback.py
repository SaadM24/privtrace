from collections import deque


class ClosedTickets:
    """Updated strictly after a job closes; no workload file or job handle."""
    def __init__(self,prior,window,strength):
        self.prior=prior
        self.recent=deque(maxlen=window)
        self.strength=strength

    def snapshot(self):
        rows={}
        for cue in ("early","late"):
            base=self.prior[cue]
            total=sum(base.values())
            rows[cue]={k:self.strength*base[k]/total for k in ("A","B")}
        for cue,ticket in self.recent:
            if ticket in ("A","B"):
                rows[cue][ticket]+=1
        return rows

    def close(self,cue,ticket):
        self.recent.append((cue,ticket))
