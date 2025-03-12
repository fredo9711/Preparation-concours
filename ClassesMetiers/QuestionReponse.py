import requests
import json

class Question:
    def __init__(self,id_question: int, question: str, reponse: str):
        self.id_question = id_question
        self.question = question
        self.reponse = reponse

    def verification_reponse(self,utilisateur_reponse:str)-> int:
        api_url = "http://localhost:1337/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        prompt = f"""Je vais te donner une question suivie de la réponse correcte, et enfin une réponse que j’ai moi-même rédigée.
Ta tâche est de me retourner uniquement un entier (entre 0 si j'ai rien compris et 100 si j'ai parfaitement compris) indiquant ma compréhension uniquement par rapport à la question réponse founis si j'ai exactement la même chose ou si j'ai parfaitement compris donne moi la note maximale.

Question :
{self.question}

Réponse correcte attendue :
{self.reponse}

Ma réponse :
{utilisateur_reponse}

repond moi uniquement un entier JE NE VEUX PAS DE TEXTE JUSTE UN ENTIER"""

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