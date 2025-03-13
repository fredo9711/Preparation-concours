import unittest
from unittest.mock import MagicMock
from Cours import Course
from SessionQCM import SessionQCM

class TestCourse(unittest.TestCase):

    def setUp(self):
        self.session1 = SessionQCM(1, "Session 1", [])
        self.session1.temps_passe = lambda: 120  # 2 minutes
        self.session1.evaluer_session = lambda: 100  # 100%

        self.session2 = SessionQCM(2, "Session 2", [])
        self.session2 = SessionQCM(2, "Session 2", [])
        self.session2.temps_passe = lambda: 180  # 3 minutes
        self.session2.evaluer_session = lambda: 50  # 50%

        self.course = Course(1, "Cours de Mathématiques")
        self.course.sessions = [self.session1, self.session2]

    def test_temps_total_passe(self):
        self.assertEqual(self.course.temps_total_passe(), 300)

    def test_taux_maitrise_global(self):
        self.assertEqual(self.course.taux_maitrise_global(), 75.0)  # moyenne de 100% et 50%

if __name__ == '__main__':
    unittest.main()
