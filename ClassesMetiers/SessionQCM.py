from datetime import datetime, timedelta
from typing import List
from QuestionReponse import Question

class SessionQCM:
    def __init__(self,id_session:int,nom_session: str,questions:List[Question]):
        self.id_session = id_session
        self.id_course = 0
        self.nom_session = nom_session
        self.questions = questions
        self.niveau_apprentissage = 0
        self.derniere_revision = None # a changer
        self.maitrise = 0.0

    def commencer_session(self):
        self.start_time = datetime.now()

    def terminer_session(self):
        self.end_time = datetime.now()
        self.derniere_revision = self.end_time

    def Temps_passe(self) -> int:
        return int((self.end_time-self.start_time).total_seconds())

    def evaluer_session(self,reponses_utilisateur: List[str]) -> float:
        if len(reponses_utilisateur) != len(self.questions):
            raise ValueError("Nombre incorrects de réponse fournis")
        
        scores = [question.verification_reponse(reponse) for question,reponse in zip(self.questions,reponses_utilisateur)]

        return sum(scores)/len(scores)
    
    def upourdowngrade_maitrise(self,niveau_apprentissage):
        self.maitrise = niveau_apprentissage*0.25