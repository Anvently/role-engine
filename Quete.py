# -*-coding:Latin-1 -*
class Quete:
    """Classe qui d�finit une qu�te. Contient :
    - nom (string)
    - id (string)
    - description (string)
    - objectifs (list)(Liste des objectifs � r�aliser)
    - objectifsAchevement (list)(Liste correspondant aux ids des objectifs � terminer pour que la qu�te soit achev�e)
    - conditionsLancement (list)(Liste de conditions pour que la qu�te puisse �tre accept�e)
    - conditionsAchevement (list)(Liste de conditions pour que la qu�te puisse �tre achev�e)
    - effetsSucces (list)(Liste d'effets activ�s lorsque la qu�te est achev�e)
    - effetsEchec (list)(Liste d'effets activ�s lorsque la qu�te est un echec)
    - tempsRestant (int)(Nombre d'heures restantes. La qu�te est un �chec lorsque le temps restants est � 0)"""

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
    """Classe qui d�finit un objectif d'une qu�te. Contient :
    - id (string)
    - description (string)
    - etat (int)(0: non d�marr� - 1: en cours - 2: termin�)
    - conditionsLancement (list)(Liste de conditions pour que l'objectif puisse �tre lanc�)
    - conditionsAchevement (list)(Liste de conditions pour que l'objectif puisse �tre achev�)
    - objectif (string)(D�finit l'action qui doit �tre accomplie pour que l'objectif soit valid�)
    - compteur (int)(Compte le nombre de fois qu'une cr�ature a �t� tu�e ou qu'un objet a �t� ramass�. L'objet et la cr�ature doivent bien sur �tre ceux correspondant � l'objectif.)
    - done (bool)(D�finit si l'objectif a �t� atteint ou non. Il faut ensuite que les conditions d'ach�vement soit remplies pour que l'objectif soit achev�.)
    - ordreAchevement (list)(Liste de string correspondant aux ids des objectifs qui doivent �tre termin�s pour que l'objectif concern� puisse �tre achev�)
    - ordreLancement (list)(Liste de string correspondant aux ids des objectifs qui doivent �tre termin�s pour que l'objectif concern� puisse �tre lanc�)"""

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