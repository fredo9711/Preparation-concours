from datetime import datetime,timedelta
from scipy.optimize import fsolve

class CourbeOubli:
    def __init__(self):pass


    def comparer_dates(self,date_revision: datetime) -> bool:
        return datetime.now() >= date_revision
    

    def calculer_prochaine_revision(self,courbe_actuelle:int,resultatSession:bool)->tuple:
        prochaine_revision=datetime.now()

        if courbe_actuelle ==0 and resultatSession:
            return 1,prochaine_revision+timedelta(days=1)
        elif courbe_actuelle ==0:return 0,prochaine_revision
        
        if courbe_actuelle ==90 and resultatSession:
            return 90,prochaine_revision+timedelta(days=90)
        elif courbe_actuelle==90 :return 0,prochaine_revision


        nouvelle_courbe =round(fsolve(lambda n:0.0417*n**4 + 2.4167*n**3 - 14.5417*n**2 + 28.0833*n - 15 - courbe_actuelle,x0=1)[0])
        if resultatSession:
            nouvelle_courbe+=1
        else:  return 0,prochaine_revision

        nouvelle_courbe = round(0.0417*nouvelle_courbe**4 + 2.4167*nouvelle_courbe**3 - 14.5417*nouvelle_courbe**2 + 28.0833*nouvelle_courbe-15)
        return nouvelle_courbe,prochaine_revision+timedelta(days=nouvelle_courbe)



