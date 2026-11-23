import dataclasses
import inspect
import itertools
import unittest
from privtrace02.cases import generate_dispatch
from privtrace02.museum import generate_loans
from privtrace02.engine import run
from privtrace02.planning import View,choose
from privtrace02.training import fit
from privtrace02.scoring import score
from privtrace02.world import offers
from privtrace02.legacy.rules import adjudicate

TABLE={"early":{"A":8,"B":2},"late":{"A":2,"B":8},"pooled":{"A":5,"B":5}}
BASE=dict(next(generate_dispatch(0,1)),prior_target="",prior_other="",staff_required=False,
          cue="early",target="client",restricted=True,withdraw=None,available=True)
ONLINE=("local","full","reserve","utility","checked","no_cue","checked_greedy")


class Boundary(unittest.TestCase):
    def test_future_mutation(self):
        for method,ticket,withdraw in itertools.product(ONLINE,("A","B","AB",""),(None,4,6)):
            a=run(BASE,"degraded",method,TABLE)
            b=run(dict(BASE,ticket=ticket,withdraw=withdraw,key="unseen",seed=-1,secret=999,
                       late_tick=12,staff_required=True),"degraded",method,TABLE)
            self.assertEqual([x for x in a if x["tick"]<4],[x for x in b if x["tick"]<4])

    def test_capability_surface(self):
        self.assertEqual(set(View.__slots__),set("tick cue phase kind recipient seen version claim proof live_version".split()))
        self.assertEqual(list(inspect.signature(choose).parameters),["method","v","table"])
        v=View(3,"early","optional","a","client",(),1,"public","unqueried",0)
        for hidden in ("ticket","seed","secret","job","case","withdraw","next_event","booking"):
            with self.assertRaises(AttributeError):
                getattr(v,hidden)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            v.cue="late"

    def test_fit_accepts_development_only(self):
        with self.assertRaises(ValueError):
            fit([dict(BASE,split="validation")])

    def test_counterfactual_history(self):
        x=View(3,"early","optional","a","client",(),1,"public","unqueried",0)
        self.assertTrue(choose("utility",x,TABLE)[0])
        self.assertFalse(choose("utility",dataclasses.replace(x,seen=("b",)),TABLE)[0])
        self.assertFalse(choose("utility",dataclasses.replace(x,cue="late"),TABLE)[0])

    def test_grant_counterfactual(self):
        x=View(6,"late","staff","digest","desk",(),1,"restricted","restricted",1)
        self.assertTrue(choose("checked",x,TABLE)[0])
        self.assertFalse(choose("checked",dataclasses.replace(x,live_version=2),TABLE)[0])
        self.assertFalse(choose("checked",dataclasses.replace(x,proof="unavailable"),TABLE)[0])

    def test_stale_hidden_truth(self):
        s=dict(BASE,withdraw=4,lag=8,fault="inverted")
        for method,expected in [("utility",1),("checked",0)]:
            events=run(s,"degraded",method,TABLE)
            self.assertEqual(score(s,events)[0]["post"],expected)
            staff=next(e for e in events if e["phase"]=="staff")
            self.assertEqual(staff["view"]["version"],1)

    def test_no_secret_payload_in_view(self):
        initial=run(BASE,"clean","utility",TABLE)
        changed=run(dict(BASE,a=1-BASE["a"],b=1-BASE["b"]),"clean","utility",TABLE)
        self.assertEqual([e["view"] for e in initial],[e["view"] for e in changed])

    def test_distinct_recipients_do_not_combine(self):
        s=dict(BASE,secondary="b",ticket="A")
        self.assertEqual(score(s,run(s,"clean","full",TABLE))[0]["reconstructed"],0)

    def test_oracle_impossibility(self):
        s=dict(BASE,ticket="AB")
        self.assertEqual(score(s,run(s,"clean","oracle",TABLE))[0]["safe_exact"],0)
        self.assertEqual(score(s,run(s,"clean","local",TABLE))[0]["exact"],1)

    def test_oracle_dominates_safe_policies(self):
        for s in generate_loans(1,32):
            oracle=score(s,run(s,"degraded","oracle",TABLE))[0]
            self.assertEqual(oracle["exposure"],0)
            for method in ONLINE:
                m=score(s,run(s,"degraded",method,TABLE))[0]
                self.assertLessEqual(m["safe_exact"],oracle["safe_exact"])

    def test_monotone_route_times(self):
        for s in generate_dispatch(3,32):
            for offer in offers(s):
                ts=[x[0] for x in offer["route"]]
                self.assertEqual(ts,sorted(ts))

    def test_two_bits_gold_controls(self):
        for a,b,who in itertools.product(range(2),range(2),("archive","client")):
            s=dict(BASE,a=a,b=b,secret=a^b,ticket="")
            events=[dict(tick=i,recipient=r,kind=k,root="slip-"+k,value=s[k],phase="parallel",deliver=True)
                    for i,(r,k) in enumerate([("client","a"),(who,"b")])]
            m,_=score(s,events)
            self.assertEqual(m["correct"],int(who=="client"))
            self.assertEqual(m["exposure"],int(who=="client"))

    def test_legacy_equivalence(self):
        for who,k,v,seen,anc in itertools.product(("desk","archive"),("a","b","digest"),(1,2),((),("a",)),(True,False)):
            view=View(8,"late","request",k,who,seen,v,"restricted" if anc else "public","unqueried",0)
            for m in ("local","full"):
                ref=adjudicate(k,who,"service",v,seen,restricted_ancestor=anc,lineage=m=="full",history=m=="full")
                self.assertEqual(choose(m,view,TABLE)[0],ref=="allow")
