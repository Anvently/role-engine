# -*-coding:Latin-1 -*
class Objet:
    """Classe qui d�finit un objet. Contient:
    - nom (string)
    - description (string)
    - id (string)(Nom de l'objet destin� au jeu. N'apparait pas en dehors des codes et est sous la forme: epee_de_l_egolas_en_cuivre)
    - motsCles (list de string)(Liste de mots cl�s commencant par # d�finissant la cr�ature. Ex: cuir;dague;bois;plastron;armureLourde)
    - poids (float)
    - prix (float)(prix de base, le prix final d�pend d'autres crit�res)
    - fonction (int)(0: Non �quipable et non utilisable (ex: tableau) - 1: Equipable mais non utilisable (ex: armure) - 2: Non �quipable mais utilisable (ex: potion))
    - nbrUse (int)(Nombre de fois utilisable. Diminue � chaque utilisation, l'objet se d�truit une fois qu'il ne peut plus �tre utilis�. Uniquement pour les objets de fonction 2 (potions))
    - effetsPoss (liste de string)(Effets activ�s lorsque l'objet est poss�d�)
    - effetsEquip (list de string)(Effets activ�s lorsque l'objet est �quip�. Uniquement pour les objets de fonction 1(armures/armes))
    - effetsUtil (list de string)(Effets activ�s lorsque l'objet est utilis�. Uniquement pour les objets de fonction 2(potions,consommables))
    - conditionsPoss (list de string)(Conditions pour prendre l'objet dans l'inventaire.)
    - conditionsEquip (list de string)(Conditions pour �quiper l'objet. Uniquement pour les objets de fonction 1(armures/armes))
    - conditionsUtil (list de string)(Conditions pour utiliser l'objet. Uniquement pour les objets de fonction 2(potions,consommables))
    - empEquip (list string)(Correspond aux des id des emplacement que peut occcuper l'objet. Uniquement pour les objets de fonction 1(armures/armes))"""

    def __init__(self):
        self.nom = ""
        self.description = ""
        self.id = ""
        self.motsCles = []
        self.poids = 0.0
        self.prix = 0.0
        self.fonction = 0
        self.nbrUse = 0
        self.effetsPoss = []
        self.effetsEquip = []
        self.effetsUtil = []
        self.conditionsPoss = []
        self.conditionsEquip = []
        self.conditionsUtil = []
        self.empEquip = []

