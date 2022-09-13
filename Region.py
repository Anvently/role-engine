# -*-coding:Latin-1 -*
class Region:
    """Classe qui d�finit une r�gion type. Contient :
    - nom (string)(Si aucun nom n'est d�fini pour une r�gion, elle prendra le nom de sa r�gion type.)
    - description (string)(Si aucun nom n'est d�fini pour une r�gion, elle prendra le nom de sa r�gion type.)
    - id (string)(Nom destin� au programme. Sous la forme : steppes_de_l_etoile_sacree.)
    - regionParent (string)(Id de la r�gion parente de cette r�gion. Si elle n'en a pas, alors il est �gal � l'id de la r�gion.)
    - motsCles (list)(Liste de mots cl�s commencant par # d�finissant la r�gion.)
    - facteurDep (int)(Multiplie la vitesse du personnage par le facteur.)
    - creaturesRencontrables (list)(Liste de cr�atures rencontrables dans la r�gion.)
    - conditionEntrer (list)(Liste de conditions pour entrer dans la r�gion.)
    - conditionSortir (list)(Liste de conditions pour sortir de la r�gion.)
    - effets (list)(Liste d'effets s'activant lorsque le joueur entre dans la r�gion. Ils se suppriment lorsqu'il en sort.)
    - objets ([[Objet,[etat,jet]]])(Liste de listes contenant un objet se trouvant dans la r�gion et une liste contenant (dans l'ordre) l'�tat de l'objet puis le jet � r�aliser pour le trouver. Etats -> 0: non d�couvert(n�cessite une fouille pour �tre trouv�) | 1: temporaire(disparait une fois que le joueur sort de la r�gion) | 2: d�couvert(visible � l'entr�e de la r�gion))
    - creatures ([[Creature,[etat,jet]]])(Liste de listes contenant une cr�ature se trouvant dans la r�gion et une liste contenant (dans l'ordre) l'�tat de la cr�ature puis le jet � r�aliser pour la trouver. Etats -> 0: non d�couverte(n�cessite une fouille pour �tre trouv�e) | 1 : d�couverte(visible � l'entr�e de la r�gion) | 2 : morte(cadavre))
    - portails ([[Portail,[etat,jet]]])(Liste de listes contenant un portail se trouvant dans la r�gion et une liste contenant (dans l'ordre) l'�tat du portail puis le jet � r�aliser pour le trouver. Etats -> 0: non d�couvert(n�cessite une fouille pour �tre trouv�) | 1 : d�couvert(visible � l'entr�e de la r�gion))
    - directionUtil (string)(Nombre � 8 chiffres correspondant au direction dans lequels peut se d�placer le personnage depuis cette r�gion. 0 indique l'interdiction et 1 l'autorisation. 
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