# -*-coding:Latin-1 -*
from Univers import *
from Objet import *
from Action import *
from Jeu import *
from Region import *
from random import *
from Creature import *
from math import *
import copy
import re
from Quete import *
from Dialogue import *
import time

univers = Univers()
personnage = Personnage()

"""creatoure = Creature()
creatoure.caracteristiques.update({'courage' : 7, 'adresse' : 13, 'attaque' : 9, 'pvBase' : 15, 'pv' : 15})
creatoure.nom = 'mabite'
creatoure.caracteristiques.setParent(creatoure)
creatoure.caracteristiques['attaque'] = 11
print(creatoure.caracteristiques['attaque'])"""

'''perso = Personnage()

perso.caracteristiques['Force']=25
perso.caracteristiques.update({'force' : 10, 'adresse' : 12, 'charisme' : 11, 'courage' : 11, 'intelligence' : 12, 'attaque' : 12, 'vitesse' : 4.0, 'pvBase' : 30, 'pv' : 25, 'poidsPortable' : 10, 'poidsPortes' : 7.5})
print(perso.caracteristiques['force'])'''


univers.reglages.frequenceRencontre = 10

coup_de_poignard_en_fer = Action()
coup_de_poignard_en_fer.id = 'coup_de_poignard_en_fer'
coup_de_poignard_en_fer.cible = 1
coup_de_poignard_en_fer.description = "Attaque l'ennemi avec le poignard de base en fer."
coup_de_poignard_en_fer.effets = ['buff -2 pv -4 false [] 666']
coup_de_poignard_en_fer.esquive = True
coup_de_poignard_en_fer.nom = 'Coup de poignard de base en fer'
coup_de_poignard_en_fer.util = 2
coup_de_poignard_durandil = Action()
coup_de_poignard_durandil.id = 'coup_de_poignard_durandil'
coup_de_poignard_durandil.cible = 1
coup_de_poignard_durandil.description = "Attaque l'ennemi avec le poignard Durandil."
coup_de_poignard_durandil.effets = ['buff -2 pv -7 false [] 667']
coup_de_poignard_durandil.esquive = True
coup_de_poignard_durandil.nom = 'Coup de poignard en acier Durandil'
coup_de_poignard_durandil.util = 2
morsure = Action()
morsure.id = 'morsure'
morsure.cible = 1
morsure.description = "Une vilaine morsure d'une b�te avec des dents pointues."
morsure.effets = ['buff -2 pv -6 false [] 668']
morsure.esquive = True
morsure.nom = 'Morsure bestiale'
morsure.util = 2
morsure.tIncant = 0
soin = Action()
soin.id = 'soin'
soin.type = 1
soin.description = "Un simple sort de soin"
soin.nom = 'Soin des cornes'
soin.util = 0
soin.effets = ['buff -2 pv +5 false [] 671']
coup_de_cornes = Action()
coup_de_cornes.id = 'coup_de_cornes'
coup_de_cornes.cible = 1
coup_de_cornes.description = "La b�te charge et frappe de plein fouet avec ses cornes."
coup_de_cornes.effets = ['buff -2 pv -4 false [] 669']
coup_de_cornes.esquive = True
coup_de_cornes.nom = 'Coup de cornes'
coup_de_cornes.util = 2
coup_de_cornes.tIncant = 2
coup_de_massue_de_troll = Action()
coup_de_massue_de_troll.id = 'coup_de_massue_de_troll'
coup_de_massue_de_troll.cible = 1
coup_de_massue_de_troll.description = "Un redoutable coup donn� par la massue d'un troll."
coup_de_massue_de_troll.effets = ['buff -2 pv -8 false [] 670']
coup_de_massue_de_troll.esquive = True
coup_de_massue_de_troll.nom = 'Coup de massue de troll'
coup_de_massue_de_troll.util = 2
univers.actions = [coup_de_poignard_en_fer,coup_de_poignard_durandil,morsure,coup_de_cornes,coup_de_massue_de_troll,soin]

piece_or = Objet()
piece_or.poids = 0.01
piece_or.description = "Les pi�ces d'or sont la monnaie la plus courante en terre de Fangh."
piece_or.fonction = 0
piece_or.id = 'piece_or'
piece_or.nom = "Piece d'or"
piece_or.motsCles = ['#argent','#or']
piece_or.prix = 1
grande_besace = Objet()
grande_besace.poids = 0.3
grande_besace.description = "Un grand sac d'aventurier."
grande_besace.effetsEquip = ['buff -1 poidsPortable +30.0 true [] 132429062015']
grande_besace.empEquip = ['dos']
grande_besace.fonction = 1
grande_besace.id = "grande_besace"
grande_besace.motsCles = ['#conteneur','#tissu']
grande_besace.nom = "Grande besace de chasseur en cuir"
grande_besace.prix = 25
chemise_voleur = Objet()
chemise_voleur.poids = 0.3
chemise_voleur.description = "Une chemise sans doute disponible au march� noir."
chemise_voleur.effetsEquip = ['buff -1 adresse +1 false [] 133029062015']
chemise_voleur.empEquip = ['torse']
chemise_voleur.fonction = 1
chemise_voleur.id = "chemise_voleur"
chemise_voleur.motsCles = ['#vetement','#tissu']
chemise_voleur.nom = "Chemise silencieuse pour voleur"
chemise_voleur.prix = 50
cheval_basique = Objet()
cheval_basique.description = "Un basique compagnon de voyage."
cheval_basique.effetsPoss = ['buff -1 poidsPortable +30.0 true [] 133429062015']
cheval_basique.effetsEquip = ['buff -1 charisme -1 false [] 133529062015','buff -1 vitesse +6.0 true [] 133629062015']
cheval_basique.empEquip = ['monture']
cheval_basique.fonction = 1
cheval_basique.id = "cheval_basique"
cheval_basique.motsCles = ['#monture','#cheval']
cheval_basique.nom = "Cheval de base"
cheval_basique.prix = 100
verre_d_eau_de_vie_de_qualite = Objet()
verre_d_eau_de_vie_de_qualite.poids = 0.4
verre_d_eau_de_vie_de_qualite.description = "Un verre de tant en tant, �a fait de mal � personne."
verre_d_eau_de_vie_de_qualite.effetsUtil = ['buff -2 pv +1 false [] 134529062015']
verre_d_eau_de_vie_de_qualite.fonction = 2
verre_d_eau_de_vie_de_qualite.nbrUse = 1
verre_d_eau_de_vie_de_qualite.id = "verre_d_eau_de_vie_de_qualite"
verre_d_eau_de_vie_de_qualite.motsCles = ['#boisson','#alcool','#consommable']
verre_d_eau_de_vie_de_qualite.nom = "Verre d'eau de vie de qualit�"
verre_d_eau_de_vie_de_qualite.prix = 1.5
poignard_base = Objet()
poignard_base.poids = 0.5
poignard_base.description = "Un vulgaire poignard en fer. L�g�rement �mouss�."
poignard_base.effetsEquip = ['action -1 +coup_de_poignard_en_fer [] 290620152035','buff -1 attaque -2 false [] 290620152040','buff -1 charisme -1 false [] 290620152041']
poignard_base.empEquip = ['main_gauche', 'main_droite']
poignard_base.fonction = 1
poignard_base.id = "poignard_base"
poignard_base.motsCles = ['#poignard','#fer','#arme']
poignard_base.nom = "Poignard de base en fer"
poignard_base.prix = 10
poignard_durandil = Objet()
poignard_durandil.poids = 0.3
poignard_durandil.description = "Un poignard durandil en acier de qualit�."
poignard_durandil.effetsEquip = ['action -1 +coup_de_poignard_durandil [] 290620152043','buff -1 attaque -1 false [] 290620152044','buff -1 charisme +1 false [] 290620152036','buff -1 courage +1 false [] 290620152045']
poignard_durandil.empEquip = ['main_gauche', 'main_droite']
poignard_durandil.fonction = 1
poignard_durandil.id = "poignard_durandil"
poignard_durandil.motsCles = ['#poignard','#acier','#arme']
poignard_durandil.nom = "Poignard Durandil"
poignard_durandil.prix = 400
univers.objets = [piece_or,grande_besace,chemise_voleur,cheval_basique,verre_d_eau_de_vie_de_qualite,poignard_base,poignard_durandil]

les_poignards_perdus = Quete()
les_poignards_perdus.id = 'les_poignards_perdus'
les_poignards_perdus.nom = 'Les poignards perdus'
les_poignards_perdus.objectifs = [Objectif(id='ramasser_poignards',description="Ramasser 5 poignards dans la plaine du Ninejaddai.",objectif='ramasser poignard_base 5 plaine_du_ninejaddai *')]
les_poignards_perdus.objectifsAchevement = ['ramasser_poignards']
les_poignards_perdus.conditionsAchevement = ['force > 20']
les_poignards_perdus.tempsRestant = -1
univers.quetes = [les_poignards_perdus]

dialogueChevre = Dialogue(text='B�h�h�h�hh�.')
dialogueChevre.reponses = {'B�h�h� ?' : dialogueChevre}
dialogueVoyageur = Dialogue(text='Bonjour !')
dialogueVoyageur2 = Dialogue(text='Tout va pour le mieux ! ')
dialogueVoyageur3 = Dialogue(text='Bonne route.')
dialogueVoyageur4 = Dialogue(text="Ahhh. Eh bien ma femme m'a quitt�e, dieu en soit b�ni mais mes enfants sont partis avec elle. C'est plus silencieux me direz vous, c'est vrai, mais du coup je me retrouve tout seul.")
dialogueVoyageur5 = Dialogue(text="Oh! Du calme.")
dialogueVoyageur6 = Dialogue(text="Ca ira pour cette fois, mais soyez plus prudent � l'avenir.")
dialogueVoyageur7 = Dialogue(text="Je vais te niquez ta m�re ptit con !")
dialogueVoyageur8 = Dialogue(text="Pff... Longue histoire... En bref, j'ai perdu des poignards qui appartenaient � mon h�ritage familiale. Je fouille la r�gion pour essayer de les retrouver...")
dialogueVoyageur8.conditionsChoix = ['quete les_poignards_perdus 0']
dialogueVoyageur9 = Dialogue(text="Effectivement, un petit peu d'aide ne serait pas de refus. C'est tr�s gentil � vous. Ramenez-moi 5 poignards que vous aurez trouv� par terre. Vous serez r�compens�.")
dialogueVoyageur10 = Dialogue(text="Merci � vous, je ne bougerais pas d'ici. Vous savez o� me trouver.")
dialogueVoyageur10.effetsChoix = ['quete ajouter les_poignards_perdus []']
dialogueVoyageur11 = Dialogue(text = "Vous les avez trouv� ?",conditionsChoix = ['quete les_poignards_perdus 1'])
dialogueVoyageur12 = Dialogue(text="D'accord. Ils n'ont aucune valeur, si ce n'est une valeur sentimentale. Ils viennent de mon arri�re grand-p�re paternel !")
dialogueVoyageur13 = Dialogue(text="Merveilleux ! Tenez, voil� votre r�compense. Merci encore et bonne route !",conditionsChoix=['poss poignard_base > 9','objectif les_poignards_perdus ramasser_poignards 2'],effetsChoix=['objet -poignard_base 5 []','objet +piece_or 75 []','quete achever les_poignards_perdus []'])
dialogueVoyageur11.reponses = {"Non, pas encore." : dialogueVoyageur12, "Oui, tenez. (Terminer la qu�te)" : dialogueVoyageur13}
dialogueVoyageur.reponses = {"Bonjour, comment �a va ?" : dialogueVoyageur2,"Tu regardes quoi fils de pute ? Tu veux ma photo ?" : dialogueVoyageur5,"Que faites-vous ici ?" : dialogueVoyageur8,"A propos des poignards..." : dialogueVoyageur11}
dialogueVoyageur8.reponses = {"Vous avez besoin d'aide ?" : dialogueVoyageur9,"Bonne chance." : dialogueVoyageur3}
dialogueVoyageur9.reponses = {"Si c'est r�compens�, alors j'accepte. (Accepter la qu�te)" : dialogueVoyageur10,"D�sol�, je vous aurais bien aid� mais je crains que vos poignards soient d�finitivement perdus... Bonne chance. (Refuser la qu�te)" : dialogueVoyageur3}
dialogueVoyageur2.reponses = {"Tant mieux ! Bonne journ�e..." : dialogueVoyageur3, "Comment va la famille ?" : dialogueVoyageur4}
dialogueVoyageur5.reponses = {"Excusez-moi... Je vous ai pris pou quelqu'un d'autre..." : dialogueVoyageur6, "Tu vas faire quoi ?" : dialogueVoyageur7}

bouc = Creature()
bouc.id = 'bouc'
bouc.nom = 'Bouc'
bouc.actions = [coup_de_cornes,soin]
bouc.amisAvec = ['bouc']
bouc.caracteristiques.update({'courage' : 7, 'adresse' : 13, 'attaque' : 9, 'pvBase' : 15, 'pv' : 15})
bouc.caracteristiques.setParent(bouc)
bouc.description = "Une innofensive cr�ature qui passe ses journ�es � brouter l'herbe verte."
bouc.dialogue = dialogueChevre
bouc.motsCles = ['#bouc','#betail','#innofensif']
bouc.exp_win = 3
bouc.hostil = 5
bouc.strategieDefensive = 2
bouc.strategieOffensive = 2
bouc.inventaire = [piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or]
coyote_affame = Creature()
coyote_affame.id = 'coyote_affame'
coyote_affame.nom = 'Coyote affam�'
coyote_affame.actions = [morsure]
coyote_affame.caracteristiques.update({'courage' : 11, 'adresse' : 12, 'attaque' : 19, 'pvBase' : 18, 'pv' : 15})
coyote_affame.caracteristiques.setParent(coyote_affame)
coyote_affame.description = "Un dangereux charognard qui chasse la nuit."
coyote_affame.motsCles = ['#coyote_affame','#charognard','#agressif']
coyote_affame.exp_win = 4
coyote_affame.hostil = 7
coyote_affame.inventaire = [piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or]
rat_pesteux = Creature()
rat_pesteux.id = 'rat_pesteux'
rat_pesteux.nom = 'Rat pesteux'
rat_pesteux.actions = [morsure]
rat_pesteux.amisAvec = ['rat_pesteux']
rat_pesteux.caracteristiques.update({'courage' : 5, 'adresse' : 13, 'attaque' : 11, 'pvBase' : 5, 'pv' : 5})
rat_pesteux.caracteristiques.setParent(rat_pesteux)
rat_pesteux.description = "Un mis�rable rat portant toutes les maladies imaginables et couinant � longueur de journ�e."
rat_pesteux.motsCles = ['#rat_pesteux','#charognard','#hostil']
rat_pesteux.exp_win = 4
rat_pesteux.hostil = 6
rat_pesteux.strategieOffensive = 0
orque_miteux = Creature()
orque_miteux.id = 'orque_miteux'
orque_miteux.nom = 'Orque miteux'
orque_miteux.actions = [coup_de_poignard_en_fer]
orque_miteux.amisAvec = ['orque_miteux']
orque_miteux.caracteristiques.update({'courage' : 8, 'adresse' : 9, 'attaque' : 9, 'pvBase' : 15, 'pv' : 15})
orque_miteux.caracteristiques.setParent(orque_miteux)
orque_miteux.description = "Un orque ayant quitt� sa l�gion et s'�tant reconverti en bandit de bas �tage."
orque_miteux.motsCles = ['#orque_miteux','#humanoide','#orque','#bandit']
orque_miteux.exp_win = 8
orque_miteux.hostil = 6
orque_miteux.niveau = 2
orque_miteux.strategieDefensive = 1
orque_miteux.inventaire = [piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,poignard_base]
troll_geant_maladroit = Creature()
troll_geant_maladroit.id = 'troll_geant_maladroit'
troll_geant_maladroit.nom = 'Troll g�ant maladroit'
troll_geant_maladroit.actions = [coup_de_massue_de_troll]
troll_geant_maladroit.amisAvec = ['troll_geant_maladroit']
troll_geant_maladroit.caracteristiques.update({'courage' : 20, 'adresse' : 6, 'attaque' : 7, 'pvBase' : 50, 'pv' : 50})
troll_geant_maladroit.caracteristiques.setParent(troll_geant_maladroit)
troll_geant_maladroit.description = "Une innofensive cr�ature qui passe ses journ�es � brouter l'herbe verte."
troll_geant_maladroit.dialogue = dialogueChevre
troll_geant_maladroit.motsCles = ['#troll_geant_maladroit','#betail','#innofensif']
troll_geant_maladroit.exp_win = 35
troll_geant_maladroit.hostil = 4
troll_geant_maladroit.niveau = 3
troll_geant_maladroit.strategieDefensive = 0
troll_geant_maladroit.strategieOffensive = 2
voyageur = Creature()
voyageur.id = 'voyageur'
voyageur.nom = 'Voyageur'
voyageur.caracteristiques.update({'courage' : 12, 'adresse': 11, 'attaque' : 10, 'pvBase' : 20, 'pv' : 20})
voyageur.caracteristiques.setParent(voyageur)
voyageur.description = 'Un voyageur traversant les plaines du Ninejaddai.'
voyageur.inventaire = [piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or,piece_or]
voyageur.motsCles = ['#voyageur','#humain']
voyageur.dialogue = dialogueVoyageur


univers.creatures = [bouc,coyote_affame,rat_pesteux,orque_miteux,troll_geant_maladroit,voyageur]
bouc1 = copy.deepcopy(bouc)
bouc1.id += '#'+str(id(bouc1))
bouc2 = copy.deepcopy(bouc)
bouc2.id += '#'+str(id(bouc2))
bouc3 = copy.deepcopy(bouc)
bouc3.id += '#'+str(id(bouc3))
plaine_du_ninejaddai = Region()
plaine_du_ninejaddai.id = 'plaine_du_ninejaddai'
plaine_du_ninejaddai.nom = 'Plaine du Ninejaddai'
plaine_du_ninejaddai.motsCles = ['#plaine','#ninejaddai']
plaine_du_ninejaddai.creatures = [[bouc1,[1,1]],[bouc2,[1,1]],[bouc3,[0,1]]]
plaine_du_ninejaddai.creaturesRencontrables = ['bouc','orque_miteux','troll_geant_maladroit','rat_pesteux','coyote_affame']
plaine_du_ninejaddai.description = "Une plaine sauvage malgr� les nombreux p�turages de boucs."
foret_de_schlipak = Region()
foret_de_schlipak.id = 'foret_de_schlipak'
foret_de_schlipak.nom = 'For�t de Schlipak'
foret_de_schlipak.motsCles = ['#foret']
foret_de_schlipak.creaturesRencontrables = ['orque_miteux','troll_geant_maladroit']
foret_de_schlipak.description = "Une grande for�t peupl�e de divers peuples et diverses cr�atures."
plaine_du_ninejaddai_lisiere_schlipak = Region()
plaine_du_ninejaddai_lisiere_schlipak.id = 'plaine_du_ninejaddai_lisiere_schlipak'
plaine_du_ninejaddai_lisiere_schlipak.nom = 'Plaine du Ninejaddai - Lisi�re de la for�t de Schlipak'
plaine_du_ninejaddai_lisiere_schlipak.regionParent = 'plaine_du_ninejaddai'
plaine_du_ninejaddai_lisiere_schlipak.motsCles = ['#plaine','#ninejaddai', '#lisiere','foret']
plaine_du_ninejaddai_lisiere_schlipak.creatures = [[bouc1,[1,1]],[bouc2,[1,1]],[bouc3,[0,1]]]
plaine_du_ninejaddai_lisiere_schlipak.creaturesRencontrables = ['bouc','orque_miteux','troll_geant_maladroit','rat_pesteux']
plaine_du_ninejaddai_lisiere_schlipak.description = "La lisi�re de la for�t de Schlipak avec la plaine du Ninejaddai."
plaine_du_ninejaddai_route = Region()
plaine_du_ninejaddai_route.id = 'plaine_du_ninejaddai_route'
plaine_du_ninejaddai_route.nom = 'Plaine du Ninejaddai - Route de Zoyek'
plaine_du_ninejaddai_route.regionParent = 'plaine_du_ninejaddai'
plaine_du_ninejaddai_route.motsCles = ['#plaine','#ninejaddai','#route']
plaine_du_ninejaddai_route.creatures = [[bouc1,[1,2]],[bouc2,[1,2]],[bouc3,[0,2]]]
plaine_du_ninejaddai_route.creaturesRencontrables = ['bouc','rat_pesteux']
plaine_du_ninejaddai_route.description = "La route traversant la plaine du Ninejaddai et reliant Zoyek au lac de Zblouf."
bordure_fleuve_elibed = Region()
bordure_fleuve_elibed.id = 'bordure_fleuve_elibed'
bordure_fleuve_elibed.nom = 'Bordures du fleuve Elibed'
bordure_fleuve_elibed.motsCles = ['#fleuve','#ninejaddai','#plaine']
bordure_fleuve_elibed.creatures = [[bouc1,[1,1]],[bouc2,[1,1]],[bouc3,[0,1]]]
bordure_fleuve_elibed.creaturesRencontrables = ['bouc','orque_miteux','troll_geant_maladroit','rat_pesteux']
bordure_fleuve_elibed.description = "Les bordures du fleuves Elibed qui s�pare la plaine du Ninejaddai des terres sauvages de Kwzprtt."
univers.regions = [plaine_du_ninejaddai,foret_de_schlipak,plaine_du_ninejaddai_lisiere_schlipak,plaine_du_ninejaddai_route,bordure_fleuve_elibed]


def ModifierMap(map = None):
    if map == None: map = []
    i = 0
    while i < len(map):
        a = 0        
        while a < len(map[i]):
            map[i][a] = copy.deepcopy(map[i][a])
            a += 1
        i += 1
    return map


univers.map = [[plaine_du_ninejaddai_route,plaine_du_ninejaddai,plaine_du_ninejaddai_lisiere_schlipak,foret_de_schlipak,foret_de_schlipak,foret_de_schlipak],
               [plaine_du_ninejaddai_route,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai_lisiere_schlipak,foret_de_schlipak,foret_de_schlipak],
               [plaine_du_ninejaddai,plaine_du_ninejaddai_route,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai_lisiere_schlipak,foret_de_schlipak],
               [plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai_route,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai_lisiere_schlipak],
               [plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai_route,plaine_du_ninejaddai_route,plaine_du_ninejaddai],
               [plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai_route],
               [plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai],
               [bordure_fleuve_elibed,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai],
               [plaine_du_ninejaddai,bordure_fleuve_elibed,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai,plaine_du_ninejaddai]
               ]
univers.map = ModifierMap(univers.map)
map = univers.map
i=0
'''while i < len(map):
        a = 0        
        while a < len(map[i]):
            print(id(map[i][a]))
            a+=1
        i+=1'''

personnage.mapUnivers = copy.deepcopy(univers.map)


personnage.nom = 'Elendil'
personnage.id = 'elendil'
personnage.motsCles = ['#humain']
personnage.emplacements = {'dos' : '', 'main_gauche' : '', 'main_droite' : '', 'torse' : '', 'monture' : ''}
personnage.caracteristiques.update({'force' : 10, 'adresse' : 12, 'charisme' : 11, 'courage' : 11, 'intelligence' : 12, 'attaque' : 12, 'vitesse' : 4.0, 'pvBase' : 30, 'pv' : 15, 'poidsPortable' : 10, 'poidsPortes' : 7.5})
personnage.positionX = 5
personnage.positionY = 3
personnage.inventaire = {poignard_base:15}
personnage.quetesActives.append(copy.deepcopy(les_poignards_perdus))
personnage.mapUnivers[6][3].creatures.append([copy.deepcopy(voyageur),[2,1]])
personnage.mapUnivers[6][3].objets = [[poignard_base,[1,1]],[poignard_base,[1,1]],[poignard_base,[1,1]],[poignard_base,[1,1]],[poignard_base,[1,1]]]

univers.textes = {}
univers.textes['entrer foret_de_schlipak nuit *'] = ["Malgr� l'obscurit� de la nuit, vous p�n�trez dans la sombre for�t de Schlipak. Peu � peu les arbres se font de plus en plus dense et vous vous voyez vite tremp� par l'humidit� des plantes."]
univers.textes['entrer foret_de_schlipak jour *'] = ["Sous un soleil de plomb, vous p�n�trez dans la sombre for�t de Schlipak. Peu � peu l'air se rafraichit et l'humidit� de la for�t se fait sentir. La v�g�tation est tr�s dense et tr�s feuillue."]
univers.textes['entrer foret_de_schlipak * *'] = ["Vous p�n�trez dans la sombre for�t de Schlipak. Peu � peu la v�g�tation s'�paissit et vous voyez difficilement � plus de 50m."]
univers.textes['entrer plaine_du_ninejaddai jour *'] = ["Vous arrivez dans les vastes plaines du Ninejaddai. Elles s'�tendent � perte de vue et vous observer quelques bosquets par ci par l�."]
univers.textes['entrer plaine_du_ninejaddai nuit *'] = ["Vous remarquez que, malgr� l'obscurit� qui vous entoure, le relief s'est aplati et qu'une plaine se dessine devant vous. Il s'agit de la plaine du Ninejaddai. Au loin, vous entendez des cris de coyotes."]
univers.textes['entrer plaine_du_ninejaddai_lisiere_schlipak * *'] = ["Vous arrivez � la lisi�re de la for�t de Schlipak. D'un c�t� l'�paisse silhouette de la for�t, de l'autre le vide de la plaine du Ninejaddai."]
univers.textes['entrer plaine_du_ninejaddai_route * *'] = ["Vous rejoignez une route bien distincte qui traverse la plaine."]
univers.textes['entrer bordure_fleuve_elibed * *'] = ["Vous arrivez au bord du fleuve qui s�pare les terres sauvages de la plaine du Ninejaddai. Le courant est trop fort pour pouvoir franchir le fleuve."]
univers.textes['decrire plaine_du_ninejaddai_route * *'] = ["La route semble aller du sud-ouest au nord-est."]
univers.textes['decrire 0,0 *'] = ["La route semble aller du sud � l'est."]
univers.textes['decrire 1,0 *'] = ["La route semble aller de l'ouest au nord-est."]
univers.textes['decrire 4,3 *'] = ["La route semble aller du sud-ouest au nord."]
univers.textes['decrire 4,4 *'] = ["La route semble aller du sud au nord-est."]
univers.textes['aller N'] = ["Vous partez vers le nord.","Vous vous dirigez vers le nord","Vous allez au nord."]
univers.textes['aller S'] = ["Vous partez vers le sud.","Vous vous dirigez vers le sud","Vous allez au sud."]
univers.textes['aller O'] = ["Vous partez vers l'ouest.","Vous vous dirigez vers l'ouest","Vous allez � l'ouest."]
univers.textes['aller E'] = ["Vous partez vers l'est.","Vous vous dirigez vers l'est","Vous allez � l'est."]
univers.textes['aller NE'] = ["Vous partez vers le nord-est.","Vous vous dirigez vers le nord-est","Vous allez au nord-est."]
univers.textes['aller NO'] = ["Vous partez vers le nord-ouest.","Vous vous dirigez vers le nord-ouest","Vous allez au nord-ouest."]
univers.textes['aller SE'] = ["Vous partez vers le sud-est.","Vous vous dirigez vers le sud-est","Vous allez au sud-est."]
univers.textes['aller SO'] = ["Vous partez vers le sud-ouest.","Vous vous dirigez vers le sud-ouest","Vous allez au sud-ouest."]
univers.textes['mort #bandit * nuit'] = ["Les bandits sont souvent des couards qui profitent de l'obscurit� pour tuer les voyageurs et d�pouiller leur cadavre. Malgr�s un combat �pique, ils vous ont tu�."]
univers.textes['mort #gibier #foret nuit'] = ["Une cr�ature massue vous percute dans l'obscurit� de la for�t et vous d�c�dez sur le coup."]
univers.textes['mort * #foret nuit'] = ["Une masse vous percute dans l'obscurit� de la for�t et vous d�c�dez sur le coup."]
univers.textes['mort * * nuit'] = ["C'est dans une nuit sombre que vous d�c�dez."]
univers.textes['mort * * *'] = ["Aujourd'hui est un beau jour pour mourir."]
univers.textes['entrer * nuit *'] = ["Vous avancez malgr�s l'obscurit� mais ne parvenez � distinguer ce qui vous entoure."]
univers.textes['entrer * jour *'] = ["Vous arrivez dans une nouvelle r�gion sous un soleil �clatant."]
univers.textes['entrer * * *'] = ["Vous arrivez dans une nouvelle r�gion."]
univers.textes['ramasser * * *'] = ["Vous ramassez l'objet par terre."]
univers.textes['ajout * * *'] = ["Un nouvel objet a �t� ajout� � votre inventaire !"]
univers.textes['enlever * * *'] = ["Un objet a �t� retir� de votre inventaire !"]
univers.textes['jeter * * *'] = ["Vous jetez un objet � terre."]
univers.textes['cacher * * *'] = ["Vous cachez un objet sous la terre au pied d'un rocher."]
univers.textes['equiper * * *'] = ["Vous avez �quip� cet objet."]
univers.textes['desequiper * * *'] = ["Vous avez retir� cet objet."]
univers.textes['utiliser * * *'] = ["Vous utilisez cet objet."]
univers.textes['erreur objet_non_possede'] = ["Vous ne poss�dez pas cet objet."]
univers.textes['erreur objet_non_trouvable'] = ["Objet introuvable dans votre zone."]
univers.textes['erreur creature_non_trouvable'] = ["Cr�ature introuvable dans votre zone."]
univers.textes['erreur action_non_autorisee'] = ["Vous ne pouvez r�aliser cette action."]
univers.textes['erreur objet_non_trouvable_depouille'] = ["Objet introuvable sur la d�pouille."]
univers.textes['erreur depouille_non_trouvable'] = ["D�pouille introuvable dans votre zone."]
univers.textes['erreur mauvaise_direction'] = ["Direction incorrect."]
univers.textes['erreur *'] =  ["Action non autoris�e."]
univers.textes['achever_quete *'] = ['Vous avez achev� une qu�te !']
univers.textes['ajouter_quete *'] = ['Une nouvelle qu�te a �t� ajout�e � vos qu�tes actives.']
univers.textes['retirer_quete *'] = ['Une qu�te a �t� supprim� de vos qu�te active.']
univers.textes['rencontre bouc * *'] = ["Alors que vous marchiez tranquillement, un bouc surgit soudainement d'un bosquet et vous barre la route."]
univers.textes['rencontre coyote_affame * *'] = ["Vous avancez p�niblement � pas lent quand vous entendez tout � coup des aboiements. Ils sont d'abord lointains mais semblent se rapprocher constament. Peu � peu vous entendez des bruits dans les feuillages puis surgit d'un coup un coyote bavant et montrant les crocs. Il s'avance petit � petit vers vous."]
univers.textes['rencontre * * *'] = ["Une cr�ature vous barre soudainement la route."]
univers.textes['fuite * * *'] = ["%auteur s'enfuit."]
univers.textes['fuite !PLAYER * *'] = ['Vous parvenez � fuir !']
univers.textes['fuite_echec * * *'] = ["%auteur ne parvient pas � s'enfuir !"]
univers.textes['fuite_echec !PLAYER * *'] = ['Vous ne parvenez pas � fuir !']
univers.textes['action * * * * *'] = ["%auteur attaque %cible avec %action !"]
univers.textes['action * !PLAYER * * *'] = ["Vous �tes attaqu� par %auteur avec %action !"]
univers.textes['buff !PLAYER gain pv * *'] = ["Vous gagnez %valeur point(s) de vie !"]
univers.textes['buff !PLAYER perte pv * *'] = ["Vous perdez %valeur point(s) de vie !"]
univers.textes['buff * gain * * *'] = ["%cible gagne %valeur point(s) de %caract !"]
univers.textes['buff * perte * * *'] = ["%cible perd %valeur point(s) de %caract !"]
univers.textes['esquive * * * *'] = ["%cible esquive %action !"]
univers.textes['esquive !PLAYER * * *'] = ["Vous esquivez %action !"]
univers.textes['mort * * *'] = ["%cible meurt ! "]
univers.textes['mort #betail * *'] = ["Du b�tail est mort !"]
univers.textes['mort !PLAYER * *'] = ["%cible est meurt ! "]
univers.textes['incantation * * * * *'] = ["%auteur d�marre l'incantation %action pour une dur�e de %duree tour(s) !"]
univers.textes['action_ratee * * * * *'] = ["%auteur rate %cible avec %action !"]
univers.textes['action_ratee * * soin * *'] = ["%auteur rate un soin !"]
univers.textes['action * * soin * *'] = ["%auteur se soigne !"]
univers.textes['* * * * * *'] = ["ERREUR"]


personnage = effets.AjoutEffet(personnage,'buff 1 vitesse +1.2 true [] 2654645656',univers)

stop = False
while stop == False:
    entree = input("cmd: ")
    if entree == 'stop': break
    univers,personnage = console.ExecuterCommande(univers,personnage,entree)


print()
print(round(time.clock(),10))