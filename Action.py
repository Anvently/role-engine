# -*-coding:Latin-1 -*
class Action:
    """D�finit une action. Peut-�tre une attaque, un boost, un sort, etc... Contient:
    - nom (string)
    - description (string)
    - id (string)(Nom de l'action destin� au jeu. N'apparait pas en dehors des codes et est sous la forme: coup_d_epee_de_l_egolas_en_cuivre)
    - motsCles (list)(Liste de mots cl�s commencant par # d�finissant l'action.)
    - type (int)(0: attaque, 1: soin, 2: buff)
    - cible (int)(0: Lanceur - 1: Autre)
    - util (int)(0: Nimporte quand - 1: En dehors d'un combat - 2: En combat)
    - conditions (list de string)(Conditions pour lancer l'action)
    - effets (list de string)(Effets de l'action)
    - tIncant (int)(Correspond au nombre d'assaut n�cessaire pour que les effets soient actifs)
    - etatIncant (int)(Correspond � l'�tat dans lequel est le personnage pendant l'incantation. Un nombre n�gatif n'effectuera aucun changement.)
    - ratable (bool)(D�finit si l'action est ratable ou non.)
    - esquive (bool)(Autorise ou non la cible � faire un jet d'esquive pour ne pas subir les effets de l'action)"""

    def __init__(self):
        self.nom = ""
        self.description = ""
        self.id = ""
        self.motsCles = []
        self.type = 0
        self.cible = 0
        self.util = 0
        self.conditions = []
        self.effets = []
        self.tIncant = 0
        self.etatIncant = -1
        self.ratable = True
        self.esquive = False


