import unittest
import os
from datetime import datetime
from Databasemanager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_app.db"
        self.db = DatabaseManager(self.db_path)

    def tearDown(self):
        self.db.fermer_connexion()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ajouter_et_obtenir_course(self):
        id_course = self.db.ajouter_course("Mathématiques")
        course = self.db.obtenir_course(id_course=id_course)

        self.assertIsNotNone(course)
        self.assertEqual(course["nom_course"], "Mathématiques")

    def test_modifier_nom_course(self):
        id_course = self.db.ajouter_course("Physique")
        self.db.modifier_nom_course(id_course, "Physique-Chimie")
        course = self.db.obtenir_course(id_course=id_course)

        self.assertEqual(course["nom_course"], "Physique-Chimie")

    def test_supprimer_course(self):
        id_course = self.db.ajouter_course("Histoire")
        self.db.supprimer_course(id_course)
        course = self.db.obtenir_course(id_course=id_course)

        self.assertIsNone(course)

    def test_ajouter_et_obtenir_session(self):
        id_course = self.db.ajouter_course("Géographie")
        id_session = self.db.ajouter_session("Capitale QCM", id_course, 180, 85.5)
        sessions = self.db.obtenir_sessions_par_course(id_course)

        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]["nom_session"], "Capitale QCM")
        self.assertEqual(sessions[0]["temps_passe"], 180)
        self.assertAlmostEqual(sessions[0]["taux_maitrise"], 85.5)

    def test_mettre_a_jour_session(self):
        id_course = self.db.ajouter_course("Géographie")
        id_session = self.db.ajouter_session("Villes", id_course, 120, 50.0)

        self.db.mettre_a_jour_session(id_session,300,75.5,0,datetime(2025,8,21))
        sessions = self.db.obtenir_sessions_par_course(id_course)

        self.assertEqual(sessions[0]["temps_passe"], 300)
        self.assertAlmostEqual(sessions[0]["taux_maitrise"], 75.5)

    def test_supprimer_session(self):
        id_course = self.db.ajouter_course("Géographie")
        id_session = self.db.ajouter_session("Pays du monde", id_course, 240, 90.0)

        self.db.supprimer_session(id_session)
        sessions = self.db.obtenir_sessions_par_course(id_course)

        self.assertEqual(len(sessions), 0)

if __name__ == '__main__':
    unittest.main()
