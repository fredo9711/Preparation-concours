from typing import List
from SessionQCM import SessionQCM
from Databasemanager import DatabaseManager

class Course:
    def __init__(self,nom_course: str, db_manager:DatabaseManager, id_course:int=None ):
        self.id_course = id_course
        self.nom_course = nom_course
        self.sessions: List[SessionQCM] = []
        self.db = db_manager

        if self.id_course:
            self.charger_sessions_depuis_db()

    def ajouter_session(self, session: SessionQCM):
        session.id_course = self.id_course
        self.sessions.append(session)

    def charger_sessions_depuis_db(self):
        sessions_data = self.db.obtenir_sessions_par_course(self.id_course)
        
        self.sessions = [
            SessionQCM( nom_session=session["nom_session"],
                        id_course=session["id_course"],
                        temps_passe=session["temps_passe"],
                        maitrise=session["taux_maitrise"],
                        db_manager=self.db,
                        id_session=session["id_session"],
                        courbe_oublie=session["courbe_oubli"],
                        prochaine_revision=session["prochaine_revision"]
                        )
                        for session in sessions_data

        ]
    
    def sauvegarder_course(self):
        if not self.id_course:
            self.id_course = self.db.ajouter_course(self.nom_course)
        else:
            self.db.modifier_nom_course(self.id_course, self.nom_course)

        for session in self.sessions:
            session.sauvegarder_session(session.temps_passe, session.maitrise)

    def supprimer_session(self, id_session):
        self.db.supprimer_session(id_session)
        self.sessions = [s for s in self.sessions if s.id_session != id_session]


    def retirer_session(self, id_session: int):
        self.sessions = [s for s in self.sessions if s.id_session != id_session]

    def temps_total_passe(self) -> int:
        return sum(session.temps_passe() for session in self.sessions)

    def taux_maitrise_global(self) -> float:
        if not self.sessions:
            return 0.0
        taux_total = sum(session.evaluer_session() for session in self.sessions)
        return round(taux_total / len(self.sessions), 2)

    def sauvegarder(self, db_manager):
        if not self.id_course:
            self.id_course = db_manager.ajouter_course(self.nom_course)
        for session in self.sessions:
            if session.id_session is None:
                session.id_session = db_manager.ajouter_session(
                    nom_session=session.nom_session,
                    id_course=self.id_course,
                    temps_passe=session.temps_passe,
                    taux_maitrise=session.maitrise
                )
            else:
                db_manager.mettre_a_jour_session(
                    session.id_session,
                    session.temps_passe(),
                    session.evaluer_session()
                )

    @classmethod
    def charger(cls, id_course, db_manager):
        data_course = db_manager.obtenir_course(id_course)
        if not data_course:
            return None

        course = cls(nom_course=data_course["nom_course"])
        course.id_course = id_course

        sessions_data = db_manager.obtenir_sessions_par_course(id_course)
        for data_session in sessions_data:
            session = SessionQCM(
                id_session=data_session["id_session"],
                nom_session=data_session["nom_session"],
                temps_passe=data_session["temps_passe"],
                taux_maitrise=data_course["taux_maitrise"],
            )
            course.sessions.append(session)

        return course
