from typing import List
from SessionQCM import SessionQCM

class Course:
    def __init__(self, id_course: int, nom_course: str):
        self.id_course = id_course
        self.nom_course = nom_course
        self.sessions: List[SessionQCM] = []

    def ajouter_session(self, session: SessionQCM):
        self.sessions.append(session)

    def retirer_session(self, id_session: int):
        self.sessions = [s for s in self.sessions if s.id_session != id_session]

    def temps_total_passe(self) -> int:
        return sum(session.temps_passe() for session in self.sessions)

    def taux_maitrise_global(self) -> float:
        if not self.sessions:
            return 0.0
        taux_total = sum(session.evaluer_session() for session in self.sessions)
        return round(taux_total / len(self.sessions), 2)
