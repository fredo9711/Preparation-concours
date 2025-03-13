import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from SessionQCM import SessionQCM
from QuestionReponse import Question
from Databasemanager import DatabaseManager
import os

class TestSessionQCM(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_session_qcm.db"
        self.db = DatabaseManager(self.db_path)
        self.id_course = self.db.ajouter_course("Informatique")
        self.session = SessionQCM(
            nom_session="Session Python",
            id_course=self.id_course,
            db_manager=self.db,
            temps_passe=0,
            maitrise=0.0
        )

        # Sauvegarde session pour obtenir id_session
        self.session.sauvegarder_session(0, 0.0)

        # Ajouter des questions
        self.q1 = Question(question="Qu'est-ce que Python ?", reponse="Un langage de programmation.")
        self.q2 = Question(question="Capitale de la France ?", reponse="Paris")

        self.session.ajouter_question(self.q1)
        self.session.ajouter_question(self.q2)

    """ def test_temps_passe(self):
        self.session.start_time = datetime(2025, 3, 12, 10, 0, 0)
        self.session.end_time = datetime(2025, 3, 12, 10, 5, 0)
        self.assertEqual(self.session.temps_passe(), 300)  # 5 min = 300 sec"""


    def tearDown(self):
        self.db.fermer_connexion()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


    """def test_evaluer_session(self):
        reponses = ["Un système qui apprend par expérience.", "4"]
        score = self.session.evaluer_session(reponses)
        self.assertEqual(score,0.5)
        #self.assertTrue(0 <= score <= 10)"""


    def test_ajouter_et_charger_questions(self):
        nouvelle_session = SessionQCM(
            nom_session="Session Python",
            id_course=self.id_course,
            db_manager=self.db,
            temps_passe=0,
            maitrise=0.0,
            id_session=self.session.id_session
        )

        self.assertEqual(len(nouvelle_session.questions), 2)
        self.assertEqual(nouvelle_session.questions[0].question, "Qu'est-ce que Python ?")
        self.assertEqual(nouvelle_session.questions[1].question, "Capitale de la France ?")


    def test_evaluer_session_toutes_correctes(self):
        reponses = ["Un langage de dévellopement informatique.", "C'est Paris"]
        score = self.session.evaluer_session(reponses)
        print(score)
        self.assertEqual(score, 1.0)

    def test_evaluer_session_toutes_incorrectes(self):
        reponses = ["Un serpent.", "Lyon"]
        score = self.session.evaluer_session(reponses)
        print(score)
        self.assertEqual(score, 0)

    def test_evaluer_session_mixtes(self):
        reponses = ["Un langage de script conçu pour automatiser des tâches", "Lyon"]
        print(reponses)
        score = self.session.evaluer_session(reponses)
        print(score)
        self.assertEqual(score, 0.5)

if __name__ == '__main__':
    unittest.main()
