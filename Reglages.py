# -*-coding:Latin-1 -*
class Reglages:
    """Classe qui contient les différents réglages du jeu. Contient:
    - modeCalculMalusDeplacement (string)(Avec la valeur "absolu", les malus de déplacements seront fixes et indépendants de la vitesse du personnage. Avec la valeur "relatif", les malus correspondront à un % de la vitesse totale.
    - rencontresParNiveau (bool)(Définit si le joueur peut rencontrer uniquement des créatures de niveaux égal ou inférieur. Si False, il pourra rencontrer des créatures de niveaux supérieurs au sien.)
    - autoriserEsquive (bool)(Définit si le jeu autorise l'esquive ou non.)
    - caractEsquive (string)(Nom du caractéristique avec lequel les jets d'esquive sont faits.)
    - caractFouille (string)(Nom du caractéristique avec lequel les jets de fouille sont faits.)
    - caractNegociation1 (string)(Premier caractéristique avec lequel les jets de négociation sont faits.)
    - caractNegociation2 (string)(Deuxième caractéristique avec lequel les jets de négociation sont faits.)
    - caractFuite (string)(Nom du caractéristique avec lequel les jets de fuite sont faits.)
    - caractInitiative (string)(Nom du caractéristique qui intervient dans la répartition de l'ordre d'un tour de combat.)
    - maxCaract (int)(Définit le maximum des caractéristiques, hors pv, pvBase, vitesse, poidsPortes, poidsPortable.)
    - frequenceRencontre (int)(Le joueur rencontrera un monstre à peu près toutes les x heures de voyage.)
	- caracts (list)(Liste des caractéristiques possibles.)
    """

    def __init__(self):
        self.modeCalculMalusDeplacement = "relatif"
        self.rencontresParNiveau = True
        self.autoriserEsquive = True
        self.caractEsquive = 'adresse'
        self.caractFouille = 'intelligence'
        self.caractNegociation1 = 'intelligence'
        self.caractNegociation2 = 'charisme'
        self.caractFuite = 'adresse'
        self.caractInitiative = 'courage'
        self.caractAttaque = 'attaque'
        self.caractSoin = 'attaque'
        self.maxCaract = 20
        self.frequenceRencontre = 6.0
        self.caracts = []
