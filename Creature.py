# -*-coding:Latin-1 -*

class Creature:
    """Classe qui d�finit UNE cr�ature. Contient :
    - nom (string)
    - description (string)
    - id (string)(Nom destin� au programme. Sous la forme loup_solitaire_qui_mort.)
    - type(string)(Creature, permet de diff�rencier le joueur d'une cr�ature dans certaines situations.)
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
    - inventaire (list)(Liste d'objets trouvable sur la cr�ature.)
    - niveau (int)(Niveau de la cr�ature.)
    - exp_win (int)(facultatif, exp gagn� par le joueur s'il tue la cr�ature.)
    - effets (list)(Liste de string contenant les effets actifs.)
    - effetsCombat (list)(list de string contenant les effets actifs en combat: empoisonnement, buff, etc...)
    - actions (list)(Liste d'action utilisables.)
    - corruptible (int)(0: non, 1: par l'argent, 2: par la s�duction, 3: par l'argent et la s�duction)  
    - etat (int)(0: mort, 1: en forme, 2: fatigu�, 3: immobilis�, 4: gel�e, 5: inconscient)
    - strategieOffensive (int)(0: l�che - attaque toujours les plus faibles, 1: honorable - attaque toujours les plus forts, 2: cibl�e - attaque toujours un m�me cr�ature choisie au hasard, 3: hasardeuse - attaque les cr�atures au hasard)
    - strategieDefensive (int)(0: sacrifice - la cr�ature n'h�site pas � mourir tant qu'elle inflige le plus de dommage possible, 1: offensive - la cr�ature utilise des sorts de soins d�s qu'il lui reste -20% de sa vie, 2: �quilibr�e - la cr�ature utilise des sorts de soins d�s qu'il lui reste -50% de sa vie, 3: d�fensive - la cr�ature utilise des sorts de soins d�s qu'elle n'a pas toute sa vie, 4: totale - la cr�ature utilise tout le temps des sorts de soins)
    - rompreIncant (bool)(D�finit si oui ou non une cr�ature peut rompre une incantation en cours pour se soigner selon sa strat�gie d�fensive)
    - cible (string)(Contient l'id de la cible que la cr�ature va attaqu�e.)
    - hostil (int)(0: tr�s farouche - s'enfuit � vue du joueur, 1: farouche - s'enfuit � vue de combat, 2: peureux - s'enfuit en combat, 3: passif - n'attaque jamais et ne fuie pas, 4: neutre - attaque de repr�saille, 5: d�fenseur - attaque � vue de combat, 6: hostil - attaque le joueur � vue, 7: agressif - attaque tout le monde � vue)
    - amisAvec (list)(Liste d'id des cr�atures que cette cr�ature est susceptible de d�fendre si son hostilit� est � 5. Les cr�atures amis entre elles ne s'attaquent pas.)
    - dialogue (dialogue)(D�finit le dialogue entre la cr�ature et le personnage. Vide par d�faut.)
    - malusFuite (int)(Score enlev� au jet de fuite du personnage. 0 pour aucun et 20 pour une fuite impossible.)
    - enCombatAvec (list)(Liste d'id des  cr�atures avec lesquelles est en combat la cr�ature. Temporaire.)
    - tIncantRestant (int)(Nombre de tours restants d'incantation d'un sort. Temporaire.)
    - sortIncant (Action)(Contient l'action que le joueur est entrain d'invoquer. Temporaire.)"""
   

    def __init__(self):
        self.nom = ''
        self.description = ''
        self.id = ''
        self.type = 'creature'
        self.motsCles = []
        self.caracteristiques = CaractCreature()
        self.caracteristiques.update({'force' : 0, 'adresse' : 0, 'charisme' : 0, 'courage' : 0, 'intelligence' : 0, 'attaque' : 0, 'vitesse' : 0.0, 'pvBase' : 0, 'pv' : 0})
        self.inventaire = []
        self.niveau = 1
        self.exp_win = 0
        self.effets = []
        self.effetsCombat = []
        self.actions = []
        self.corruptible = 0
        self.etat = 1
        self.strategieOffensive = 0
        self.strategieDefensive = 0
        self.rompreIncant = True
        self.cible = ''
        self.hostil = 4
        self.amisAvec = []
        self.dialogue = None
        self.malusFuite = 0
        self.enCombatAvec = []
        self.tIncantRestant = 0
        self.sortIncant = ''

class CaractCreature(dict):
    def __setitem__(self, key, item): 
        """if key == 'pv' and (self.__dict__[key] - item) != 0: 
            print(self.nom+' a perdu '+str(self.__dict__[key] - item)+' points de vie.')"""
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

    def setParent(self, parent):
        self.parent = parent
        self.nom = self.parent.nom

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