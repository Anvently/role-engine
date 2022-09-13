# -*-coding:Latin-1 -*
class Reglages:
    """Classe qui contient les diff�rents r�glages du jeu. Contient:
    - modeCalculMalusDeplacement (string)(Avec la valeur "absolu", les malus de d�placements seront fixes et ind�pendants de la vitesse du personnage. Avec la valeur "relatif", les malus correspondront � un % de la vitesse totale.
    - rencontresParNiveau (bool)(D�finit si le joueur peut rencontrer uniquement des cr�atures de niveaux �gal ou inf�rieur. Si False, il pourra rencontrer des cr�atures de niveaux sup�rieurs au sien.)
    - autoriserEsquive (bool)(D�finit si le jeu autorise l'esquive ou non.)
    - caractEsquive (string)(Nom du caract�ristique avec lequel les jets d'esquive sont faits.)
    - caractFouille (string)(Nom du caract�ristique avec lequel les jets de fouille sont faits.)
    - caractNegociation1 (string)(Premier caract�ristique avec lequel les jets de n�gociation sont faits.)
    - caractNegociation2 (string)(Deuxi�me caract�ristique avec lequel les jets de n�gociation sont faits.)
    - caractFuite (string)(Nom du caract�ristique avec lequel les jets de fuite sont faits.)
    - caractInitiative (string)(Nom du caract�ristique qui intervient dans la r�partition de l'ordre d'un tour de combat.)
    - maxCaract (int)(D�finit le maximum des caract�ristiques, hors pv, pvBase, vitesse, poidsPortes, poidsPortable.)
    - frequenceRencontre (int)(Le joueur rencontrera un monstre � peu pr�s toutes les x heures de voyage.)
	- caracts (list)(Liste des caract�ristiques possibles.)
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
