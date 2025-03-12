import unittest
from unittest.mock import patch
import unittest.mock
from QuestionReponse import Question

class TestQuestion(unittest.TestCase):

    def setUp(self):
            self.question = Question(
            id_question=1,
            question="Définis Machine learning.",
            reponse="Un système qui apprend par expérience."
        )
            

    def test_verification_reponse_correcte(self): # direct un test d'integration
        for i in range(10):
            resultat = self.question.verification_reponse("Un système qui apprend grâce à l'expérience.")
            #resultat = self.question.verification_reponse("Tom Mitchell,1997, Un programme capable de réaliser une tache (T) en fonction de l'expérience acquise (E) selon l'unité de mesure testant la qualité de sa tache (P)")
            self.assertEqual(resultat,1)

  
    def test_verification_reponse_incorrecte(self):
        for i in range(10):
            resultat = self.question.verification_reponse("Paris")
            self.assertEqual(resultat, 0)
          

if __name__ =='__main__':
      unittest.main()