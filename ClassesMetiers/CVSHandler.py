import csv
from Databasemanager import DatabaseManager

class CSVHandler:
    def __init__(self, db_manager: DatabaseManager, id_course: int):
        self.db = db_manager
        self.id_course = id_course

    def importer_depuis_csv(self, chemin_csv: str):
        sessions_csv = {}
        with open(chemin_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for ligne in reader:
                nom_session = ligne["nom_session"]
                question = ligne["question"]
                reponse = ligne["reponse"]
                temps_passe = int(ligne.get("temps_passe", 0))
                maitrise = float(ligne.get("maitrise", 0.0))

                if nom_session not in sessions_csv:
                    sessions_csv[nom_session] = {
                        'temps_passe': temps_passe,
                        'maitrise': maitrise,
                        'questions': []
                    }

                sessions_csv[nom_session]['questions'].append((question, reponse))

        sessions_db = {s["nom_session"]: s for s in self.db.obtenir_sessions_par_course(self.id_course)}

        # Synchroniser les sessions et questions
        for nom_session, details in sessions_csv.items():
            if nom_session in sessions_db:
                session_id = sessions_db[nom_session]["id_session"]
                self.db.mettre_a_jour_session(session_id, details['temps_passe'], details['maitrise'])
            else:
                session_id = self.db.ajouter_session(nom_session, self.id_course, details['temps_passe'], details['maitrise'])

            questions_db = {q["question"]: q for q in self.db.get_questions_for_session(session_id)}

            # Ajout ou mise à jour des questions
            for question, reponse in details['questions']:
                if question in questions_db:
                    if questions_db[question]["reponse"] != reponse:
                        self.db.update_question(questions_db[question]["id_question"], question, reponse)
                else:
                    self.db.ajouter_question(question, reponse, session_id)

            # Supprimer les questions absentes du CSV
            questions_csv_set = set(q[0] for q in details['questions'])
            for question_db in questions_db:
                if question_db not in questions_csv_set:
                    self.db.delete_question(questions_db[question_db]["id_question"])

        # Supprimer les sessions absentes du CSV
        sessions_csv_set = set(sessions_csv.keys())
        for nom_session_db, data_session_db in sessions_db.items():
            if nom_session_db not in sessions_csv_set:
                self.db.supprimer_session(data_session_db["id_session"])

    def exporter_vers_csv(self, chemin_csv: str):
        sessions_db = self.db.obtenir_sessions_par_course(self.id_course)

        with open(chemin_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['nom_session', 'temps_passe', 'maitrise', 'question', 'reponse']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for session in sessions_db:
                questions_db = self.db.get_questions_for_session(session["id_session"])
                for q in questions_db:
                    writer.writerow({
                        'nom_session': session["nom_session"],
                        'temps_passe': session["temps_passe"],
                        'maitrise': session["taux_maitrise"],
                        'question': q["question"],
                        'reponse': q["reponse"]
                    })
