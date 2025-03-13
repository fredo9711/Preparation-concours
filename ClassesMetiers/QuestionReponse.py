import requests
import json

class Question:
    def __init__(self, question: str, reponse: str,id_session=None,id_question=None):
        self.id_question = id_question
        self.question = question
        self.reponse = reponse
        self.id_session = id_session

    def verification_reponse(self,utilisateur_reponse:str)-> int:
        api_url = "http://localhost:1337/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        prompt = f"""Je vais te donner une question suivie de la réponse correcte, et enfin une réponse que j’ai moi-même rédigée.
TA TÂCHE EST IMPÉRATIVEMENT DE ME RETOURNER UN ENTIER UNIQUEMENT (entre 0 et 100) basé sur ces critères :

- 100 : La réponse est parfaitement correcte et complète.
- 80-99 : La réponse est correcte avec quelques erreurs mineures ou imprécisions.
- 60-79 : La réponse est partiellement correcte mais manque de précision ou d'exemples clés.
- 40-59 : La réponse contient des éléments corrects mais présente des erreurs importantes.
- 20-39 : La réponse est en grande partie incorrecte mais montre quelques signes de compréhension.
- 1-19 : La réponse est largement hors sujet avec peu d'éléments valides.
- 0 : La réponse est totalement hors sujet ou incompréhensible.
Question :
{self.question}

Réponse correcte attendue :
{self.reponse}

Ma réponse :
{utilisateur_reponse}

RÉPONDS UNIQUEMENT PAR UN ENTIER. TOUT TEXTE SUPPLÉMENTAIRE EST INTERDIT.
NE DONNE AUCUN TEXTE SUPPLÉMENTAIRE, AUCUNE EXPLICATION, AUCUN MOT. SEULEMENT UN ENTIER."""

        data = {
            "model": "llama3.1-8b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            ai_response = response.json()
            try:
                print(ai_response)
                score = int(ai_response['choices'][0]['message']['content'].strip())

                return 1 if min(max(score, 0), 100) >79 else 0
            except (ValueError, KeyError):
                print("Erreur dans la réponse IA, réponse par défaut = 0")
                return 0
        else:
            print(f"Erreur API : {response.status_code}")
            return 0