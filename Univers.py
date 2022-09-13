# -*-coding:Latin-1 -*
from Reglages import *
from Objet import *
from Creature import *
from Region import *
from Action import *
class Univers:
    """Classe qui d�finit le contenu d'un univers. Contient :
    - id (string)
    - objets (list)
    - creatures (list)
    - regions (list)
    - actions (list)
    - map (list de list)(Contient une liste de X. Chaque X est une liste de Region.)
    - textes (dict{str:list})(Chaque cl� correspond � une description des conditions n�cessaires � l'utilisation d'un texte. Chaque valeur contient une liste de textes.)
    - quetes (list)(Liste des qu�tes (object) du jeu.)
    - reglages (reglages)
    ..."""

    def __init__(self):
        self.id = ""
        self.objets = [Objet()]
        self.creatures = [Creature()]
        self.regions = [Region()]
        self.actions = [Action()]
        self.map = [[]]
        self.textes = {}
        self.quetes = []
        self.reglages = Reglages()


