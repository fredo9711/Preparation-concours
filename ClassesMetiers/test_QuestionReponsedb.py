import unittest
from Databasemanager import DatabaseManager
from QuestionReponse import Question

class TestQuestionPersistence(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager("test_questions.db")
        # insérer d'abord une session temporaire pour avoir un id_session valide
        self.db.cursor.execute("INSERT INTO sessions (nom_session, id_course, temps_passe, taux_maitrise) VALUES ('Session Temp', 1, 120, 100)")
        self.db.conn.commit()
        self.id_session = self.db.cursor.lastrowid

    def tearDown(self):
        self.db.conn.close()
        import os
        os.remove("test_questions.db")

    def test_insert_and_get_question(self):
        id_question = self.db.ajouter_question(
            "Capitale de la France ?", "Paris", self.db.cursor.lastrowid
        )

        fetched_question = self.db.get_question(id_question)
        self.assertIsNotNone(fetched_question)
        self.assertEqual(fetched_question["question"], "Capitale de la France ?")
        self.assertEqual(fetched_question["reponse"], "Paris")

    def test_update_question(self):
        id_question = self.db.ajouter_question(
            "2+2 ?", "4", self.db.cursor.lastrowid
        )
        self.db.update_question(id_question, "2+2 ?", "4")

        updated_question = self.db.get_question(id_question)
        self.assertEqual(updated_question["question"], "2+2 ?")

    def test_get_questions_for_session(self):
        self.db.ajouter_question("Q1", "R1", self.db.cursor.lastrowid)
        self.db.ajouter_question("Q2", "R2", self.db.cursor.lastrowid)

        questions = self.db.get_questions_for_session(self.id_session)
        self.assertEqual(len(questions), 2)

if __name__ == '__main__':
    unittest.main()
