# -*-coding:Latin-1 -*
from math import *
class Personnage:
    """Classe qui définit les informations sur un personnage. Contient :
    - nom (string)
    - id (string)(Nom destiné au programme. Sous la forme loup_solitaire_qui_mort.)
    - type(string)(Joueur, permet de différencier le joueur d'une créature dans certaines situations.)
    - motsCles (list)(Liste de mots clés commencant par # définissant la créature.)
    - caracteristiques (dict)[Gère les caractéristiques d'un personnage, d'une créature. Contient:
                            - force (int)(1 à 20)
                            - adresse (int)(1 à 20)
                            - charisme (int)(1 à 20)
                            - courage (int)(1 à 20)
                            - intelligence (int)(1 à 20)
                            - attaque (int)(1 à 20)
                            - vitesse (float)(en km/h)
                            - pvBase (int)(nombre de points de vie total)
                            - pv (int)(nombre de points de vie)]
                            - poidsPortable (float)(Définit le poids maximum portable par le personnage.)
                            - poidsPortes (float)(Définit le poids porté par le personnage.)
    - niveau (int)
    - exp (int)
    - positionX (int)
    - positionY (int)
    - etat (int)(0: mort, 1: en forme, 2: fatigué, 3: immobilisé, 4: gelée, 5: inconscient)
    - fatigue (float)(Score de fatigue variant de 0 à 100. Le personnage est épuisé et s'évanouit lorsque le score atteint 100. Diminue avec l'inactivité ou le repos.)
    - effets (list)(Liste de string contenant les effets actifs.)
    - effetsCombat (list)(list de string contenant les effets actifs en combat: empoisonnement, buff, etc...)
    - emplacements (dict)(Dictionnaire dont la longueur correspond au nombre d'emplacements utilisables. Une clé correspond à un emplacement et sa valeur à l'objet qui l'occupe.)
    - inventaire (dict)(Dictionnaire ayant pour clé un objet possédé et pour valeur la quantité dans laquelle l'objet est possédé.)
    - actions (list)(Liste de string. Chaque string correspond à l'id d'une action utilisable.)
    - tIncantRestant (int)(Nombre de tours restants d'incantation d'un sort. Temporaire.)
    - sortIncant (Action)(Contient l'action que le joueur est entrain d'invoquer. Temporaire.)
    - interdictions (list)(Liste de string.)
    - hostilites (list)(Liste d'ids des créatures hostiles envers le joueur. Lorsqu'une créature dans cette liste rencontre le joueur, son niveau d'hosilité est à 6 (hostil).)
    - malusFuite (int)(Score enlevé au jet de fuite des créatures. 0 pour aucun et 20 pour une fuite impossible.)
    - enCombatAvec (list)(Liste des créatures avec lesquelles le joueur est en combat.)
    - quetesActives (list)(Liste de quêtes actives.)
    - quetesAchevees (list)(Liste string correspondant aux ids des quêtes que le joueur a achevé.)
    - heure (date)(Contient un objet date qui représente la date et l'heure du jeu. En heures.)
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
        '''Modifie la fatigue d'un personnage en gérant l'évanouissement.'''
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