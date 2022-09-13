# -*-coding:Latin-1 -*
from Reglages import *
from Objet import *
from Creature import *
from Region import *
from Action import *
class Univers:
    """Classe qui définit le contenu d'un univers. Contient :
    - id (string)
    - objets (list)
    - creatures (list)
    - regions (list)
    - actions (list)
    - map (list de list)(Contient une liste de X. Chaque X est une liste de Region.)
    - textes (dict{str:list})(Chaque clé correspond à une description des conditions nécessaires à l'utilisation d'un texte. Chaque valeur contient une liste de textes.)
    - quetes (list)(Liste des quêtes (object) du jeu.)
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


