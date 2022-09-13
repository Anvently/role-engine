# -*-coding:Latin-1 -*
class Objet:
    """Classe qui définit un objet. Contient:
    - nom (string)
    - description (string)
    - id (string)(Nom de l'objet destiné au jeu. N'apparait pas en dehors des codes et est sous la forme: epee_de_l_egolas_en_cuivre)
    - motsCles (list de string)(Liste de mots clés commencant par # définissant la créature. Ex: cuir;dague;bois;plastron;armureLourde)
    - poids (float)
    - prix (float)(prix de base, le prix final dépend d'autres critères)
    - fonction (int)(0: Non équipable et non utilisable (ex: tableau) - 1: Equipable mais non utilisable (ex: armure) - 2: Non équipable mais utilisable (ex: potion))
    - nbrUse (int)(Nombre de fois utilisable. Diminue à chaque utilisation, l'objet se détruit une fois qu'il ne peut plus être utilisé. Uniquement pour les objets de fonction 2 (potions))
    - effetsPoss (liste de string)(Effets activés lorsque l'objet est possédé)
    - effetsEquip (list de string)(Effets activés lorsque l'objet est équipé. Uniquement pour les objets de fonction 1(armures/armes))
    - effetsUtil (list de string)(Effets activés lorsque l'objet est utilisé. Uniquement pour les objets de fonction 2(potions,consommables))
    - conditionsPoss (list de string)(Conditions pour prendre l'objet dans l'inventaire.)
    - conditionsEquip (list de string)(Conditions pour équiper l'objet. Uniquement pour les objets de fonction 1(armures/armes))
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

