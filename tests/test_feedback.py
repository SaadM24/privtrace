import unittest
from privtrace02.feedback import ClosedTickets


class Feedback(unittest.TestCase):
    def test_close_boundary_and_forgetting(self):
        prior={k:{"A":1,"B":1} for k in ("early","late")}
        b=ClosedTickets(prior,2,2)
        old=b.snapshot()
        b.close("early","A")
        self.assertEqual(old["early"]["A"],1)
        self.assertEqual(b.snapshot()["early"]["A"],2)
        b.close("late","AB")
        b.close("late","B")
        self.assertEqual(b.snapshot(),{"early":{"A":1,"B":1},"late":{"A":1,"B":2}})

    def test_snapshot_isolation(self):
        b=ClosedTickets({k:{"A":3,"B":2} for k in ("early","late")},2,2)
        snap=b.snapshot()
        snap["early"]["A"]=900
        self.assertAlmostEqual(b.snapshot()["early"]["A"],1.2)
