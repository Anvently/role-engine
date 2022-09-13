# -*-coding:Latin-1 -*
class Quete:
    """Classe qui définit une quête. Contient :
    - nom (string)
    - id (string)
    - description (string)
    - objectifs (list)(Liste des objectifs à réaliser)
    - objectifsAchevement (list)(Liste correspondant aux ids des objectifs à terminer pour que la quête soit achevée)
    - conditionsLancement (list)(Liste de conditions pour que la quête puisse être acceptée)
    - conditionsAchevement (list)(Liste de conditions pour que la quête puisse être achevée)
    - effetsSucces (list)(Liste d'effets activés lorsque la quête est achevée)
    - effetsEchec (list)(Liste d'effets activés lorsque la quête est un echec)
    - tempsRestant (int)(Nombre d'heures restantes. La quête est un échec lorsque le temps restants est à 0)"""

    def __init__(self):
        self.nom = ''
        self.id = ''
        self.description = ''
        self.objectifs = []
        self.objectifsAchevement = []
        self.conditionsLancement = []
        self.conditionsAchevement = []
        self.effetsSucces = []
        self.effetsEchec = []
        self.tempsRestant = 0
    


class Objectif:
    """Classe qui définit un objectif d'une quête. Contient :
    - id (string)
    - description (string)
    - etat (int)(0: non démarré - 1: en cours - 2: terminé)
    - conditionsLancement (list)(Liste de conditions pour que l'objectif puisse être lancé)
    - conditionsAchevement (list)(Liste de conditions pour que l'objectif puisse être achevé)
    - objectif (string)(Définit l'action qui doit être accomplie pour que l'objectif soit validé)
    - compteur (int)(Compte le nombre de fois qu'une créature a été tuée ou qu'un objet a été ramassé. L'objet et la créature doivent bien sur être ceux correspondant à l'objectif.)
    - done (bool)(Définit si l'objectif a été atteint ou non. Il faut ensuite que les conditions d'achèvement soit remplies pour que l'objectif soit achevé.)
    - ordreAchevement (list)(Liste de string correspondant aux ids des objectifs qui doivent être terminés pour que l'objectif concerné puisse être achevé)
    - ordreLancement (list)(Liste de string correspondant aux ids des objectifs qui doivent être terminés pour que l'objectif concerné puisse être lancé)"""

    def __init__(self,id='',description="", etat=0,conditionsLancement=[],conditionsAchevement=[],objectif='',compteur=0,done=False,ordreAchevement=[],ordreLancement=[]):
        self.id = id
        self.description = description
        self.etat = etat
        self.conditionsLancement = conditionsLancement
        self.conditionsAchevement = conditionsAchevement
        self.objectif = objectif
        self.compteur = compteur
        self.done = done
        self.ordreAchevement = ordreAchevement
        self.ordreLancement = ordreLancement