import unittest
import os
import csv
from Databasemanager import DatabaseManager
from CVSHandler import CSVHandler

class TestCSVHandler(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_csv_handler.db"
        self.db = DatabaseManager(self.db_path)
        self.id_course = self.db.ajouter_course("Informatique")
        self.csv_handler = CSVHandler(self.db, self.id_course)
        self.test_csv = "test_sessions_questions.csv"

        with open(self.test_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['nom_session', 'temps_passe', 'maitrise', 'question', 'reponse'])
            writer.writeheader()
            writer.writerow({'nom_session': 'Session Python', 'temps_passe': 120, 'maitrise': 80.0, 'question': "Qu'est-ce que Python ?", 'reponse': "Un langage de programmation."})
            writer.writerow({'nom_session': 'Session Python', 'temps_passe': 120, 'maitrise': 80.0, 'question': 'Capitale de la France ?', 'reponse': 'Paris'})

    def tearDown(self):
        self.db.fermer_connexion()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
        if os.path.exists("export_sessions.csv"):
            os.remove("export_sessions.csv")

    def test_importer_depuis_csv(self):
        # Ne crée pas de nouvelle instance DatabaseManager ici !
        self.csv_handler.importer_depuis_csv(self.test_csv)

        sessions = self.db.obtenir_sessions_par_course(self.id_course)
        self.assertEqual(len(sessions), 1)

        questions = self.db.get_questions_for_session(sessions[0]["id_session"])
        self.assertEqual(len(questions), 2)

    def test_exporter_vers_csv(self):
        # Importer d'abord, puis exporter
        self.csv_handler.importer_depuis_csv(self.test_csv)

        export_csv = "export_sessions.csv"
        self.csv_handler.exporter_vers_csv(export_csv)

        with open(export_csv, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            self.assertEqual(len(reader), 2)
            self.assertEqual(reader[0]['nom_session'], 'Session Python')
            self.assertEqual(reader[0]['temps_passe'], '120')
            self.assertEqual(reader[0]['maitrise'], '80.0')

if __name__ == '__main__':
    unittest.main()
