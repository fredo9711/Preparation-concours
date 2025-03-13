from datetime import datetime, timedelta
from typing import List
from QuestionReponse import Question
from Databasemanager import DatabaseManager

class SessionQCM:
    def __init__(self,nom_session: str,db_manager: DatabaseManager,id_course:int,temps_passe:int,maitrise:float,id_session=None):
        self.id_session = id_session
        self.id_course = id_course
        self.nom_session = nom_session
        self.db = db_manager
        self.questions: List[Question] =[]
        self.temps_passe = temps_passe
        self.maitrise = maitrise


        if self.id_session:
            self.charger_questions_depuis_db()

    def ajouter_question(self, question: Question):
        question.id_session = self.id_session
        question.id_question = self.db.ajouter_question(
            question=question.question,
            reponse=question.reponse,
            id_session=self.id_session
        )
        self.questions.append(question)

    def charger_questions_depuis_db(self):
        questions_data = self.db.get_questions_for_session(self.id_session)
        self.questions = [
            Question(
                id_question=q["id_question"],
                question=q["question"],
                reponse=q["reponse"],
                id_session=self.id_session
            )
            for q in questions_data
        ]

    def sauvegarder_session(self, temps_passe: int, taux_maitrise: float):
        if self.id_session is None:
            self.id_session = self.db.ajouter_session(
                self.nom_session, self.id_course, temps_passe, taux_maitrise
            )
        else:
            self.db.mettre_a_jour_session(self.id_session, temps_passe=temps_passe, taux_maitrise=taux_maitrise)

    def supprimer_question(self, id_question):
        self.db.delete_question(id_question)
        self.questions = [q for q in self.questions if q.id_question != id_question]

    def supprimer_session(self):
        if self.id_session:
            self.db.supprimer_session(self.id_session)
            self.questions.clear()



    """def commencer_session(self):
        self.start_time = datetime.now()

    def terminer_session(self):
        self.end_time = datetime.now()
       

    def Temps_passe(self):
        return int((self.end_time-self.start_time).total_seconds())"""

    def evaluer_session(self,reponses_utilisateur: List[str]) -> float:
        if len(reponses_utilisateur) != len(self.questions):
            raise ValueError("Nombre incorrects de réponse fournis")
        
        scores = [question.verification_reponse(reponse) for question,reponse in zip(self.questions,reponses_utilisateur)]

        return sum(scores)/len(scores)
    
