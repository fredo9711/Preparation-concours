import unittest
import os
import csv
from datetime import datetime
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
            writer = csv.DictWriter(csvfile, fieldnames=[
                'nom_session', 'temps_passe', 'maitrise',
                'courbe_oubli', 'prochaine_revision',
                'question', 'reponse'
            ])
            writer.writeheader()
            writer.writerow({
                'nom_session': 'Session Python',
                'temps_passe': 120,
                'maitrise': 80.0,
                'courbe_oubli': 2,
                'prochaine_revision': '2025-08-21 14:00:00',
                'question': "Qu'est-ce que Python ?",
                'reponse': "Un langage de programmation."
            })
            writer.writerow({
                'nom_session': 'Session Python',
                'temps_passe': 120,
                'maitrise': 80.0,
                'courbe_oubli': 2,
                'prochaine_revision': '2025-08-21 14:00:00',
                'question': 'Capitale de la France ?',
                'reponse': 'Paris'
            })

    def tearDown(self):
        self.db.fermer_connexion()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
        if os.path.exists("export_sessions.csv"):
            os.remove("export_sessions.csv")

    def test_importer_depuis_csv(self):
        # Importer le CSV dans la base de données
        self.csv_handler.importer_depuis_csv(self.test_csv)

        # Vérification des sessions
        sessions = self.db.obtenir_sessions_par_course(self.id_course)
        self.assertEqual(len(sessions), 1)

        session = sessions[0]
        self.assertEqual(session["nom_session"], "Session Python")
        self.assertEqual(session["temps_passe"], 120)
        self.assertAlmostEqual(session["taux_maitrise"], 80.0)
        self.assertEqual(session["courbe_oubli"], 2)
        self.assertEqual(session["prochaine_revision"], '2025-08-21 14:00:00')

        # Vérification des questions
        questions = self.db.get_questions_for_session(session["id_session"])
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0]["question"], "Qu'est-ce que Python ?")
        self.assertEqual(questions[0]["reponse"], "Un langage de programmation.")
        self.assertEqual(questions[1]["question"], "Capitale de la France ?")
        self.assertEqual(questions[1]["reponse"], "Paris")

    def test_exporter_vers_csv(self):
        # Importer les données, puis les exporter
        self.csv_handler.importer_depuis_csv(self.test_csv)

        export_csv = "export_sessions.csv"
        self.csv_handler.exporter_vers_csv(export_csv)

        # Vérification du contenu du fichier exporté
        with open(export_csv, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            self.assertEqual(len(reader), 2)

            # Vérification de la première ligne
            self.assertEqual(reader[0]['nom_session'], 'Session Python')
            self.assertEqual(reader[0]['temps_passe'], '120')
            self.assertEqual(reader[0]['maitrise'], '80.0')
            self.assertEqual(reader[0]['courbe_oubli'], '2')
            self.assertEqual(reader[0]['prochaine_revision'], '2025-08-21 14:00:00')
            self.assertEqual(reader[0]['question'], "Qu'est-ce que Python ?")
            self.assertEqual(reader[0]['reponse'], "Un langage de programmation.")

            # Vérification de la deuxième ligne
            self.assertEqual(reader[1]['nom_session'], 'Session Python')
            self.assertEqual(reader[1]['question'], 'Capitale de la France ?')
            self.assertEqual(reader[1]['reponse'], 'Paris')

if __name__ == '__main__':
    unittest.main()
