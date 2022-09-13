# -*-coding:Latin-1 -*
class Region:
    """Classe qui définit une région type. Contient :
    - nom (string)(Si aucun nom n'est défini pour une région, elle prendra le nom de sa région type.)
    - description (string)(Si aucun nom n'est défini pour une région, elle prendra le nom de sa région type.)
    - id (string)(Nom destiné au programme. Sous la forme : steppes_de_l_etoile_sacree.)
    - regionParent (string)(Id de la région parente de cette région. Si elle n'en a pas, alors il est égal à l'id de la région.)
    - motsCles (list)(Liste de mots clés commencant par # définissant la région.)
    - facteurDep (int)(Multiplie la vitesse du personnage par le facteur.)
    - creaturesRencontrables (list)(Liste de créatures rencontrables dans la région.)
    - conditionEntrer (list)(Liste de conditions pour entrer dans la région.)
    - conditionSortir (list)(Liste de conditions pour sortir de la région.)
    - effets (list)(Liste d'effets s'activant lorsque le joueur entre dans la région. Ils se suppriment lorsqu'il en sort.)
    - objets ([[Objet,[etat,jet]]])(Liste de listes contenant un objet se trouvant dans la région et une liste contenant (dans l'ordre) l'état de l'objet puis le jet à réaliser pour le trouver. Etats -> 0: non découvert(nécessite une fouille pour être trouvé) | 1: temporaire(disparait une fois que le joueur sort de la région) | 2: découvert(visible à l'entrée de la région))
    - creatures ([[Creature,[etat,jet]]])(Liste de listes contenant une créature se trouvant dans la région et une liste contenant (dans l'ordre) l'état de la créature puis le jet à réaliser pour la trouver. Etats -> 0: non découverte(nécessite une fouille pour être trouvée) | 1 : découverte(visible à l'entrée de la région) | 2 : morte(cadavre))
    - portails ([[Portail,[etat,jet]]])(Liste de listes contenant un portail se trouvant dans la région et une liste contenant (dans l'ordre) l'état du portail puis le jet à réaliser pour le trouver. Etats -> 0: non découvert(nécessite une fouille pour être trouvé) | 1 : découvert(visible à l'entrée de la région))
    - directionUtil (string)(Nombre à 8 chiffres correspondant au direction dans lequels peut se déplacer le personnage depuis cette région. 0 indique l'interdiction et 1 l'autorisation. 
        Les chiffres (0 ou 1) correspondant aux directions suivent l'ordre suivant: Nord ; Nord-Est ; Est ; Sud-Est ; Sud ; Sud-Ouest ; Ouest ; Nord-Ouest.)"""

    def __init__(self):
        self.nom = ""
        self.description = ""
        self.id = ""
        self.regionParent = self.id
        self.motsCles = []
        self.facteurDep = 1.0
        self.creaturesRencontrables= []
        self.conditionsEntrer = []
        self.conditionsSortir = []
        self.effets = []
        self.objets = []
        self.creatures = []
        self.portails = []
        self.directionUtil = '11111111'