import unittest
from dataclasses import fields,replace
from privtrace03.benchmark import jobs
from privtrace03.controls import Opening,Offer,decide,schedule
from privtrace03.experiment import simulate
from privtrace03.evaluation import score
from privtrace03.language import dictionary,literal,wording,MASK

TABLE={"early":{"A":38,"B":5},"late":{"A":17,"B":39}}
S=next(jobs(1,1,"test"))
METHODS=("open","greedy","minimum","cue","eligible","checked","no_history","text_gate")


class Validation(unittest.TestCase):
    def test_hidden_ticket_counterfactual(self):
        for m in METHODS:
            a=simulate(S,m,"mixed",TABLE)
            b=simulate(dict(S,id="different",seed=99,later=[2,1],after=["z"]*3,withdraw=6,
                            requires_doc=not S["requires_doc"]),m,"mixed",TABLE)
            self.assertEqual(a[:2],b[:2])
            self.assertEqual([e for e in a[2] if e["t"]<5],[e for e in b[2] if e["t"]<5])

    def test_schema(self):
        for cls in (Opening,Offer):
            self.assertFalse({"seed","site","later","withdraw","requires_doc","split"} & {f.name for f in fields(cls)})

    def test_history_counterfactual(self):
        v=Offer("certify","p0","service",3,15,False,False,True,"",0,1)
        self.assertTrue(decide("checked",v)[0])
        self.assertFalse(decide("checked",replace(v,history=5))[0])

    def test_permission(self):
        v=Offer("memo","staff","service",15,15,True,False,True,"",1,1)
        self.assertTrue(decide("checked",v)[0])
        self.assertFalse(decide("checked",replace(v,expired=True))[0])
        self.assertFalse(decide("checked",replace(v,verified=False))[0])

    def test_alias_preference(self):
        v=Opening((0,),("pool","pool","other"),1,"late")
        self.assertEqual(schedule("eligible",v,TABLE)[0],2)

    def test_lexical_controls(self):
        self.assertIsNone(dictionary("They said it might be the upper one."))
        self.assertEqual(dictionary("The form uses Alder as an example."),15)
        self.assertNotEqual(literal("The form uses Alder as an example."),15)
        self.assertEqual(dictionary("outside the northern district"),12)

    def test_quorum_distinct(self):
        events=simulate(S,"open","clean",TABLE)[2]
        for e in events:
            if e["phase"]=="vote":
                e["role"]=0
        self.assertFalse(score(dict(S,quota=2),events)[0]["exact"])

    def test_complete_gold_semantics(self):
        for s in jobs(101,24,"test"):
            for label in (s["early"],s["late"],s["prior"][1]):
                self.assertTrue((1<<s["site"])&MASK[label])
            self.assertEqual((MASK[s["early"]]&MASK[s["late"]]).bit_count(),1)

    def test_no_cross_recipient_inference(self):
        event=dict(t=1,phase="vote",role=0,who="p0",truth=3,asset="ordinary",purpose="service",sent=True)
        a=score(S,[event,dict(event,who="p1",truth=5)])[0]
        b=score(S,[event,dict(event,truth=5)])[0]
        self.assertEqual((a["identified"],b["identified"]),(0,1))
