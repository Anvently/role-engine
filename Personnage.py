# -*-coding:Latin-1 -*
from math import *
class Personnage:
    """Classe qui d�finit les informations sur un personnage. Contient :
    - nom (string)
    - id (string)(Nom destin� au programme. Sous la forme loup_solitaire_qui_mort.)
    - type(string)(Joueur, permet de diff�rencier le joueur d'une cr�ature dans certaines situations.)
    - motsCles (list)(Liste de mots cl�s commencant par # d�finissant la cr�ature.)
    - caracteristiques (dict)[G�re les caract�ristiques d'un personnage, d'une cr�ature. Contient:
                            - force (int)(1 � 20)
                            - adresse (int)(1 � 20)
                            - charisme (int)(1 � 20)
                            - courage (int)(1 � 20)
                            - intelligence (int)(1 � 20)
                            - attaque (int)(1 � 20)
                            - vitesse (float)(en km/h)
                            - pvBase (int)(nombre de points de vie total)
                            - pv (int)(nombre de points de vie)]
                            - poidsPortable (float)(D�finit le poids maximum portable par le personnage.)
                            - poidsPortes (float)(D�finit le poids port� par le personnage.)
    - niveau (int)
    - exp (int)
    - positionX (int)
    - positionY (int)
    - etat (int)(0: mort, 1: en forme, 2: fatigu�, 3: immobilis�, 4: gel�e, 5: inconscient)
    - fatigue (float)(Score de fatigue variant de 0 � 100. Le personnage est �puis� et s'�vanouit lorsque le score atteint 100. Diminue avec l'inactivit� ou le repos.)
    - effets (list)(Liste de string contenant les effets actifs.)
    - effetsCombat (list)(list de string contenant les effets actifs en combat: empoisonnement, buff, etc...)
    - emplacements (dict)(Dictionnaire dont la longueur correspond au nombre d'emplacements utilisables. Une cl� correspond � un emplacement et sa valeur � l'objet qui l'occupe.)
    - inventaire (dict)(Dictionnaire ayant pour cl� un objet poss�d� et pour valeur la quantit� dans laquelle l'objet est poss�d�.)
    - actions (list)(Liste de string. Chaque string correspond � l'id d'une action utilisable.)
    - tIncantRestant (int)(Nombre de tours restants d'incantation d'un sort. Temporaire.)
    - sortIncant (Action)(Contient l'action que le joueur est entrain d'invoquer. Temporaire.)
    - interdictions (list)(Liste de string.)
    - hostilites (list)(Liste d'ids des cr�atures hostiles envers le joueur. Lorsqu'une cr�ature dans cette liste rencontre le joueur, son niveau d'hosilit� est � 6 (hostil).)
    - malusFuite (int)(Score enlev� au jet de fuite des cr�atures. 0 pour aucun et 20 pour une fuite impossible.)
    - enCombatAvec (list)(Liste des cr�atures avec lesquelles le joueur est en combat.)
    - quetesActives (list)(Liste de qu�tes actives.)
    - quetesAchevees (list)(Liste string correspondant aux ids des qu�tes que le joueur a achev�.)
    - heure (date)(Contient un objet date qui repr�sente la date et l'heure du jeu. En heures.)
    - mapUnivers (list de list)(Contient une liste de X. Chaque X est une liste de Region.)"""

    def __init__(self):
        self.nom = ""
        self.id = ""
        self.type = "joueur"
        self.motsCles = []
        self.caracteristiques = CaractPersonnage()
        self.caracteristiques.update({'force' : 0, 'adresse' : 0, 'charisme' : 0, 'courage' : 0, 'intelligence': 0, 'attaque' : 0, 'vitesse' : 0.0, 'pvBase' : 0, 'pv' : 0, 'poidsPortable' : 0.0, 'poidsPortes' : 0.0})
        self.niveau = 1
        self.exp = 0
        self.positionX = 0
        self.positionY = 0
        self.etat = 1
        self._fatigue = 0.0
        self.effets = []
        self.effetsCombat = []
        self.emplacements = {}
        self.inventaire = {}
        self.actions = []
        self.tIncantRestant = 0
        self.sortIncant = ''
        self.interdictions = []
        self.hostilites = []
        self.malusFuite = 0
        self.enCombatAvec = []
        self.quetesActives = []
        self.quetesAchevees = []
        self.heure = 0
        self.mapUnivers = []
    def get_fatigue(self):
        return self._fatigue
    def set_fatigue(self, bonus):
        '''Modifie la fatigue d'un personnage en g�rant l'�vanouissement.'''
        self._fatigue = bonus

    fatigue = property(get_fatigue,set_fatigue)


class CaractPersonnage(dict):
    def __setitem__(self, key, item): 
        #if key == 'pv': print('Vous perdez : '+str(self.__dict__[key] - item)+' points de vie.')
        self.__dict__[key] = item

    def __getitem__(self, key): 
        return self.__dict__[key]

    def __repr__(self): 
        return repr(self.__dict__)

    def __len__(self): 
        return len(self.__dict__)

    def __delitem__(self, key): 
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return self.__dict__.has_key(k)

    def pop(self, k, d=None):
        return self.__dict__.pop(k, d)

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict):
        return cmp(self.__dict__, dict)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))