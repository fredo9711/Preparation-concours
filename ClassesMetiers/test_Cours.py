import unittest
from unittest.mock import MagicMock
from Cours import Course
from SessionQCM import SessionQCM
import os
from Databasemanager import DatabaseManager

class TestCourse(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_course.db"
        self.db = DatabaseManager(self.db_path)
        self.course = Course("Mathématiques", self.db)
        self.course.id_course = self.db.ajouter_course("Mathématiques")

        # Création et sauvegarde de sessions
        self.session1 = SessionQCM("Algèbre", self.db, self.course.id_course, temps_passe=120, maitrise=100.0,courbe_oublie=0,prochaine_revision=0)
        self.session2 = SessionQCM("Géométrie", self.db, self.course.id_course, temps_passe=240, maitrise=80.0,courbe_oublie=0,prochaine_revision=0)
        self.course.ajouter_session(self.session1)
        self.course.ajouter_session(self.session2)

    def tearDown(self):
        self.db.conn.close()
        import os
        os.remove(self.db_path)

    def test_sauvegarde_et_chargement_course_sessions(self):
        # Sauvegarde
        self.course.sauvegarder(self.db)

        # Chargement
        course_charge = Course("Mathématiques", self.db, id_course=self.course.id_course)

        self.assertEqual(course_charge.nom_course, "Mathématiques")
        self.assertEqual(len(course_charge.sessions), 2)
        self.assertEqual(course_charge.sessions[0].nom_session, "Algèbre")
        self.assertEqual(course_charge.sessions[1].nom_session, "Géométrie")

    def test_supprimer_session(self):
        self.course.sauvegarder(self.db)
        self.course.supprimer_session(self.session1.id_session)

        sessions_restantes = self.db.obtenir_sessions_par_course(self.course.id_course)
        self.assertEqual(len(sessions_restantes), 1)
        self.assertEqual(sessions_restantes[0]["nom_session"], "Géométrie")

if __name__ == '__main__':
    unittest.main()
