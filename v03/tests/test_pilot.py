import importlib.util
import unittest
from pathlib import Path

file=Path(__file__).resolve().parents[1]/"pilot.py"
spec=importlib.util.spec_from_file_location("pilot",file)
pilot=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


class PilotContract(unittest.TestCase):
    def test_ack(self):
        self.assertEqual(pilot.assess("REVIEW ACCEPTED",3,"REVIEW ACCEPTED"),(True,"clear",15))
    def test_free_prose_unknown(self):
        self.assertIsNone(pilot.assess("REVIEW ACCEPTED meet at my usual place",3,"REVIEW ACCEPTED")[2])
    def test_composition(self):
        self.assertEqual(pilot.assess("REVIEW ACCEPTED The dossier places the site on the coast.",3,"REVIEW ACCEPTED")[1],"exposure")
