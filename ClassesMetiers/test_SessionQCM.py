import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from SessionQCM import SessionQCM
from QuestionReponse import Question

class TestSessionQCM(unittest.TestCase):

    def setUp(self):
        self.question1 = Question(1, "Capitale France ?", "Paris")
        self.question2 = Question(2, "2+2 ?", "4")
        self.session = SessionQCM(
            id_session=1,
            nom_session="Test session",
            questions=[self.question1, self.question2]
        )

    def test_temps_passe(self):
        self.session.start_time = datetime(2025, 3, 12, 10, 0, 0)
        self.session.end_time = datetime(2025, 3, 12, 10, 5, 0)
        self.assertEqual(self.session.temps_passe(), 300)  # 5 min = 300 sec

    def test_evaluer_session(self):
        reponses = ["Un système qui apprend par expérience.", "4"]
        score = self.session.evaluer_session(reponses)
        self.assertEqual(score,0.5)
        #self.assertTrue(0 <= score <= 10)

if __name__ == '__main__':
    unittest.main()
