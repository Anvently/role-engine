# -*-coding:Latin-1 -*
class Portail:
    """Définit un portail. Contient :
    - nom (string)(Nom du portail. ex: Auberge de ville (porte); Portail magique;...)
    - id (string)
    - conditionsUtil (list)(Liste de conditions à remplir pour utiliser le portail.)
    - destination (tuple)(Tuple sous la forme (X,Y) indiquant la destination du portail.)"""

    def __init__(self):
        self.nom = ""
        self.id = ""
        self.conditionsUtil = []
        self.destination = (0,0)


