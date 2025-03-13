import sqlite3
from typing import List

class DatabaseManager:
    def __init__(self, db_path="app.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id_course INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_course TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id_session INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_session TEXT NOT NULL,
                id_course INTEGER,
                temps_passe INTEGER DEFAULT 0,
                taux_maitrise FLOAT DEFAULT 0.0,
                FOREIGN KEY (id_course) REFERENCES courses(id_course) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    # --- CRUD sur Cours ---
    def ajouter_course(self, nom_course: str) -> int:
        self.cursor.execute("INSERT INTO courses (nom_course) VALUES (?)", (nom_course,))
        self.conn.commit()
        return self.cursor.lastrowid

    def supprimer_course(self, id_course: int):
        self.cursor.execute("DELETE FROM courses WHERE id_course=?", (id_course,))
        self.conn.commit()

    def obtenir_course(self, id_course: int):
        self.cursor.execute("SELECT * FROM courses WHERE id_course=?", (id_course,))
        return self.cursor.fetchone()

    def obtenir_tous_courses(self):
        self.cursor.execute("SELECT * FROM courses")
        return self.cursor.fetchall()

    def modifier_nom_course(self, id_course: int, nouveau_nom: str):
        self.cursor.execute("UPDATE courses SET nom_course=? WHERE id_course=?", (nouveau_nom, id_course))
        self.conn.commit()

    # --- CRUD sur Sessions ---
    def ajouter_session(self, nom_session: str, id_course: int, temps_passe: int, taux_maitrise: float) -> int:
        self.cursor.execute("""
            INSERT INTO sessions (nom_session, id_course, temps_passe, taux_maitrise) 
            VALUES (?, ?, ?, ?)""", 
            (nom_session, id_course, temps_passe, taux_maitrise)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def obtenir_sessions_par_course(self, id_course: int):
        self.cursor.execute("SELECT * FROM sessions WHERE id_course=?", (id_course,))
        return self.cursor.fetchall()

    def supprimer_course(self, id_course: int):
        self.cursor.execute("DELETE FROM courses WHERE id_course=?", (id_course,))
        self.conn.commit()

    def supprimer_session(self, id_session: int):
        self.cursor.execute("DELETE FROM sessions WHERE id_session=?", (id_session,))
        self.conn.commit()

    def mettre_a_jour_session(self, id_session: int, temps_passe: int, taux_maitrise: float):
        self.cursor.execute("""
            UPDATE sessions SET temps_passe=?, taux_maitrise=? WHERE id_session=?""",
            (temps_passe, taux_maitrise, id_session)
        )
        self.conn.commit()

    def fermer_connexion(self):
        self.conn.close()
