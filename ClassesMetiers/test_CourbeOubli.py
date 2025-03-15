import unittest
from datetime import datetime, timedelta
from CourbeOubli import CourbeOubli

class TestCourbeOubli(unittest.TestCase):

    def setUp(self):
        self.courbe = CourbeOubli()

    # ------------------------------------------------------
    # 1) Test de la méthode comparer_dates(date_revision)
    # ------------------------------------------------------
    def test_comparer_dates_passee(self):
        # Date passée -> doit retourner True
        date_passee = datetime.now() - timedelta(days=1)
        self.assertTrue(self.courbe.comparer_dates(date_passee))

    def test_comparer_dates_future(self):
        # Date future -> doit retourner False
        date_future = datetime.now() + timedelta(days=2)
        self.assertFalse(self.courbe.comparer_dates(date_future))

    # ------------------------------------------------------
    # 2) Test de la méthode calculer_prochaine_revision(courbe_actuelle, resultatSession)
    # ------------------------------------------------------

    # ---- 2.1) cas courbe_actuelle = 0
    def test_calc_prochaine_revision_courbe0_reussie(self):
        courbe_actuelle = 0
        resultatSession = True
        nouvelle_courbe, date_prochaine = self.courbe.calculer_prochaine_revision(courbe_actuelle, resultatSession)

        # Étant donné l'implémentation, courbe passe à 1, date +1 jour
        self.assertEqual(nouvelle_courbe, 1)
        delta = date_prochaine - datetime.now()
        # Le delta devrait être environ 1 jour
        self.assertTrue(0.9 < delta.total_seconds() / 86400 < 1.1)

    def test_calc_prochaine_revision_courbe0_echec(self):
        courbe_actuelle = 0
        resultatSession = False
        nouvelle_courbe, date_prochaine = self.courbe.calculer_prochaine_revision(courbe_actuelle, resultatSession)

        # Reste à 0, date révision = maintenant
        self.assertEqual(nouvelle_courbe, 0)
        # date_prochaine doit être environ la même qu'actuellement
        self.assertTrue(abs((date_prochaine - datetime.now()).total_seconds()) < 2)

    # ---- 2.2) cas courbe_actuelle = 90
    def test_calc_prochaine_revision_courbe90_reussie(self):
        courbe_actuelle = 90
        resultatSession = True
        nouvelle_courbe, date_prochaine = self.courbe.calculer_prochaine_revision(courbe_actuelle, resultatSession)

        # Reste à 90, date +90 jours
        self.assertEqual(nouvelle_courbe, 90)
        delta = date_prochaine - datetime.now()
        self.assertTrue(89.9 < delta.total_seconds() / 86400 < 90.1)

    def test_calc_prochaine_revision_courbe90_echec(self):
        courbe_actuelle = 90
        resultatSession = False
        nouvelle_courbe, date_prochaine = self.courbe.calculer_prochaine_revision(courbe_actuelle, resultatSession)

        # Retombe à 0, date = now
        self.assertEqual(nouvelle_courbe, 0)
        # date_prochaine doit être environ la même qu'actuellement
        self.assertTrue(abs((date_prochaine - datetime.now()).total_seconds()) < 2)

    # ---- 2.3) cas intermédiaires
    def test_calc_prochaine_revision_courbe_intermediaire_reussie(self):
        """
        On teste par exemple courbe_actuelle=7 et on s'attend à ce que le polynôme
        renvoie un certain nouveau stade. On vérifie que tout se passe sans erreur.
        """
        courbe_actuelle = 7
        resultatSession = True
        nouvelle_courbe, date_prochaine = self.courbe.calculer_prochaine_revision(courbe_actuelle, resultatSession)

        # On ne sait pas forcément quel sera le nouveau résultat exact sans analyser le polynôme,
        # mais on s'assure que la date_prochaine > now de (nouvelle_courbe) jours
        self.assertIsInstance(nouvelle_courbe, int)
        self.assertTrue(nouvelle_courbe >= 0)

        delta = (date_prochaine - datetime.now()).total_seconds()
        # On s'assure juste que c'est dans le futur (>=0)
        self.assertTrue(delta > -2)

    def test_calc_prochaine_revision_courbe_intermediaire_echec(self):
        """
        On teste par exemple courbe_actuelle=7 + échec.
        On s'attend à retomber à 0 et date_prochaine = now.
        """
        courbe_actuelle = 7
        resultatSession = False
        nouvelle_courbe, date_prochaine = self.courbe.calculer_prochaine_revision(courbe_actuelle, resultatSession)

        self.assertEqual(nouvelle_courbe, 0)
        # Vérification date proche de now
        self.assertTrue(abs((date_prochaine - datetime.now()).total_seconds()) < 2)

if __name__ == '__main__':
    unittest.main()
