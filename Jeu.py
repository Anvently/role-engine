# -*-coding:Latin-1 -*
from Personnage import *
from Univers import *
from Creature import *
from Region import *
import re
import copy
from random import *
from Objet import *
import time
import sys
from Quete import *
class effets:
    """Classe qui gère la gestion des effets et leur application. Contient des méthodes."""
    def AjoutEffet(personnage = Personnage(), effet = "", univers = Univers(), joueur = ""):
        '''Applique un effet et l'ajoute à la liste des effets actifs.'''
        if joueur == "": joueur = personnage #Si aucun objet désignant le véritable personnage (personnage serait alors une créature), on confond les deux.
        listConditions = effet[effet.find('[')+1:effet.find(']')].split('/')
        if listConditions == ['']: listConditions = []
        if conditions.VerifListConditions(personnage,univers,listConditions) == True:            
            type = effet.split()[0]

            if type == "buff":
                 caract = effet.split()[2]
                 operateur = effet.split()[3][0]
                 valeur = effet.split()[3][1:]
                 valeurReel = valeur
                 if (not '.' in valeur) and effet.split()[4] == 'false' and caract != 'pv':
                     maximum = univers.reglages.maxCaract
                     if operateur == "+":
                         if personnage.caracteristiques[caract] + int(valeur) <= maximum and personnage.caracteristiques[caract] + int(valeur) >= 0:
                             personnage.caracteristiques[caract] += int(valeur)
                         elif personnage.caracteristiques[caract] + int(valeur) > maximum:
                             effet = util.ModifierValeurBuff(effet, maximum - personnage.caracteristiques[caract])
                             valeurReel = maximum - personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = maximum                             
                         elif personnage.caracteristiques[caract] + int(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, 0 - personnage.caracteristiques[caract])
                             valeurReel = 0 - personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0                                                 
                     elif operateur == "-":
                         if personnage.caracteristiques[caract] - int(valeur) >= 0 and personnage.caracteristiques[caract] - int(valeur) <= maximum:
                             personnage.caracteristiques[caract] -= int(valeur)
                         elif personnage.caracteristiques[caract] - int(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, personnage.caracteristiques[caract])
                             valeurReel = personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0                             
                         elif personnage.caracteristiques[caract] - int(valeur) > maximum:
                             effet = util.ModifierValeurBuff(effet, -maximum + personnage.caracteristiques[caract])
                             valeurReel = -maximum + personnage.caracteristiques[caract]      
                             personnage.caracteristiques[caract] = maximum                                     

                 elif caract == 'vitesse' or caract == 'poidsPortable':
                 
                     if operateur == "+":
                         if personnage.caracteristiques[caract] + float(valeur) >= 0:
                             personnage.caracteristiques[caract] = round(personnage.caracteristiques[caract] + float(valeur), 1)
                         elif personnage.caracteristiques[caract] + float(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, 0 - personnage.caracteristiques[caract])
                             valeurReel = 0 - personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0.0                             
                     elif operateur == "-":
                         if personnage.caracteristiques[caract] - float(valeur) >= 0:
                             personnage.caracteristiques[caract] = round(personnage.caracteristiques[caract] - float(valeur), 1)         
                         elif personnage.caracteristiques[caract] - float(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, personnage.caracteristiques[caract])
                             valeurReel = personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0                                     
            
                 elif caract == 'pvBase' or (caract == 'pv' and effet.split()[4] == 'true'):
                 
                     if operateur == "+":
                         if personnage.caracteristiques[caract] + int(valeur) >= 0:
                             personnage.caracteristiques[caract] += int(valeur)
                         elif personnage.caracteristiques[caract] + int(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, 0 - personnage.caracteristiques[caract])
                             valeurReel = 0 - personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0                             
                     elif operateur == "-":
                         if personnage.caracteristiques[caract] - int(valeur) >= 0:
                             personnage.caracteristiques[caract] -= int(valeur)  
                         elif personnage.caracteristiques[caract] - int(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, personnage.caracteristiques[caract])
                             valeurReel = personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0                                      

                 elif caract == 'pv' and effet.split()[4] == 'false':

                     if operateur == "+":
                         if personnage.caracteristiques[caract] + int(valeur) >= 0 and personnage.caracteristiques[caract] + int(valeur)  <= personnage.caracteristiques['pvBase']:
                             personnage.caracteristiques[caract] += int(valeur)
                         elif personnage.caracteristiques[caract] + int(valeur) > personnage.caracteristiques['pvBase']:
                             effet = util.ModifierValeurBuff(effet, personnage.caracteristiques['pvBase'] - personnage.caracteristiques[caract])
                             valeurReel = personnage.caracteristiques['pvBase'] - personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = personnage.caracteristiques['pvBase']                           
                         elif personnage.caracteristiques[caract] + int(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, 0 - personnage.caracteristiques[caract])
                             valeurReel = 0 - personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0         
                     elif operateur == "-":
                         if personnage.caracteristiques[caract] - int(valeur) >= 0 and personnage.caracteristiques[caract] - int(valeur)  <= personnage.caracteristiques['pvBase']:
                             personnage.caracteristiques[caract] -= int(valeur)   
                         elif personnage.caracteristiques[caract] - int(valeur) < 0:
                             effet = util.ModifierValeurBuff(effet, personnage.caracteristiques[caract])
                             valeurReel = personnage.caracteristiques[caract]
                             personnage.caracteristiques[caract] = 0                           
                         elif personnage.caracteristiques[caract] - int(valeur) > personnage.caracteristiques['pvBase']:
                             effet = util.ModifierValeurBuff(effet, -personnage.caracteristiques['pvBase'] + personnage.caracteristiques[caract])
                             valeurReel = -personnage.caracteristiques['pvBase'] + personnage.caracteristiques[caract] 
                             personnage.caracteristiques[caract] = personnage.caracteristiques['pvBase']                                 
                 
                 opTextuel = ""
                 if operateur == "+": opTextuel = "gain"
                 elif operateur == "-": opTextuel = "perte"
                 if personnage.type == "joueur": cible = "!PLAYER"
                 elif personnage.type == "creature": cible = re.findall('^[a-zA-Z_]*[^#]',personnage.id)[0]
                 print(textes.TrouverTexte(univers,personnage,'buff '+cible+' '+opTextuel+' '+caract+' '+str(joueur.positionX) + ',' + str(joueur.positionY)+' '+temps.MomentJournee(joueur.heure),{'caract':caract,'valeur':str(valeurReel),'operateur':opTextuel,'cible':personnage.nom,'lieu':joueur.mapUnivers[joueur.positionX][joueur.positionY].nom}))

                 if int(effet.split()[1]) != -2: personnage.effets.append(effet)                 

            elif type == "interdiction":

                operateur = effet.split()[2][0]
                interdiction  = effet.split()[2:4]
                interdiction[0] = interdiction[0][1:]
                interdiction = " ".join(interdiction)
                if operateur == "+":
                    if personnage.interdictions.count(interdiction) == 0: #Si l'interdiction n'existe pas déjà,
                        personnage.interdictions.append(interdiction) #On l'ajoute
                        if int(effet.split()[1]) != -2: personnage.effets.append(effet)
                elif operateur == "-":
                    if personnage.interdictions.count(interdiction) > 0:
                        personnage.interdictions.remove(interdiction)
                        if int(effet.split()[1]) != -2: personnage.effets.append(effet)

            elif type == "etat":

                etat_old = personnage.etat
                new_effet = effet.split()
                personnage.etat = int(new_effet[2])           
                new_effet[2] = str(etat_old)
                effet = " ".join(new_effet)
                if int(effet.split()[1]) != -2: personnage.effets.append(effet)

            elif type == "teleportation":

                destination = effet.split()[1]
                x = int(destination.split(',')[0])
                y = int(destination.split(',')[1])
                regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
                regionFuture = personnage.mapUnivers[x][y]
                personnage = deplacements.ChangementZone(univers,personnage,regionActuelle,regionFuture,x,y)

            elif type == "objet":

                operateur = effet.split()[1][0]
                valeur = effet.split()[1][1:]
                quantite = int(effet.split()[2])
                obj=util.TrouverObject(univers.objets,re.findall('^[a-zA-Z_]*[^#]',valeur)[0])
                if obj==None: 
                    print('Objet inexistant')
                    return False
                if operateur == "+":
                    while quantite > 0:
                        personnage = interactions.AjoutObjet(personnage,obj,univers)
                        quantite -= 1
                elif operateur == "-":
                    while quantite > 0:
                        personnage = interactions.EnleverObjet(personnage,obj,univers)
                        quantite -= 1

            elif type == "action" or type == "hostilite": #Les deux sont identiques donc autant faire d'une pierre deux coups.
                operateur = effet.split()[2][0]
                valeur = effet.split()[2][1:]
                if type == 'action': #On refera la différence à la fin
                    personnageList = personnage.actions
                    objectList = univers.actions
                elif type == 'hostilite':
                    personnageList = personnage.hostilites
                    objectList = univers.creatures
                objet = util.TrouverObject(objectList,re.findall('^[a-zA-Z_]*[^#]',valeur)[0])
                if objet==None:
                    print('Action ou créature inexistante')
                    return False
                if operateur == "+": #Si on ajoute                  
                    if not objet in personnageList: #Si l'objet n'est pas déjà dans la liste
                        personnageList.append(objet)
                        if int(effet.split()[1]) != -2: personnage.effets.append(effet)
                elif operateur == "-":
                    if objet in personnageList: #Si l'objet est dans la liste
                        personnageList.remove(objet)
                        if int(effet.split()[1]) != -2: personnage.effets.append(effet)
                if type == 'action': personnage.actions = personnageList #On différencie les deux                  
                elif type == 'hostilite': personnage.hostilites = personnageList
            
            elif type == "emplacement": #Si l'effet concerne un emplacement.
                operateur = effet.split()[1]
                idEmplacement = effet.split()[1][1:]
                if operateur == '+': #Si l'on veut ajouter un emplacement utilisable.
                    if not idEmplacement in personnage.emplacements: #Si l'emplacement n'est pas déjà utilisable.
                        personnage.emplacements[idEmplacement] = '' #On ajoute l'emplacement dans la liste des emplacements utilisables.
                elif operateur == "-": #Si l'on veut enlever un emplacement utilisable.
                    if idEmplacement in personnage.emplacements: #Si l'emplacement est déjà dans la liste des emplacements utilisables.
                        if personnage.emplacements[idEmplacement] == '': #Si aucun objet n'est équipé dans l'emplacement.
                            del personnage.emplacements[idEmplacement] #On supprime l'emplacement de la liste des emplacements utilisables.
                        elif personnage.emplacements[idEmplacement] != '': #Si un objet est équipé sur l'emplacement.
                            personnage = interactions.DesequiperObjet(personnage,personnage.emplacements[idEmplacement],univers) #On déséquippe l'objet.
                            del personnage.emplacements[idEmplacement] #On supprime l'emplacement de la liste des emplacements utilisables.

            elif type == "quete":
                operateur = effet.split()[1]
                idQuete = effet.split()[2]
                if operateur == 'ajouter': #Si l'on doit ajouter une quête.
                    if not idQuete in [quete.id for quete in personnage.quetesActives]: #Si la quête n'est pas déjà active.
                        quete = util.TrouverObject(univers.quetes,idQuete)
                        if quete=="None":
                            print('Quête inexistante')
                            return False
                        personnage.quetesActives.append(copy.deepcopy(quete)) #On ajoute la quête à la liste des quêtes actives.
                        print(textes.TrouverTexte(univers,personnage,'ajouter_quete '+quete.id))
                        personnage = quetes.VerificationQuetes(univers,personnage) #On vérifie les quêtes pour éventuellement démarrer certains objectifs de la nouvelle quête.
                elif operateur == 'retirer': #Si l'on doit retirer une quête.
                    for quete in personnage.quetesActives:
                        if quete.id == idQuete: #Si la quête parcouru est celle qu'on veut enlever.
                            personnage.quetesActives.remove(quete) #On supprime la quête de la liste des quêtes actives.
                            print(textes.TrouverTexte(univers,personnage,'retirer_quete '+quete.id))
                elif operateur == 'achever': #Si l'on doit achever une quête.
                    for quete in personnage.quetesActives:
                        if quete.id == idQuete: 
                            print(textes.TrouverTexte(univers,personnage,'achever_quete '+quete.id))
                            personnage = effets.AjoutListeEffets(personnage,univers,quete.effetsSucces) #On applique les effets de succès.
                            personnage.quetesAchevees.append(quete.id) #On ajoute la quête à la liste des quêtes achevées.
                            personnage.quetesActives.remove(quete) #On supprime la quête de la liste des quêtes actives.

            else:
                print("Erreur dans le type d'effet.")
        
        return personnage   
    def SupprEffet(personnage = Personnage(),effet = "", univers = Univers(), joueur = ""):
        '''Retire un effet du personnage et de la liste des effets actifs.'''
        if joueur == "": joueur = personnage #Si aucun objet désignant le véritable personnage (personnage serait alors une créature), on confond les deux.
        type = effet.split()[0]        
        effetExist = False
        if util.TrouverEffet(effet,personnage.effets) != -1: 
                 effet = personnage.effets[util.TrouverEffet(effet,personnage.effets)]
                 effetExist = True
        if effetExist == True:
            if type == "buff":            
                 caract = effet.split()[2]
                 operateur = effet.split()[3][0]
                 valeur = effet.split()[3][1:]
                 if not '.' in valeur:
                     
                     if operateur == "+":
                         personnage.caracteristiques[caract] -= int(valeur)
                     elif operateur == "-":
                         personnage.caracteristiques[caract] += int(valeur)
                            
                 elif '.' in valeur:
                     
                     if operateur == "+":
                         personnage.caracteristiques[caract] = round(personnage.caracteristiques[caract] - float(valeur), 1)
                     elif operateur == "-":
                         personnage.caracteristiques[caract] = round(personnage.caracteristiques[caract] + float(valeur), 1)                                 
                                     
                 opTextuel = ""
                 if operateur == "+": opTextuel = "perte"
                 elif operateur == "-": opTextuel = "gain"
                 if personnage.type == "joueur": cible = "!PLAYER"
                 elif personnage.type == "creature": cible = re.findall('^[a-zA-Z_]*[^#]',personnage.id)[0]
                 print(textes.TrouverTexte(univers,personnage,'buff '+cible+' '+opTextuel+' '+caract+' '+str(joueur.positionX) + ',' + str(joueur.positionY)+' '+temps.MomentJournee(joueur.heure),{'caract':caract,'valeur':str(valeur),'cible':personnage.nom,'lieu':joueur.mapUnivers[joueur.positionX][joueur.positionY].nom}))
                          
            elif type == "interdiction":

                operateur = effet.split()[2][0]
                interdiction  = effet.split()[2:4]
                interdiction[0] = interdiction[0][1:]
                interdiction = " ".join(interdiction)
                if operateur == "+":
                    if personnage.interdictions.count(interdiction) > 0:
                        personnage.interdictions.remove(interdiction)
                elif operateur == "-":
                    if personnage.interdictions.count(interdiction) == 0:
                        personnage.interdictions.append(interdiction)         
                                      
            elif type == "etat":
                personnage.etat = int(effet.split()[2])

            elif type == "action" or type == "hostilite":
                operateur = effet.split()[2][0]
                valeur = effet.split()[2][1:]
                if type == 'action': #On refera la différence à la fin
                    personnageList = personnage.actions
                    objectList = univers.actions
                elif type == 'hostilite':
                    personnageList = personnage.hostilites
                    objectList = univers.creatures
                objet = util.TrouverObject(objectList,re.findall('^[a-zA-Z_]*[^#]',valeur)[0])
                if objet==None: 
                    print('Objet inexistant')
                    return False
                if operateur == "+": #Alors on supprime                 
                    if objet in personnageList: #Si l'objet est dans la liste
                        personnageList.remove(objet)
                elif operateur == "-":
                    if not objet in personnageList: #Si l'objet n'est pas dans la liste
                        personnageList.append(objet)
                if type == 'action': personnage.actions = personnageList #On différencie les deux                  
                elif type == 'hostilite': personnage.hostilites = personnageList

            else:
                print("Erreur dans le type d'effet.")
          
            personnage.effets.remove(effet)  

        return personnage
    def AjoutListeEffets(personnage = Personnage(), univers = Univers(), listeEffet = [],joueur = "null"):
        '''Applique une liste d'effets.'''
        if joueur == "null":
            for effet in listeEffet:
                personnage = effets.AjoutEffet(personnage,effet,univers)
        else:
            for effet in listeEffet:
                personnage = effets.AjoutEffet(personnage,effet,univers,joueur)
        return personnage
    def SuprrListeEffets(personnage = Personnage(), univers = Univers(), listeEffet = [], joueur = "null"):
        '''Supprime une liste d'effets.'''
        if joueur == "null":
            for effet in listeEffet:
                personnage = effets.SupprEffet(personnage,effet,univers)
        else:
            for effet in listeEffet:
                personnage = effets.SupprEffet(personnage,effet,univers,joueur)
        return personnage
    def ChangementHeure(personnage = Personnage(), univers = Univers()):
        '''Retire une heure au temps restant de tous les effets actifs et annule ceux dont le temps restant est écoulé.'''
        i = 0
        while i < len(personnage.effets) and i != -1:
            newEffet = personnage.effets[i].split()
            duree = int(newEffet[1])
            duree -= 1
            if duree == 0:
                personnage = effets.SupprEffet(personnage,personnage.effets[i],univers)
                i -= 1
                continue
            newEffet[1] = str(duree)
            personnage.effets[i] = " ".join(newEffet)
            i += 1
        return personnage

class conditions:
    """Classe qui gère la vérification des conditions."""

    def VerifCondition(personnage = Personnage(), univers = Univers(), condition = ''):
        '''Vérifie une condition et retourne True si elle est validée ou False si elle n'est pas validée'''
        bool = False #Passe à True lorsqu'une condition est validée
        tabCondition = condition.split('||') #Sépare les conditions de type OU dans un tableau. 
        i = 0 #index de la condition à vérifier dans tabCondition
        while bool == False:
            condition = tabCondition[i]
            invert = False #définit si on doit inverser le résultat de la condition
            if condition[0] == '!':
                tab = condition.split()
                tab[0] = tab[0][1:]
                condition = ' '.join(tab)
                invert = True            
            prop = condition.split()[0]

            if prop in personnage.caracteristiques: #si il s'agit d'un caracteristique
                operateur = condition.split()[1]
                caract = prop
                valeur = condition.split()[2]
                if (   (operateur == '<' and personnage.caracteristiques[caract] < float(valeur)) 
                    or (operateur == '>' and personnage.caracteristiques[caract] > float(valeur)) 
                    or (operateur == '=' and personnage.caracteristiques[caract] == float(valeur))): bool = True
            elif prop == 'poss':
                idObjet = condition.split()[1]               
                for objet in personnage.inventaire:
                    if util.VerifItem(list(personnage.inventaire.keys()),idObjet,re.findall('^[a-zA-Z_]*[^#]',objet.id)[0]): 
                        bool = True
                        break
                if len(condition.split()) == 4:
                    operateur = condition.split()[2]
                    valeur = int(condition.split()[3])
                    if bool == True:
                        bool = False
                        quantite = util.CompterObjetDansInventaire(personnage.inventaire,idObjet)
                        if (   (operateur == '<' and quantite < valeur) 
                            or (operateur == '>' and quantite > valeur) 
                            or (operateur == '=' and quantite == valeur)): bool = True
            elif prop == 'equip':
                for objet in list(personnage.emplacements.values()):                 
                    if objet != "" and util.VerifItem(list(personnage.emplacements.values()),condition.split()[1],re.findall('^[a-zA-Z_]*[^#]',objet.id)[0]):
                            bool = True
                            break
            elif prop == 'etat':
                etat = condition.split()[1]
                if etat == personnage.etat: bool = True
            elif prop == 'in':
                if "," in condition.split()[1]: #Si la condition vise un emplacement précis.
                    posX = int(condition.split()[1].split(',')[0])
                    posY = int(condition.split()[1].split(',')[1])
                    if posX == personnage.positionX and posY == personnage.positionY: bool = True #Si le joueur est sur le bonne emplacement, alors on passe la condition à True.
                else: #Si la condition vise une région.
                    regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
                    if util.VerifItem(univers.regions,condition.split()[1],regionActuelle.id): bool = True #Si la région est celle dans laquelle est le joueur, alors on passe la condition à True.
            elif prop == 'quete':
                queteId = condition.split()[1]
                etat = int(condition.split()[2])
                if etat == 0: #Si la quête ne doit pas avoir été commencé (ni active ni achevée)
                    bool = True
                    for quete in personnage.quetesActives: #On vérifie la liste des quêtes actives
                        if quete.id == queteId: 
                            bool = False #Si la quête est active, on passe la condition à False
                            break
                    if queteId in personnage.quetesAchevees: bool = False #on vérifie la liste des quêtes achevées. Si la quête est achevée, on passe la condition à False.
                elif etat == 1: #Si la quête doit être active.
                    for quete in personnage.quetesActives: 
                        if quete.id == queteId: #Si la quête est dans la liste des quêtes actives,
                            bool = True  #alors on passe la condition à True.
                            break
                elif quete == 2: #Si la quête doit être achevée
                    if queteId in personnage.quetesAchevees: bool = True #Si la quête est dans liste des quêtes achevées, alors on passe la condition à true.
            elif prop == 'objectif':
                queteId = condition.split()[1]
                objectifId = condition.split()[2]
                etat = int(condition.split()[3])
                for quete in personnage.quetesActives:
                    if quete.id == queteId: #Si on parcourt la bonne quête.
                        for objectif in quete.objectifs: 
                            if objectif.id == objectifId and objectif.etat == etat: bool = True #Si l'objectif qu'on cherche est dans le bon état, alors la condition passe à vrai.
                if bool == False: #Si on a pas trouvé le bon objectif dans les quêtes actives.
                    if queteId in personnage.quetesAchevees: #Si la quête concernée a déjà été achevée
                        bool = True #Alors l'objectif a déjà été achevé.

            if invert == True: bool = not(bool) #invertion de bool si nécessaire
            if len(tabCondition) > i + 1: i+=1 #Si il reste des conditions à vérifier dans tabCondition, on continue.
            else: break #Sinon on s'arrête.

        return bool
    def VerifListConditions(personnage = Personnage(), univers = Univers(), listConditions = []):
        '''Vérifie une liste de conditions, renvoie True si toutes les conditions sont validées ou False si au moins une condition n'est pas validée.'''
        bool = True
        if len(listConditions) != 0:
            for condition in listConditions:
                if conditions.VerifCondition(personnage,univers,condition) == False: 
                    bool = False
                    break
        return bool

class interdictions:
    """Classe qui vérifie la liste des interdictions du joueur."""
    def VerifInterdiction(univers = Univers(), personnage = Personnage(),interdictionTest = ''):
        '''Renvoie True si le joueur est autorisé à faire l'action ou False si l'action lui est interdite'''      
        for interdiction in personnage.interdictions:
            typeTest = interdictionTest.split()[0]
            valeurTest = interdictionTest.split()[1]
            type = interdiction.split()[0]
            valeur = interdiction.split()[1]
            if typeTest != type: continue #Si l'interdiction testée et l'interdiction parcourue sont de types différents, on passe à l'interdiction suivante.
            if type in ['poss','unposs','equip','unequip','ramasser','jeter','utiliser'] and util.VerifItem(univers.objets,valeur,re.findall('^[a-zA-Z_]*[^#]',valeurTest)[0]): return False #Si l'interdiction vise un objet et que cet objet est celui de l'interdiction testée.
            elif type in ['entrer','sortir']: #Si l'interdiction concerne des régions.
                if "," in valeur and valeur == valeurTest: return False #Si l'interdiction vise un emplacement précis et que cet emplacement est celui de l'interdiction testée.
                region = personnage.mapUnivers[int(valeurTest.split(',')[0])][int(valeurTest.split(',')[1])]
                if util.VerifItem(univers.regions,valeur,re.findall('^[a-zA-Z_]*[^#]',region.id)[0]): return False #Si l'objet de l'interdiction testée est celui de l'interdiction parcourue ou appartient à la famille d'objets de l'interdiction parcourue.
            elif type in ['rencontrer'] and util.VerifItem(univers.creatures,valeur,re.findall('^[a-zA-Z_]*[^#]',valeurTest)[0]): return False     
        return True

class interactions:
    """Classe qui gère toutes les interactions du jeu."""
    
    def VerifRamasserObjet(personnage = Personnage(), univers = Univers(), objet = Objet()):
        '''Vérifie qu'un objet peut-être ramassé. Renvoie True si oui ou False si non.'''
        interdiction = "ramasser " + objet.id
        vInterdiction = interdictions.VerifInterdiction(univers,personnage, interdiction)
        vConditions = conditions.VerifListConditions(personnage,univers,objet.conditionsPoss)
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        obj = [obj for obj in regionActuelle.objets if obj[0] == objet][0]
        vDecouvert = obj[1][0] != 0
        poids = objet.poids
        vPoids = personnage.caracteristiques['poidsPortes'] + poids <= personnage.caracteristiques['poidsPortable']
        vSituation = personnage.enCombatAvec == [] #Si le joueur n'est pas en combat

        if vInterdiction and vConditions and vDecouvert and vPoids and vSituation: return True
        else: return False

    def RamasserObjet(personnage = Personnage(), univers = Univers(), objet = Objet()):
        '''Gère l'action de ramassage d'un objet. Supprime l'objet de la région de l'emplacement où il a été ramassé et appelle la fonction AjoutObjet(). Renvoie Personnage() ET Univers().'''
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        print(textes.TrouverTexte(univers,personnage,'ramasser '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))
        personnage = interactions.AjoutObjet(personnage,objet,univers) #On ajoute l'objet à l'inventaire.
        personnage = quetes.VerificationQuetes(univers,personnage,'ramasser '+objet.id+' '+regionActuelle.id+' '+temps.MomentJournee(personnage.heure))
        i = -1
        for objetParcouru in regionActuelle.objets: 
            i += 1
            if objetParcouru[0] != objet: continue #Si l'objet parcouru n'est pas le même que celui qu'on veut ramasser, on passe au suivant.
            if objetParcouru[1][0] == 0: continue #Si l'objet parcouru n'est pas découvert, ce n'est pas le bon objet donc on passe au suivant.
            break #L'objet est le bon donc on quitte la boucle, i étant l'index de cet objet dans la liste.
        regionActuelle.objets.pop(i) #On supprime l'objet des objets de la région.
        personnage.mapUnivers[personnage.positionX][personnage.positionY] = copy.deepcopy(regionActuelle)
        return personnage,univers

    def AjoutObjet(personnage = Personnage(), objet = Objet(), univers = Univers()):
        '''Ajoute un objet à l'inventaire et applique les effets nécessaires.'''             
        if objet in personnage.inventaire: #Si l'objet est déjà présent au moins une fois dans l'inventaire.
            personnage.inventaire[objet] += 1
        else: 
            personnage.inventaire[objet] = 1
            personnage = effets.AjoutListeEffets(personnage,univers,objet.effetsPoss)
        poids = objet.poids
        personnage.caracteristiques['poidsPortes'] += poids
        print(textes.TrouverTexte(univers,personnage,'ajout '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))
        return personnage

    def VerifJeterObjet(univers = Univers(),personnage = Personnage(), objet = Objet()):
        '''Vérifie qu'un objet peut-être retiré de l'inventaire. Renvoie True si oui ou False si non.'''
        vInterdiction = interdictions.VerifInterdiction(univers,personnage, "jeter " + objet.id)
        vSituation = personnage.enCombatAvec == [] #Si le joueur n'est pas en combat

        if vInterdiction and vSituation: return True
        else: return False

    def JeterObjet(personnage = Personnage(), univers = Univers(), objet = Objet()):
        '''Gère l'action de jet d'un objet. Ajoute l'objet dans la région de l'emplacement où il a été jeté dans l'état temporaire et appelle la fonction EnleverObjet(). Renvoie Personnage() ET Univers().'''
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        print(textes.TrouverTexte(univers,personnage,'jeter '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))
        personnage = interactions.EnleverObjet(personnage,objet,univers) #On supprime l'objet de l'inventaire.
        regionActuelle.objets.append([objet,[1,1]]) #On ajoute l'objet dans le région en tant qu'objet temporaire.
        personnage.mapUnivers[personnage.positionX][personnage.positionY] = copy.deepcopy(regionActuelle)
        return personnage,univers

    def CacherObjet(personnage = Personnage(), univers = Univers(), objet = Objet()):
        '''Gère l'action de la cache d'un objet. Ajoute l'objet dans la région de l'emplacement où il a été jeté dans l'état découvert et appelle la fonction EnleverObjet(). Renvoie Personnage() ET Univers().'''
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        personnage = interactions.EnleverObjet(personnage,objet,univers) #On supprime l'objet de l'inventaire.
        regionActuelle.objets.append([objet,[2,1]]) #On ajoute l'objet dans le région en tant qu'objet découvert.
        personnage.mapUnivers[personnage.positionX][personnage.positionY] = copy.deepcopy(regionActuelle)
        print(textes.TrouverTexte(univers,personnage,'cacher '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))
        return personnage,univers

    def EnleverObjet(personnage = Personnage(), objet = Objet(), univers = Univers()):
        '''Retire un objet de l'inventaire et supprime les effets nécessaires.'''
        if objet in personnage.inventaire:
            if personnage.inventaire[objet] == 1: 
                del personnage.inventaire[objet]
                personnage = effets.SuprrListeEffets(personnage, univers, objet.effetsPoss)
            else: personnage.inventaire[objet] -= 1          
            poids = objet.poids
            personnage.caracteristiques['poidsPortes'] -= poids 
            print(textes.TrouverTexte(univers,personnage,'enlever '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))    
        return personnage

    def VerifEquiperObjet(personnage = Personnage(), univers = Univers(), objet = Objet()):
        '''Vérifie qu'un objet peut-être équipé. Renvoie True si oui ou False si non.'''
        interdiction = "equip " + objet.id
        vInterdictions = interdictions.VerifInterdiction(univers, personnage, interdiction)
        vConditions = conditions.VerifListConditions(personnage,univers,objet.conditionsEquip)        

        if vInterdictions and vConditions: return True
        else: return False

    def EquiperObjet(personnage = Personnage(), objet = Objet(), univers = Univers()):
        '''Equipe un objet et applique les effets nécessaires. Vérifie tout de même le type et les emplacements libres.'''
        vType = objet.fonction == 1
        vInventaire = objet in personnage.inventaire
        emplacementsUtil = objet.empEquip
        emplacementLibre = util.TrouverEmplacementLibre(emplacementsUtil,personnage.emplacements)
        vEmplacements = util.TrouverEmplacementLibre(emplacementsUtil,personnage.emplacements) != ''
        if vType and vEmplacements and vInventaire:
            if personnage.inventaire[objet] == 1: del personnage.inventaire[objet] #On supprime l'objet de l'inventaire temporairement dès lors qu'il est équipé.
            else: personnage.inventaire[objet] -= 1
            personnage.emplacements[emplacementLibre] = objet
            personnage = effets.AjoutListeEffets(personnage,univers,objet.effetsEquip)
            print(textes.TrouverTexte(univers,personnage,'equiper '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))
        return personnage

    def VerifDesequiperObjet(univers = Univers(), personnage = Personnage(), objet = Objet()):
        '''Vérifie qu'un objet peut-être déséquipé. Renvoie True si oui ou False si non.'''
        vInterdiction = interdictions.VerifInterdiction(univers, personnage, "unequip " + objet.id)

        if vInterdiction: return True
        else: return False

    def DesequiperObjet(personnage = Personnage(), objet = Objet(), univers = Univers):
        '''Déséquipe un équipement et supprime les effets nécessaires.'''
        emp = util.TrouverEmplacementObjetEquipe(objet, personnage.emplacements)
        if emp != '#NULL':
            if objet in personnage.inventaire: personnage.inventaire[objet] += 1 #On réajoute l'objet dans l'inventaire 
            else: personnage.inventaire[objet] = 1
            personnage.emplacements[emp] = ''
            personnage = effets.SuprrListeEffets(personnage,univers,objet.effetsEquip)
            print(textes.TrouverTexte(univers,personnage,'desequiper '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))
        return personnage

    def VerifUtiliserObjet(univers = Univers(), personnage = Personnage(), objet = Objet()):
        '''Renvoie True si le joueur est autorisé à utiliser l'objet ou False sinon.'''
        interdiction = 'utiliser ' + objet.id
        vInterdiction = interdictions.VerifInterdiction(univers,personnage,interdiction)
        vConditions = conditions.VerifListConditions(personnage,univers,objet.conditionsUtil)
        vType = objet.fonction == 2

        if vInterdiction and vConditions and vType: return True
        else: return False

    def UtiliserObjet(univers = Univers(), personnage = Personnage(), objet = Objet()):
        '''Gère l'utilisation d'un objet. Retourne personnage.'''
        if objet.fonction == 2: #Si l'objet est bien un consommable
            personnage = effets.AjoutListeEffets(personnage,univers,objet.effetsUtil) #On ajoute les effets au personnage
            personnage = interactions.EnleverObjet(personnage,objet,univers) #On enlève (temporairement) l'objet de l'inventaire.
            objet.nbrUse -= 1 #On enlève une utilisation à l'objet
            if objet.nbrUse > 0: #S'il reste des utilisations à l'objet.
                personnage = interactions.AjoutObjet(personnage,objet,univers)
        print(textes.TrouverTexte(univers,personnage,'utiliser '+objet.id+ ' '+str(personnage.positionX) + ',' + str(personnage.positionY)+ ' '+temps.MomentJournee(personnage.heure)))
        return personnage            

    def Fouiller(univers = Univers(), personnage = Personnage(), typeFouille = 1):
        '''Gère le système de fouille d'une région. Renvoie Univers().'''
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        i = -1
        for objet in regionActuelle.objets: #On commence par parcourir les objets.
            i +=1
            if objet[1][0] != 0: continue #Si l'objet est découvert, on passe au suivant.
            probabilite = 1/((univers.reglages.maxCaract/personnage.caracteristiques[univers.reglages.caractFouille])*((-0.5*typeFouille)+2.5)*objet[1][1]) #On calcule la probabilité de trouver l'objet.
            if random() <= probabilite: #Si un nombre aléatoire entre 0 et 1 est plus petit que la probabilité alors l'objet va être découvert.
                regionActuelle.objets[i][1][0] = 2
        i = -1
        for portail in regionActuelle.portails: #On parcourt les portails.
            i +=1
            if portail[1][0] != 0: continue #Si le portail est découvert, on passe au suivant.
            probabilite = 1/((univers.reglages.maxCaract/personnage.caracteristiques[univers.reglages.caractFouille])*((-0.5*typeFouille)+2.5)*portail[1][1]) #On calcule la probabilité de trouver le portail.
            if random() <= probabilite: #Si un nombre aléatoire entre 0 et 1 est plus petit que la probabilité alors le portail va être découvert.
                regionActuelle.portails[i][1][0] = 2
        i = -1
        for creature in regionActuelle.creatures: #On parcourt les créatures.
            i +=1
            if creature[1][0] != 0: continue #Si la créature est découverte, on passe à la suivante.
            probabilite = 1/((univers.reglages.maxCaract/personnage.caracteristiques[univers.reglages.caractFouille])*((-0.5*typeFouille)+2.5)*creature[1][1]) #On calcule la probabilité de trouver la creature.
            if random() <= probabilite: #Si un nombre aléatoire entre 0 et 1 est plus petit que la probabilité alors la creature va être découverte.
                regionActuelle.creatures[i][1][0] = 2
                break
        return personnage

    def VerifFaireOffre(univers = Univers(), personnage = Personnage(), listeAchat = [], listeVente = []):
        '''Détermine si un pnj peut accepter une offre. Renvoie True si oui ou False si non.'''
        valeurAchat = 0.0
        for element in listeAchat: valeurAchat += element.prixAchat #On détermine la valeur de l'ensemble d'objet que l'on veut acheter.
        valeurVente = 0.0
        for element in listeVente: valeurVente += element.prixVente #On détermine la valeur de l'ensemble d'objet que l'on veut vendre.
        if valeurAchat <= valeurVente: return True #Si l'offre est rentable pour le pnj, alors celui-ci accepte l'offre.
        else: return False

    def VerifNegocier(univers = Univers(), personnage = Personnage(), listeAchat = [], listeVente = []):
        '''Détermine si un pnj est en mesure accepter une offre négociée. Renvoie True si oui ou False si non.'''
        valeurAchat = 0.0
        for element in listeAchat: valeurAchat += element.prixAchat #On détermine la valeur de l'ensemble d'objet que l'on veut acheter.
        valeurVente = 0.0
        for element in listeVente: valeurVente += element.prixVente #On détermine la valeur de l'ensemble d'objet que l'on veut vendre.
        moyenneCaract = ((personnage.caracteristiques[univers.reglages.caractNegociation1]/univers.reglages.maxCaract*20)+(personnage.caracteristiques[univers.reglages.caractNegociation2]/univers.reglages.maxCaract*20))/2
        r = Random()
        lancerDes = r.randint(1,univers.reglages.maxCaract)
        if lancerDes <= moyenneCaract and lancerDes >= (valeurAchat-valeurVente)/valeurAchat*100: return True #Si le jet est réussi et si il est plus petit que le % de la réduction du prix de vente sur le prix d'achat, alors le vendeur accepte l'offre.
        else : return False
    
    def JetFuite(univers = Univers(), listeCreatures = [], creature = Creature()):
        '''Retourne True si la créature réussit à fuire ou False sinon.'''
        fuite = True
        i = 0
        while i < len(creature.enCombatAvec):
            if randint(1,univers.reglages.maxCaract) > creature.caracteristiques[univers.reglages.caractFuite] - util.TrouverObject(listeCreatures,creature.enCombatAvec[i]).malusFuite: fuite = False #Si le jet est raté, alors la fuite est impossible.
            i += 1
            if fuite == False: break
        return fuite

    def FuiteJoueur(univers = Univers(), personnage = Personnage(), direction = ''):
        '''Gère la fuite du joueur. Retourne univers, personnage et listeCreatures.'''
        #for crea in listeCreatures:
         #   if personnage.id in crea.enCombatAvec: listeCreatures[listeCreatures.index(crea)].enCombatAvec.remove(personnage.id) --Si le joueur est dans la liste des cibles d'une autre créature, alors on l'y enlève.
        for creature in personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures:
            if creature[0].id == personnage.id:
                personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures.remove(creature) #On supprime le joueur de la liste des créatures de la région.
                break
        personnage.enCombatAvec = []
        print(textes.TrouverTexte(univers,personnage,"fuite "+"!PLAYER "+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'auteur':personnage.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
        univers,personnage = deplacements.Deplacement(univers,personnage,direction,0)
        return univers,personnage

    def FuiteCreature(univers = Univers(), personnage = Personnage(), creature = Creature(), listeCreatures = []):
        '''Gère la fuite d'une créature. Retourne univers et listeCreatures.'''
        region = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        direcUtil = False
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
        direction = ''
        while direcUtil == False: #Tant qu'on a pas trouvé de direction utilisable.
            nbrAleat = randint(0,7) 
            direction = directions[nbrAleat] #On prend une direction au hasard grâce au nombre aléatoire.
            if str(region.directionUtil)[nbrAleat] == '1': direcUtil = True #Si la direction aléatoire est utilisable, alors on la garde.
        for crea in listeCreatures:
            if creature.id in crea.enCombatAvec: listeCreatures[listeCreatures.index(crea)].enCombatAvec.remove(creature.id) #Si la créature est dans la liste des cibles d'une autre créature, alors on l'y enlève.
        listeCreatures.remove(creature) #On supprime la créature de la liste des créatures.
        for crea in region.creatures:
            if crea[0].id == creature.id: region.creatures.remove(crea) #On supprime la créature de la région.
        personnage.mapUnivers[personnage.positionX][personnage.positionY] = copy.deepcopy(region) #On remplace la précédent région par la nouvelle dans la map.
        creature.cible = '' #On enlève la cible de la créature.
        creature.enCombatAvec = [] #On vide la liste des cible de la créature.
        regionFuture = util.TrouverFutureRegion(personnage.mapUnivers,personnage.positionX,personnage.positionY,direction)
        regionFuture.creatures.append([creature,[1,1]]) #On ajoute la créature à la future région.
        personnage.mapUnivers[util.TrouverX(personnage.positionX,direction)][util.TrouverY(personnage.positionY,direction)] = regionFuture #On remplace la précédente future région région par la nouvelle dans la map.
        print(textes.TrouverTexte(univers,personnage,'fuite %s %s %s'%(re.findall('^[a-zA-Z_]*[^#]',creature.id)[0],str(personnage.positionX) + ',' + str(personnage.positionY),temps.MomentJournee(personnage.heure)),{'auteur':creature.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
        return univers, listeCreatures

    def DepouillerCreature(univers = Univers(), personnage = Personnage(), idCreature = '', idObjet = ''):
        '''Gère la fouille d'une créature. Enlève l'objet du cadavre de la créature en question et l'ajoute dans l'inventaire du joueur. Retourne univers,personnage.'''
        region = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        for creature in region.creatures:
            if creature[0].id == idCreature: #Si on parcourt la bonne créature.
                try : objet = [obj for obj in creature[0].inventaire if obj.id == idObjet][0]
                except IndexError:
                    print(textes.TrouverTexte(univers,personnage,'erreur objet_non_trouvable_depouille'))
                    break
                interdiction = "ramasser " + objet.id
                vInterdiction = interdictions.VerifInterdiction(univers,personnage, interdiction)
                vConditions = conditions.VerifListConditions(personnage,univers,objet.conditionsPoss)
                vMort = creature[1][0] == 2
                poids = objet.poids
                vPoids = personnage.caracteristiques['poidsPortes'] + poids <= personnage.caracteristiques['poidsPortable']
                vSituation = personnage.enCombatAvec == [] #Si le joueur n'est pas en combat
                if vInterdiction and vConditions and vMort and vPoids and vSituation: #Si le joueur est autorisé à ramasser l'objet.
                    personnage = interactions.AjoutObjet(personnage,objet,univers)  #On l'ajoute à son inventaire.
                    region.creatures[region.creatures.index(creature)][0].inventaire.remove(objet) #On supprime l'objet de l'inventaire de la créature.
                break
        return personnage
       
class combat:
    """Classe qui contient toutes les méthodes concernant le combat et l'ia."""
    def Tour(univers = Univers(), personnage = Personnage()):
        '''Gère le déroulement d'un tour.'''
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        listeCreaturesDecouvertes = []
        for creature in regionActuelle.creatures:
            if creature[1][0] == 1: listeCreaturesDecouvertes.append(creature[0]) #Si la créature est découverte on l'ajoute à la liste
        listeCreaturesDecouvertes.append(personnage) #On ajoute le joueur à la liste
        listeCreatures = sorted(listeCreaturesDecouvertes,key=lambda crea:crea.caracteristiques[univers.reglages.caractInitiative]) #On ordonne la liste selon le courage des créatures. Cet ordre correspond à l'ordre dans lequel les créatures vont jouer.
        save = True
        i = 0 
        while i < len(listeCreatures): #On parcourt la liste des Creatures
            print('Au tour de : %s'%(listeCreatures[i].nom))
            time.sleep(1)           
            for creaHostil in personnage.hostilites:
                if util.VerifItem(listeCreatures,creaHostil,re.findall('^[a-zA-Z_]*[^#]',listeCreatures[i].id)[0]): #Si la créature est dans la liste des hostilités du joueur:
                    listeCreatures[i].hostil = 6 #On passe son hostilité à hostil
                    break
            if listeCreatures[i].id == personnage.id: 
                stop = False
                entree = ""
                while stop == False:
                    entree = input("cmd: ")
                    if entree.split()[0] in ['attaquer','fuir']: stop = True
                    univers,personnage = console.ExecuterCommande(univers,personnage,entree)
                if entree.split()[0] == "fuir": 
                    save = False
                    break
            elif listeCreatures[i].hostil == 0: #Si la créature est très farouche.
                listeCreatures[i].enCombatAvec.append(personnage.id) #On ajoute quand même le joueur à cette liste pour rendre la fuite plus difficile.
                if interactions.JetFuite(univers,listeCreatures,listeCreatures[i]): #elle tente une fuite.
                    univers,listeCreatures = interactions.FuiteCreature(univers,personnage,listeCreatures[i],listeCreatures)
                    i -= 1
                else: print(textes.TrouverTexte(univers,personnage,"fuite_echec "+re.findall('^[a-zA-Z_]*[^#]',listeCreatures[i].id)[0]+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom,'auteur':listeCreatures[i].nom}))
            elif listeCreatures[i].hostil == 1 and util.CombatDansLaZone(listeCreatures): #Si la créature est farouche.
                listeCreatures[i].enCombatAvec.append(personnage.id) 
                if interactions.JetFuite(univers,listeCreatures,listeCreatures[i]): #Si il y a un combat dans la zone, elle tente une fuite.
                    univers,listeCreatures = interactions.FuiteCreature(univers,personnage,listeCreatures[i],listeCreatures)
                    i -= 1
                else: print(textes.TrouverTexte(univers,personnage,"fuite_echec "+re.findall('^[a-zA-Z_]*[^#]',listeCreatures[i].id)[0]+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom,'auteur':listeCreatures[i].nom}))
            elif listeCreatures[i].hostil == 2 and listeCreatures[i].enCombatAvec != []: #Si la créature est peureuse.
                if interactions.JetFuite(univers,listeCreatures,listeCreatures[i]): #Si elle est attaquée, elle tente une fuite.
                    univers,listeCreatures = interactions.FuiteCreature(univers,personnage,listeCreatures[i],listeCreatures)
                    i -= 1
                else: print(textes.TrouverTexte(univers,personnage,"fuite_echec "+re.findall('^[a-zA-Z_]*[^#]',listeCreatures[i].id)[0]+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom,'auteur':listeCreatures[i].nom}))
            elif listeCreatures[i].hostil == 4 and listeCreatures[i].enCombatAvec != []: #Si la créature est neutre et qu'elle est attaquée, elle riposte.
                crea = listeCreatures[i].id #On stocke l'id de la créature qu'on parcours.
                univers,personnage,listeCreatures = combat.Combat(univers,personnage,listeCreatures,listeCreatures[i]) 
                while listeCreatures[i].id != crea: i -= 1 #On compare ensuite l'ancienne créature parcourue avec la nouvelle et on adapte i pour revenir sur la bonne créature.
            elif listeCreatures[i].hostil == 5: #Si la créature est défenseur.
                listeAmis = [] #On créait une liste d'amis qui contiendra les créatures que la créature veut défendre.
                for crea in listeCreatures:
                    if listeCreatures.index(crea) == i: continue
                    for id in listeCreatures[i].amisAvec:
                        if util.VerifItem(listeCreatures,id,crea.id): listeAmis.append(crea)
                if len(listeAmis) == 1: listeCreatures[i].enCombatAvec += listeAmis[0].enCombatAvec #Si la créature a un seul 'amis' dans la zone, elle le défendra.
                elif len(listeAmis) > 1: #Si la créature a plusieurs amis dans la zone
                    for amis in listeCreatures[i].amisAvec:
                        for crea in listeCreatures:
                            if listeCreatures.index(crea) == i: continue #Si on parcourt la même créature, on passe à la suivante.
                            if util.VerifItem(listeCreatures,amis,crea.id): listeCreatures[i].enCombatAvec += crea.enCombatAvec #alors la créature défendra les créatures en fonction de leur placement dans sa "liste d'amis".
                if listeCreatures[i].enCombatAvec != []: #Si la créature a des ennemis, elle les attaque.
                    crea = listeCreatures[i].id #On stocke l'id de la créature qu'on parcours.
                    univers,personnage,listeCreatures = combat.Combat(univers,personnage,listeCreatures,listeCreatures[i]) 
                    while listeCreatures[i].id != crea: i -= 1 #On compare ensuite l'ancienne créature parcourue avec la nouvelle et on adapte i pour revenir sur la bonne créature.
            elif listeCreatures[i].hostil == 6: #Si la créature est hostile.
                if not personnage.id in listeCreatures[i].enCombatAvec: 
                    listeCreatures[i].enCombatAvec.append(personnage.id) #Si le joueur n'est pas dans la liste des cibles de la créature, alors on l'y ajoute.
                if not listeCreatures[i].id in personnage.enCombatAvec:
                    personnage.enCombatAvec.append(listeCreatures[i].id) #Si la créature n'est pas dans la liste des cibles du joueur, on on l'y ajoute.
                crea = listeCreatures[i].id #On stocke l'id de la créature qu'on parcours.
                univers,personnage,listeCreatures = combat.Combat(univers,personnage,listeCreatures,listeCreatures[i]) 
                while listeCreatures[i].id != crea: i -= 1 #On compare ensuite l'ancienne créature parcourue avec la nouvelle et on adapte i pour revenir sur la bonne créature.
            elif listeCreatures[i].hostil == 7: #Si la créature est agressive.
                for crea in listeCreatures:
                    if listeCreatures.index(crea) == i: continue
                    if not crea.id in listeCreatures[i].enCombatAvec and not re.findall('^[a-zA-Z_]*[^#]',crea.id)[0] in listeCreatures[i].amisAvec: 
                        listeCreatures[i].enCombatAvec.append(crea.id) #Si une créature n'est pas dans la liste des cibles de la créature et qu'elle n'est pas amis avec cette créature, alors on l'y ajoute.
                    if not listeCreatures[i].id  in listeCreatures[listeCreatures.index(crea)].enCombatAvec:
                        listeCreatures[listeCreatures.index(crea)].enCombatAvec.append(listeCreatures[i].id) #Si une créature n'est pas en combat avec la créature parcourue alors on ajoute également la créature dans la liste des cibles de la créature parcourue qui n'était pas dans celle de la créature.
                crea = listeCreatures[i].id #On stocke l'id de la créature qu'on parcours.
                univers,personnage,listeCreatures = combat.Combat(univers,personnage,listeCreatures,listeCreatures[i]) 
                while listeCreatures[i].id != crea: i -= 1 #On compare ensuite l'ancienne créature parcourue avec la nouvelle et on adapte i pour revenir sur la bonne créature.
            i+=1
        if save == True:
            region = personnage.mapUnivers[personnage.positionX][personnage.positionY]
            for creature in listeCreatures:
                if creature.id == personnage.id: continue #Si la créature est le joueur, on passe à la suivante.
                for crea in region.creatures:
                    if crea[0].id == creature.id: region.creatures[region.creatures.index(crea)][0] = creature #On actualise les créatures de la région.
            personnage.mapUnivers[personnage.positionX][personnage.positionY] = copy.deepcopy(region)
        return personnage
    def Combat(univers = Univers(), personnage = Personnage(), listeCreatures = [], creature = Creature()):
        '''Gère le déroulement d'un combat. Retourne univers,personnage,listeCreatures.'''
        sortie = False
        while sortie == False:
            if creature.sortIncant == '': #Si la créature n'est pas déjà entrain d'incanter un autre sort.
                listeSoins = []
                for action in creature.actions:
                    if action.type == 1 and action.cible == 0 and action.util != 1 and conditions.VerifListConditions(creature,univers,action.conditions): listeSoins.append(action) #Si l'action respecte tous les critères alors on l'ajoute à la liste des soins utilisables.
                listeAttaques = []
                for action in creature.actions:
                    if action.type == 0 and action.cible == 1 and action.util != 1 and conditions.VerifListConditions(creature,univers,action.conditions): listeAttaques.append(action) #Si l'action respecte tous les critères alors on l'ajoute à la liste des soins utilisables.
                pourcentageVie = creature.caracteristiques['pv']*100/creature.caracteristiques['pvBase']
                if creature.strategieDefensive == 0 or (creature.strategieDefensive == 1 and pourcentageVie > 20) or (creature.strategieDefensive == 2 and pourcentageVie > 50) or (creature.strategieDefensive == 3 and pourcentageVie == 100) or (creature.strategieDefensive >= 1 and len(listeSoins) == 0): #Si la stratégie défensive est le sacrifice, si elle est protectrice et qu'il reste plus de 20% de pv à la créature ou si elle est protectrice et qu'aucuns sorts de soins n'est utilisable
                    if listeAttaques != []: #Si la créature possède bien des attaques
                        attaque = listeAttaques[randint(0,len(listeAttaques)-1)] #On sélectionne une attaque au hasard dans la liste.
                        creature = combat.SelectionCible(listeCreatures,creature) #alors on sélectionne une cible.
                        cibleId = re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0]
                        if re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0] == personnage.id: #Si la cible de l'attaque est le joueur
                            cibleId = '!PLAYER'
                            cibleNom = personnage.nom
                        if not re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0] == personnage.id: cibleNom = util.TrouverObject(univers.creatures,re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0]).nom #Si la créature attaquée n'est pas le joueur, alors on peut récupérer son nom.
                        if (attaque.ratable == True and randint(1,univers.reglages.maxCaract) <= creature.caracteristiques[univers.reglages.caractAttaque]) or attaque.ratable ==  False: #Si l'action est ratable et le jet d'attaque est réussi ou si l'action est inratable.
                            if attaque.tIncant == 0: #Si l'attaque n'a pas de temps d'incantation
                                print(textes.TrouverTexte(univers,personnage,'action '+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+' '+cibleId+' '+attaque.id+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'auteur':creature.nom,'cible':cibleNom,'action':attaque.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
                                univers,personnage,listeCreatures = combat.Attaque(univers,personnage,listeCreatures,creature.cible,attaque)
                            elif attaque.tIncant > 0: #Si l'ataque a un temps d'incantation
                                print(textes.TrouverTexte(univers,personnage,"incantation %s %s %s %s %s"%(re.findall('^[a-zA-Z_]*[^#]',creature.id)[0],cibleId,attaque.id,str(personnage.positionX) + ',' + str(personnage.positionY),temps.MomentJournee(personnage.heure)),{'auteur':creature.nom,'cible':cibleNom,'action':attaque.nom,'duree':attaque.tIncant,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
                                creature.tIncantRestant = attaque.tIncant
                                creature.sortIncant = attaque
                        else: #Si l'action est ratée
                            print(textes.TrouverTexte(univers,personnage,'action_ratee '+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+' '+cibleId+' '+attaque.id+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'auteur':creature.nom,'cible':cibleNom,'action':attaque.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
                elif creature.strategieDefensive >= 1: #Si la stratégie défensive est protectrice
                    if listeSoins != []: #Si la créature possède bien des soins
                        soin = listeSoins[randint(0,len(listeSoins)-1)] #On sélectionne un soin au hasard dans la liste.
                        if (soin.ratable == True and randint(1,univers.reglages.maxCaract) <= creature.caracteristiques[univers.reglages.caractSoin]) or soin.ratable ==  False: #Si l'action est ratable et le jet d'attaque est réussi ou si l'action est inratable.
                            if soin.tIncant == 0: #Si le soin n'a pas de temps d'incantation:
                                print(textes.TrouverTexte(univers,personnage,'action '+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+' '+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+' '+soin.id+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'auteur':creature.nom,'cible':creature.nom,'action':soin.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
                                creature = effets.AjoutListeEffets(creature,univers,soin.effets,personnage) #On applique directement ses effets sur la créature.
                            elif soin.tIncant > 0: #Si le soin a un temps d'incantation:
                                creature.tIncantRestant = soin.tIncant
                                creature.sortIncant = soin
                        else: #Si le soin est ratée
                            print(textes.TrouverTexte(univers,personnage,'action_ratee '+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+' '+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+' '+soin.id+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'auteur':creature.nom,'cible':creature.nom,'action':soin.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
                sortie = True
            elif creature.sortIncant != '': #Si la créature est entrain d'incanter un sort.
                creature.tIncantRestant -= 1 #On enlève un tour au temps d'incantation restant.
                if creature.tIncantRestant == 0: #Si le temps d'incantation est écoulé.
                    
                    if creature.sortIncant.cible == 0: #Si le sort vise le lanceur (un buff ou un soin).
                        creature = effets.AjoutListeEffets(creature,univers,creature.sortIncant.effets,personnage) #On applique directement ses effets sur la créature.
                        creature.tIncantRestant = 0
                        creature.sortIncant = ''
                    elif creature.sortIncant.cible == 1 and creature.cible in [crea.id for crea in listeCreatures]: #Si le sort cible une autre créature et que cette cible est toujours présente
                        cibleId = re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0]
                        if re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0] == personnage.id: #Si la cible de l'attaque est le joueur
                            cibleId = '!PLAYER'
                            cibleNom = personnage.nom
                        if not re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0] == personnage.id: cibleNom = util.TrouverObject(univers.creatures,re.findall('^[a-zA-Z_]*[^#]',creature.cible)[0]).nom #Si la créature attaquée n'est pas le joueur, alors on peut récupérer son nom.
                        print(textes.TrouverTexte(univers,personnage,'action '+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+' '+cibleId+' '+creature.sortIncant.id+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'auteur':creature.nom,'cible':cibleNom,'action':creature.sortIncant.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
                        univers,personnage,listeCreatures = combat.Attaque(univers,personnage,listeCreatures,creature.cible,creature.sortIncant)
                        creature.tIncantRestant = 0
                        creature.sortIncant = ''                    
                    elif not creature.cible in [crea.id for crea in listeCreatures]: #Si la créature n'est plus présente
                        creature.tIncantRestant = 0
                        creature.cible = ''
                        creature.sortIncant = ''
                        continue #alors on permet à la créature d'attaquer ce tour là.
                    creature.sortIncant = ''
                elif creature.tIncantRestant > 0: #Si le temps d'incantation n'est pas écoulé.
                    pourcentageVie = creature.caracteristiques['pv']*100/creature.caracteristiques['pvBase']
                    if creature.sortIncant.cible == 1 and not creature.cible in [crea.id for crea in listeCreatures]: #Si le sort cible une créature qui n'est plus présente.
                        creature.tIncantRestant = 0
                        creature.cible = ''
                        creature.sortIncant = ''
                        continue #alors on permet à la créature d'attaquer ce tour là.                   
                    elif creature.sortIncant.type == 0 and creature.rompreIncant and ((creature.strategieDefensive == 1 and pourcentageVie < 20) or (creature.strategieDefensive == 2 and pourcentageVie < 50) or (creature.strategieDefensive == 3 and pourcentageVie != 100)): #Si la créature est entrain d'incanter une attaque, si elle est autorisée à rompre une incantation et si ses pv passent en dessous du seuil de sa stratégie défensive permettant l'attaque, alors on romp l'incantation pour qu'elle puisse soigner.
                        creature.tIncantRestant = 0
                        creature.sortIncant = ''
                        continue #alors on permet à la créature d'attaquer ce tour là.
                sortie = True
        for crea in listeCreatures:
            if crea.id == creature.id: listeCreatures[listeCreatures.index(crea)] = creature #On actualise la créature ans la liste des créatures.
        return univers,personnage,listeCreatures

    def SelectionCible(listeCreatures = [], creature = Creature()):
        '''Sélectionne une cible que va attaquer la créature. Retourne creature.'''
        if len(creature.enCombatAvec) == 1: #Si la créature a un seul ennemi.
            creature.cible = creature.enCombatAvec[0]
        elif len(creature.enCombatAvec) > 1: #Si la créature a plus d'un ennemi.
            if creature.cible == '' or creature.strategieOffensive == 3: #Si la créature n'a pas de cible ou sa stratégie offensive est hasardeuse.
                if creature.strategieOffensive == 0: #Si la stratégie offensive de la créature est lâche.
                    liste = []
                    for crea in listeCreatures:
                        if crea.id in creature.enCombatAvec:
                            liste.append(crea) #On ajoute les créatures (objet) avec lesquelles la créature est en combat dans la liste.
                    creature.cible = sorted(liste,key=lambda crea:crea.caracteristiques['pv'])[0].id #La cible est la première créature d'une liste triée en fonction des pv dans l'ordre croissant, donc celle avec le moins de pv.
                if creature.strategieOffensive == 1: #Si la stratégie offensive de la créature est honorable.
                    liste = []
                    for crea in listeCreatures:
                        if crea.id in creature.enCombatAvec:
                            liste.append(crea) #On ajoute les créatures (objet) avec lesquelles la créature est en combat dans la liste.
                    creature.cible = sorted(liste,key=lambda crea:crea.caracteristiques['pv'])[-1].id #La cible est la dernière créature d'une liste triée en fonction des pv dans l'ordre croissant, donc celle avec le plus de pv.
                if creature.strategieOffensive == 2 or creature.strategieOffensive == 3: #Si la stratégie offensive de la créature est ciblée ou hasardeuse.
                    creature.cible = creature.enCombatAvec[randint(0,len(creature.enCombatAvec)-1)] #alors on choisit une cible au hasard dans liste des ennemis de la créature.
        return creature

    def Attaque(univers = Univers(), personnage = Personnage(), listeCreatures = [], creature = Creature(), attaque = Action()):
        '''Applique les effets d'une attaque sur une cible et gère sa mort. Retourne univers, personnage, listeCreatures.'''
        creature = [crea for crea in listeCreatures if crea.id == creature][0]
        esquive = False
        if univers.reglages.autoriserEsquive == True and attaque.esquive == True: #Si l'esquive est autorisée dans l'univers et sur cette attaque.
            if randint(1,univers.reglages.maxCaract) <= creature.caracteristiques[univers.reglages.caractEsquive]: 
                esquive = True #Si le jet esquive est réussi, alors le joueur va esquiver l'attaque.
                cibleEsquive = ''
                if personnage.id == creature.id: cibleEsquive = '!PLAYER' #Si la créature est le joueur, alors on le précise lors de la recherche du texte.
                else: cibleEsquive = re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]
                print(textes.TrouverTexte(univers,personnage,'esquive '+cibleEsquive+' '+attaque.id+' '+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'cible':creature.nom,'action':attaque.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
        if esquive == False: creature = effets.AjoutListeEffets(creature,univers,attaque.effets,personnage) #Si l'esquive est râtée ou inutilisable, la créature reçoit les effets.
        if creature.caracteristiques['pv'] <= 0: #Si la créature n'a plus de points de vie.
            if creature.id != personnage.id: #Si la créature n'est pas le joueur.
                for crea in listeCreatures:
                    if creature.id in crea.enCombatAvec: listeCreatures[listeCreatures.index(crea)].enCombatAvec.remove(creature.id) #Si la créature est dans la liste des cibles d'une autre créature, alors on l'y enlève.
                    if crea.id != personnage.id: 
                        if creature.id in crea.cible: listeCreatures[listeCreatures.index(crea)].cible = "" #Si la créature est la cible d'une autre, alors on remet la cible à 0.
                listeCreatures.remove(creature) #On supprime la créature de la liste des créatures.
                for crea in personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures:
                    if crea[0].id == creature.id: personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures[personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures.index(crea)][1][0] = 2 #On indique que la créature est morte dans la liste des créatures de la région.
                print(textes.TrouverTexte(univers,personnage,"mort "+re.findall('^[a-zA-Z_]*[^#]',creature.id)[0]+" "+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'cible':creature.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
            elif creature.id == personnage.id: #Si la créature est le joueur.
                for crea in listeCreatures:
                    if creature.id in crea.enCombatAvec: listeCreatures[listeCreatures.index(crea)].enCombatAvec.remove(creature.id) #Si la créature est dans la liste des cibles d'une autre créature, alors on l'y enlève.
                    if crea.id != personnage.id: 
                        if creature.id in crea.cible: listeCreatures[listeCreatures.index(crea)].cible = "" #Si la créature est la cible d'une autre, alors on remet la cible à 0.
                listeCreatures.remove(creature) #On supprime la créature de la liste des créatures.
                print(textes.TrouverTexte(univers,personnage,"mort "+"!PLAYER"+" "+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'cible':personnage.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))
                sys.exit()
        elif creature.caracteristiques['pv'] > 0: #Si la créature a encore des points de vie.
            for crea in listeCreatures:
                if crea.id == creature.id: listeCreatures[listeCreatures.index(crea)] = creature #On actualise la créature dans la liste des creatures.
        return univers, personnage, listeCreatures

class deplacements:
    '''Classe qui gère le déplacement du personnage.'''
    def CalculMalusDeplacement(personnage = Personnage(), mode = ""):
        '''Retourne le malus total de déplacements du à la fatigue et au poids.'''
        if mode == "absolu":
            return (personnage.caracteristiques['poidsPortes']/personnage.caracteristiques['poidsPortable']*1.5) + personnage.fatigue/50
        if mode == "relatif":
            return ((personnage.caracteristiques['poidsPortes']/personnage.caracteristiques['poidsPortable']*20)*personnage.caracteristiques['vitesse']/100) + ((personnage.fatigue/100*40)*personnage.caracteristiques['vitesse']/100)
    def CalculVitesseReel(personnage = Personnage(), malusDeplacement = 0, region = Region()):
        '''Calcul la vitesse réelle du personnage en prenant en compte les malus de déplacements et le facteur de déplacement de la région dans laquelle il se trouve.'''
        return (personnage.caracteristiques['vitesse'] - malusDeplacement)*region.facteurDep
    def CalculDistanceParcourable(vitesseReel = 0, temps = 0):
        '''Calcul la distance que peut parcourir le personnage en x heures à vitesse réelle.'''
        return vitesseReel * temps
    def CalculTempsParRegion(vitesseReel):
        '''Calcul le temps nécessaire en heure pour faire 1km.'''
        return 60/vitesseReel/60
    def CalculMalusFatigue(temps):
        '''Retourne le malus à la fatigue en fonction du temps pour parcourir une zone.'''
        return temps*4
    def VerifSortir(personnage = Personnage(), region = Region(), univers = Univers(), direction = ""):
        '''Renvoie True si le personnage est autorisé à sortir de la zone en question ou False s'il ne l'est pas.'''
        interdiction = "sortir " + str(personnage.positionX) + "," + str(personnage.positionY)
        vInterdiction = interdictions.VerifInterdiction(univers,personnage,interdiction)
        directionsUtil = region.directionUtil
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
        vDirection = directionsUtil[directions.index(direction)] == '1' #Vérification qu'on peut emprunter cette direction dans cette zone
        vConditions = conditions.VerifListConditions(personnage,univers,region.conditionsSortir)
        if vInterdiction and vDirection and vConditions: return True
        else: return False
    def VerifEntrer(personnage = Personnage(), region = Region(), univers = Univers(), direction = ""):
        '''Renvoie True si le personnage est autorisé à entrer dans la zone en question ou False s'il ne l'est pas.'''
        interdiction = "entrer " + str(util.TrouverX(personnage.positionX,direction)) + "," + str(util.TrouverY(personnage.positionY,direction))
        vInterdiction = interdictions.VerifInterdiction(univers,personnage,interdiction)
        vConditions = conditions.VerifListConditions(personnage,univers,region.conditionsEntrer)
        if vInterdiction and vConditions: return True
        else: return False
    def VerificationsDeplacement(personnage = Personnage(), univers = Univers(), regionActuelle = Region(), regionFuture = Region(), direction = ""):
        '''Vérifie qu'un joueur peut effectuer un déplacement d'une zone à une autre.'''
        if regionFuture != "OUT": #Si on ne s'apprète pas à sortir de la carte.
                vSortir = deplacements.VerifSortir(personnage,regionActuelle,univers,direction)
                vEntrer = deplacements.VerifEntrer(personnage,regionFuture,univers,direction)
                if regionActuelle.id == regionFuture.id or regionActuelle.regionParent == regionFuture.id: #Si on ne change pas de région ou si on passe d'une région enfant à une région parent, alors on ne change pas de région.
                    vSortir = True
                    vEntrer = True
                if vSortir and vEntrer: return True
                else: return False
    def ChangementZone(univers = Univers(), personnage = Personnage(),regionActuelle = Region(), regionFuture = Region(), X = 0, Y = 0):
        '''Change le personnage de zone. Change les coordonnées et applique les effets nécessaires. Retourne personnage (objet)'''
        changementRegion = not(regionActuelle.id == regionFuture.id or regionActuelle.regionParent == regionFuture.id)
        if changementRegion: personnage = effets.SuprrListeEffets(personnage,univers,regionActuelle.effets) #Supprime les effets de la précédente zone
        for creature in regionActuelle.creatures:
            if creature[1][0] == 2: regionActuelle.creatures.remove(creature) #Si une créature est à l'état de cadavre, alors on la supprime.
        for objet in regionActuelle.objets:
            if objet[1][0] == 1: regionActuelle.objets.remove(objet) #Si un objet est temporaire, alors on le supprime.
        personnage.mapUnivers[personnage.positionX][personnage.positionY] = copy.deepcopy(regionActuelle)
        personnage.positionX = X #Attribue les nouveaux coordonnées
        personnage.positionY = Y # ""
        if changementRegion: personnage = effets.AjoutListeEffets(personnage,univers,regionFuture.effets) #Ajoute les effets de la zone cible
        return univers,personnage
    def TestDeRencontre(temps,frequenceRencontre):
        '''Test si le joueur doit rencontrer une créature en fonction du temps en h qu'il a mis pour parcourir le km. Retourne True si oui ou False si non.'''
        frequence = temps/frequenceRencontre
        if frequence >= random(): return True
        else: return False
    def ChoisirCreature(univers = Univers(), personnage = Personnage(),listeCreaturesRencontrables = [], rencontreParNiveau = True):
        '''Retourne une créature que le joueur rencontre après avoir fait plusieurs vérifications.'''
        creaturesRencontrables = []

        for creature in listeCreaturesRencontrables:
            
            interdiction = "rencontrer " + creature
            vInterdiction = interdictions.VerifInterdiction(univers,personnage,interdiction)
            
            if creature[0]=="#" and vInterdiction: 
                liste = util.TrouverObjects(univers.creatures,creature)
                for crea in liste: listeCreaturesRencontrables.append(crea.id)
                pass         
            
            creature = util.TrouverObject(univers.creatures,creature)
            
            vNiveau = True
            if rencontreParNiveau == True:
                if personnage.niveau < creature.niveau: vNiveau = False
            if vInterdiction and vNiveau:
                creaturesRencontrables.append(creature) #si la créature est rencontrable, on l'ajoute à la liste
        if creaturesRencontrables:
            i = randint(0,len(creaturesRencontrables)-1)
            return creaturesRencontrables[i]
        else: return "NULL"
    def Deplacement(univers = Univers(),personnage = Personnage(),direction = "", tempsDep = 0):
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        malusDeplacement = deplacements.CalculMalusDeplacement(personnage,univers.reglages.modeCalculMalusDeplacement)
        vitesseReel = deplacements.CalculVitesseReel(personnage,malusDeplacement,regionActuelle)
        distanceParcourable = deplacements.CalculDistanceParcourable(vitesseReel,tempsDep) #Calcul de la distance parcourable
        distanceUneZone = 1.0 
        if direction == 'NE' or direction == 'SE' or direction == 'SO' or direction == 'NO': distanceUneZone = 1.4 #Diagonale d'un carré plus longue qu'un côté donc les directions diagonales sont plus longues
        if (distanceParcourable >= distanceUneZone) or tempsDep == 0: #Si on peut parcourir plus d'une zone
            regionFuture = util.TrouverFutureRegion(personnage.mapUnivers,personnage.positionX,personnage.positionY,direction)
            if regionFuture == 'OUT': return univers,personnage
            changementRegion = True
            if (regionActuelle.id == regionFuture.id) or (regionActuelle.regionParent == regionFuture.id): changementRegion = False #Si on ne change pas de région ou si on passe d'une région enfant à une région parent, alors on ne change pas de région.
            if deplacements.VerificationsDeplacement(personnage,univers,regionActuelle,regionFuture,direction): #Si les vérifications sont ok
                tempsUneZone = deplacements.CalculTempsParRegion(vitesseReel)
                malus = deplacements.CalculMalusFatigue(tempsUneZone)
                personnage.fatigue += malus #Ajout de la fatigue
                personnage = temps.ModifierHeure(personnage,univers,tempsUneZone)
                univers,personnage = deplacements.ChangementZone(univers,personnage,regionActuelle,regionFuture,util.TrouverX(personnage.positionX,direction),util.TrouverY(personnage.positionY,direction)) #Changement de zone 
                regionActuelle = regionFuture
                print(textes.TrouverTexte(univers,personnage,'aller '+direction,{'direction':direction}))
                time.sleep(1)
                if changementRegion == True: 
                    print(textes.TrouverTexte(univers,personnage,'entrer '+str(personnage.positionX) + ',' + str(personnage.positionY) + ' ' + temps.MomentJournee(personnage.heure))) #Si on change de région on affiche le texte d'entrée dans la nouvelle région. 
                    time.sleep(1)
                txt = textes.TrouverTexte(univers,personnage,'decrire '+str(personnage.positionX) + ',' + str(personnage.positionY) + ' ' + temps.MomentJournee(personnage.heure))
                if txt != 'ERREUR': print(txt) #On décrit la région si une description est renseignée.
                if deplacements.TestDeRencontre(tempsUneZone,univers.reglages.frequenceRencontre) == True:
                    creature = deplacements.ChoisirCreature(univers,personnage,regionActuelle.creaturesRencontrables,univers.reglages.rencontresParNiveau)
                    if creature != "NULL": 
                        print(textes.TrouverTexte(univers,personnage,'rencontre %s %s %s'%(creature.id,str(personnage.positionX) + ',' + str(personnage.positionY),temps.MomentJournee(personnage.heure)),{'cible':creature.nom,'lieu':regionActuelle.nom}))
                        creature = copy.deepcopy(creature)
                        creature.id+='#'+str(id(creature))
                        personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures.append([creature,[1,1]])
                        time.sleep(1)
                personnage = combat.Tour(univers,personnage)
                skip = False
                while skip == False: 
                    tour = False
                    for crea in personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures:
                        if crea[0].enCombatAvec != [] or personnage.enCombatAvec != []: #Tant qu'il y a un combat dans la zone,
                            tour = True #Un nouveau tour doit avoir lieu
                            break
                    if tour == True: 
                        print('On lance un nouveau tour')
                        personnage = combat.Tour(univers,personnage) #On lance un nouveau tour
                        continue
                    skip = True
        return univers,personnage

class textes:
    '''Classe qui gère tout ce qui concerne les textes.'''

    def TrouverTexte(univers = Univers(),personnage = Personnage(),phrase = '',variables = {}):
        '''Renvoie un texte sélectionné dans le dictionnaire de textes.'''
        dict = univers.textes
        i = 0
        for mot in phrase.split(): #Premier tri, on accepte les *
            newDict = {}
            listItems = []
            type = phrase.split()[0]
            if i == 1:
                if type == 'entrer': listItems = univers.regions
                elif type in ['rencontre','mort','buff','action','fuite','esquive','fuite_echec','incantation','action_ratee']: listItems = univers.creatures
            elif i == 2:
                if type in ['rencontre','mort','fuite','fuite_echec']: listItems = univers.regions
                elif type in ['action','incantation','action_ratee']: listItems = univers.creatures
                elif type in ['esquive']: listItems = univers.actions
            elif i == 3:
                if type in ['action','incantation','action_ratee']: listItems = univers.actions
                elif type in ['esquive']: listItems = univers.regions
            elif i == 4:
                if type in ['action','buff','incantation','action_ratee']: listItems = univers.regions
            for element,valeur in dict.items():
                elementSplit = element.split()[i]
                type = element.split()[0]
               # if phrase.split()[0]=="entrer" and type == "entrer" : print(mot, elementSplit, element)
                if mot == '!PLAYER' or util.VerifItem(listItems,elementSplit,re.findall('^[a-zA-Z_,\d]*[^#]',mot)[0],personnage) or elementSplit == '*': 
                    newDict[element] = valeur
            dict = newDict
            
            i+=1
        if len(dict) > 1: #Si il reste plus d'une valeur, on priorise les emplacements précis
          i = 0
          for mot in phrase.split():
            if len(dict) > 1: #Si il reste plus d'une valeur 
                newDict = {}
                for element,valeur in dict.items():
                    elementSplit = element.split()[i]
                    if ',' in elementSplit: 
                        newDict[element] = valeur
                if newDict: dict = newDict
                i+=1
            else: break
        if len(dict) > 1: #Si il reste plus d'une valeur, on effectue un deuxième tri en éliminant les *
            i = 0
            for mot in phrase.split():
                if len(dict) > 1: #Si il reste plus d'une valeur 
                    newDict = {}
                    for element,valeur in dict.items():
                        elementSplit = element.split()[i]
                        if elementSplit != '*': 
                            newDict[element] = valeur
                    if newDict: dict = newDict
                    i+=1
                else: break
        if len(dict) > 1: #Si il reste plus d'une valeur, on effectue un deuxième tri en éliminant les #
            i = 0
            for mot in phrase.split():
                if len(dict) > 1: #Si il reste plus d'une valeur 
                  newDict = {}
                  for element,valeur in dict.items():
                      elementSplit = element.split()[i]
                      if elementSplit[0] != '#': newDict[element] = valeur
                  if newDict: dict = newDict
                  i+=1
                else: break
        if len(dict) != 0: #Si une valeur a été trouvé
            listeValeurs = list(dict.values())[0]
            random = Random()
            valeur = listeValeurs[random.randint(0,len(listeValeurs) - 1)]
            valeur = textes.TraitementVariables(univers,personnage,variables,valeur)
            return valeur
        else: return "Erreur: aucun texte n'a été trouvé."

    def TraitementVariables(univers = Univers(), personnage = Personnage(), variables = {}, texte = ''):
        """Remplace les éventuels %'' du texte par des données."""
        if '%cible' in texte: texte = texte.replace('%cible',variables['cible'])
        if '%auteur' in texte: texte = texte.replace('%auteur',variables['auteur'])
        if '%action' in texte: texte = texte.replace('%action',variables['action'])
        if '%caract' in texte: texte = texte.replace('%caract',variables['caract'])
        if '%valeur' in texte: texte = texte.replace('%valeur',variables['valeur'])
        if '%lieu' in texte: texte = texte.replace('%lieu',variables['lieu'])
        if '%duree' in texte: texte = texte.replace('%duree',str(variables['duree']))
        if '%direction' in texte: texte = texte.replace('%direction',str(variables['direction']))
        if '%operateur' in texte: texte = texte.replace('%operateur',str(variables['operateur']))
        return texte

class quetes:
    '''Classe qui gère tout ce qui concerne les quêtes.'''
    def VerificationQuetes(univers = Univers(), personnage = Personnage(), action = "null"):
        '''Vérifie les quêtes actives. Retourne personnage.'''
        i = 0
        while i < len(personnage.quetesActives):
            personnage.quetesActives[i].objectifs = quetes.VerificationObjectifs(univers,personnage,personnage.quetesActives[i].objectifs,action) #On vérifie les objectifs de la quête.
            objectifsAcheves = quetes.VerifOrdre(personnage.quetesActives[i].objectifs,personnage.quetesActives[i].objectifsAchevement,2)
            if objectifsAcheves == True: #Si tous les objectifs sont achevés.
                vConditions = conditions.VerifListConditions(personnage,univers,personnage.quetesActives[i].conditionsAchevement) #On vérifie les conditions d'achèvement.
                if vConditions:
                    print(textes.TrouverTexte(univers,personnage,'achever_quete '+quetesActives[i].id))
                    personnage = effets.AjoutListeEffets(personnage,univers,personnage.quetesActives[i].effetsSucces) #On applique les effets de succès.
                    personnage.quetesAchevees.append(personnage.quetesActives[i].id) #On ajoute la quête à la liste des quêtes achevées.
                    del personnage.quetesActives[i] #On supprime la quête de la liste des quêtes actives.
                    i -= 1 #On enlève 1 à i puisque il y a une quête en moins dans la liste que nous sommes entrain de parcourir.  
                    continue #On passe à la quête suivante.       
            elif objectifsAcheves == False and action.split()[0] == 'newHeure': #Si les objectifs ne sont pas achevés et on passe à une nouvelle heure.
                personnage.quetesActives[i].tempsRestant -= 1 #On enlève une heure au temps restant.
            if personnage.quetesActives[i].tempsRestant == 0: #Si le temps restant est écoulé.
                personnage = effets.AjoutListeEffets(personnage,univers,personnage.quetesActives[i].effetsEchec) #On ajoute les effets d'échec au personnage.
                del personnage.quetesActives[i] #On supprime la quête de la liste des quêtes actives.
                i -= 1 #On enlève 1 à i puisque il y a une quête en moins dans la liste que nous sommes entrain de parcourir. 
            i += 1

        return personnage

    def VerificationObjectifs(univers = Univers(), personnage = Personnage(), objectifs = [Objectif()], action = "null"):
        '''Vérifie les objectifs d'une quête active.'''
        for i in range(0,len(objectifs)):
            if objectifs[i].etat == 2: continue #Si l'objectif est achevé, on passe au suivant
            elif objectifs[i].etat == 0: #Si l'objectif n'a pas encore été lancé, on vérifie s'il peut démarrer maintenant.
                if conditions.VerifListConditions(personnage,univers,objectifs[i].conditionsLancement) and quetes.VerifOrdre(objectifs,objectifs[i].ordreLancement,2):
                    objectifs[i].etat = 1
            if objectifs[i].etat == 1: #Si l'objectif est en cours.
                objectifTab = objectifs[i].objectif.split()
                type = objectifTab[0]
                if action != 'null' and action != 'newHeure': #Si une action est bien renseignée. newHeure correspond seulement au changement d'heure pour la vérification des quêtes.      
                    typeAction = action.split()[0]
                    valeurAction = action.split()[1]
                    valeur = objectifTab[1]
                    quantite = int(objectifTab[2])
                    if (type == 'tuer' and typeAction == 'tuer') or (type == 'ramasser' and typeAction == 'ramasser'):                                              
                        lieu = objectifTab[3]
                        heure = objectifTab[4]
                        lieuAction = action.split()[2]
                        heureAction = action.split()[3]
                        if type == 'tuer': listItems = univers.creatures
                        elif type == 'ramasser': listItems = univers.objets
                        if util.VerifItem(listItems,valeur,re.findall('^[a-zA-Z_]*[^#]',valeurAction)[0]) and (util.VerifItem(univers.regions,lieu,re.findall('^[a-zA-Z_]*[^#]',lieuAction)[0]) or lieu == "*") and (heure == heureAction or heure == "*"): objectifs[i].compteur += 1 #Si on a ramassé le bon objet ou tuer la bonne créature au bonne endroit et au bon moment, on ajoute plus 1 au compteur.
                        if objectifs[i].compteur == quantite: objectifs[i].done = True #Si le compteur atteint la quantité voulue, l'objectif est atteint.
                        elif quantite == 0 and objectifs[i].compteur != 0: objectifs[i].done = False #Si la quantité doit être 0, done est alors par défaut à True et passe à False si le compteur augmente.
                    elif (type == 'entrer' and typeAction == 'entrer') or (type == 'parler' and typeAction == 'parler'):
                        heure = objectifTab[3]
                        heureAction = action.split()[2]
                        if type == 'entrer': listItems = univers.regions
                        elif type == 'parler': listItems = univers.creatures
                        if util.VerifItem(listItems,valeur,re.findall('^[a-zA-Z_]*[^#]',valeurAction)[0]) and (heure == heureAction or heure == "*"): objectifs[i].compteur += 1 #Si on a parlé à la bonne personne ou si on est entré dans la bonne région au bon moment, on ajoute plus 1 au compteur.
                        if objectifs[i].compteur == quantite: objectifs[i].done = True #Si le compteur atteint la quantité voulue, l'objectif est atteint.
                        elif quantite == 0 and objectifs[i].compteur != 0: objectifs[i].done = False #Si la quantité doit être 0, done est alors par défaut à True et passe à False si le compteur augmente.
                if objectifs[i].done == True: #Si l'objectif est atteint.
                    if conditions.VerifListConditions(personnage,univers,objectifs[i].conditionsAchevement) and quetes.VerifOrdre(objectifs,objectifs[i].ordreAchevement,2): #Si les conditions d'achèvement sont remplies et l'ordre d'achèvement respecté.
                        objectifs[i].etat = 2
        return objectifs

    def VerifOrdre(objectifs = [Objectif()], list = [''], etat = 0):
        '''Vérifie que les objectifs d'ids donnés dans list sont dans l'etat donné dans objectifs'''
        bool = True
        for element in list:
            if bool == False: break
            for objectif in objectifs:
                if element == objectif.id and objectif.etat != etat: 
                    bool = False
                    break
        return bool

class temps:
    '''Classe qui gère tout ce qui concerne le temps.'''

    def ModifierHeure(personnage = Personnage(), univers = Univers(), ajout = 0.0):
        '''Ajoute x heure à l'heure actuelle. Retourne personnage.'''
        heurePrec = floor(personnage.heure) #Contient l'heure (int) actuelle.
        personnage.heure += ajout #On modifie l'heure.
        if floor(personnage.heure) > heurePrec: #Si on a changé d'heure.
            personnage = effets.ChangementHeure(personnage,univers)
            personnage = quetes.VerificationQuetes(univers,personnage,'newHeure')
        return personnage
    def HeureReel(heure):
        reste = heure%24
        heureReel = 12+reste
        if heureReel > 24: heureReel -= 24
        return heureReel
    def MomentJournee(heure = 0.0):
        '''Donne le moment de la journée en fonction de l'heure (jour ou nuit).'''
        heureReel = temps.HeureReel(heure)
        if 8 <= heureReel <= 21: return 'jour'
        else: return 'nuit'
                                                                                                      
class util:
    """Classe qui contient des méthodes utilitaires."""

    def ModifierValeurBuff(effet , valeur):
        '''Modifie la valeur d'un buff pour faciliter la suppression d'un effet.'''
        tab = effet.split()
        tab[2] = tab[2][0] + str(valeur)
        return " ".join(tab)
    def TrouverEffet(effet = " ", liste = []):
        '''Recherche un effet dans une liste d'après son id(qui est obligatoirement le dernier mot de l'effet).'''
        i = 0
        for element in liste:
            if effet.split()[-1] == element.split()[-1]:
                return i
            else: i+=1
        return -1
    def TrouverEmplacementLibre(emplacementsUtil, emplacements):
        '''Renvoie l'index du premier emplacement utilisable dans le dictionnaires des emplacements. Renvoie -1 aucun emplacement n'est libre.'''
        i = ''
        for empUtil in emplacementsUtil:
            if emplacements[empUtil] == '': 
                i = empUtil
                break
        return i #Retourne l'id de l'emplacement libre dans emplacements
    def TrouverEmplacementObjetEquipe(objet, emplacements):
        '''Renvoie la cle de l'emplacement utilisé par un équipement. Renvoie #NULL si cet équipement n'est pas équipé.'''
        valeurs = list(emplacements.values())
        if objet in valeurs: return list(emplacements.keys())[valeurs.index(objet)]
        else : return '#NULL'
    def TrouverObject(listeObjet,id):
        '''Retourne l'objet avec un id identique à celui donné.'''
        for objet in listeObjet:
            if objet != "" and objet.id == id: return objet
        return None
    def TrouverObjects(listeObjet,motCle):
        '''Renvoie une liste d'objets ayant pour mots clés celui donné.'''
        objets = []
        for objet in listeObjet:
            if motCle in objet.motsCles: objets.append(objet)
        return objets
    def TrouverFutureRegion(map = [[]],X = 0, Y = 0, direction = ""):
        '''Renvoie la région (objet) dans laquelle le joueur veut aller.'''
        Xmax = len(map) - 1
        Ymax = len(map[0]) - 1
        if direction == 'N': Y += 1
        elif direction == 'NE': 
            Y += 1 
            X += 1
        elif direction == 'E': X += 1
        elif direction == 'SE':
            Y -= 1
            X += 1
        elif direction == 'S': Y -= 1
        elif direction == 'SO': 
            Y -= 1
            X -= 1
        elif direction == 'O': X -= 1
        elif direction == 'NO':
            Y += 1
            X -= 1
        if X < 0 or Y < 0 or X > Xmax or Y > Ymax: return "OUT"
        else: return map[X][Y]
    def TrouverX(X = 0, direction = ""):
        '''Renvoie le futur coordonnée X en fonction de la direction.'''
        if direction == 'NE': X += 1
        elif direction == 'E': X += 1
        elif direction == 'SE': X += 1
        elif direction == 'SO': X -= 1
        elif direction == 'O': X -= 1
        elif direction == 'NO': X -= 1
        return X
    def TrouverY(Y = 0, direction = ""):
        '''Renvoie le futur coordonnée Y en fonction de la direction.'''      
        if direction == 'N': Y += 1
        elif direction == 'NE': Y += 1 
        elif direction == 'SE': Y -= 1
        elif direction == 'S': Y -= 1
        elif direction == 'SO': Y -= 1
        elif direction == 'NO': Y += 1
        return Y
    def VerifItem(listeItems = [], idCategorie = "", idItem = "", personnage = None):
        '''Retourne True si l'item est bien l'item voulu ou s'il est dans la bonne catégorie.'''
        
        #Si c'est l'emplacement d'une région
        if ',' in idCategorie:
          if idCategorie == idItem: return True
          else : return False
          
        if ',' in idItem:
          X,Y=int(idItem.split(",")[0]),int(idItem.split(",")[1])
          idItem=personnage.mapUnivers[X][Y].id

        #Si ce n'est pas l'emplacement d'une région, ou un mot-clé : vérification directe
        if idCategorie[0] != "#" and idCategorie == idItem: return True
 
        #Si c'est un mot clé, on vérifie les mots-clés de l'object concerné
        elif idCategorie[0] == "#":
            obj=util.TrouverObject(listeItems,idItem)
            if obj==None: return False
            if idCategorie in obj.motsCles: return True
        else: return False
    def CompterObjetDansInventaire(inventaire = {}, idObjet = ""):
        quantiteObjet = 0
        for objet in inventaire:
            if util.VerifItem(list(inventaire.keys()),idObjet,objet.id): quantiteObjet += inventaire[objet]
        return quantiteObjet
    def CombatDansLaZone(liste = []):
        '''Retourne True si il y a un combat dans la zone ou False sinon.'''
        for creature in liste:
            if creature.enCombatAvec != []:
                return True
        return False

class console:
    """Permet de jouer au jeu grâce à la console."""
    def printEmplacements(dict = {}):
        strings = 'EMPLACEMENTS : '
        for element in dict:
            if dict[element] == '': id = 'vide'
            else: id = dict[element].id
            strings += element + ' : ' + id + ', '
        print(strings)
    def printActions(list = []):
        strings = 'ACTIONS : '
        for element in list:
            strings += element.id + ', '
        print(strings)
    def printHostilites(list = []):
        strings = 'HOSTILITES : '
        for element in list:
            strings += element.id + ', '
        print(strings)
    def printInventaire(dict = {}):
        strings = 'INVENTAIRE : '
        for element in dict:
            strings += str(dict[element]) + ' ' + element.id + ', '
        print(strings)
    def printInterdictions(list = []):
        strings = 'INTERDICTIONS : '
        for element in list:
            strings += element + ', '
        print(strings)
    def printZone(univers = Univers(),personnage = Personnage()):
        regionActuelle = personnage.mapUnivers[personnage.positionX][personnage.positionY]
        print('La zone contient:')
        liste = regionActuelle.objets + regionActuelle.portails + regionActuelle.creatures
        for element in liste:
            if element[1][0] != 0: 
                print(' '+'- '+element[0].id)
    def ExecuterCommande(univers = Univers(), personnage = Personnage(), commande = ''):
        """Analyse et exécute les commandes données par l'utilisateur."""
        if commande == '' or commande == ' ': return univers, personnage
        action = commande.split()[0]
        if action == "aller":
            direction = commande.split()[1]
            if not direction in ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']: print(textes.TrouverTexte(univers,personnage,'erreur mauvaise_direction'))
            else:
                tempsDep = 0
                if len(commande.split()) > 2: tempsDep = float(commande.split()[2])
                univers,personnage = deplacements.Deplacement(univers,personnage,direction,tempsDep)
        elif action == "heure": print(temps.HeureReel(personnage.heure))
        elif action == "position": print(str(personnage.positionX)+','+str(personnage.positionY))
        elif action == "decrire": 
            region = personnage.mapUnivers[personnage.positionX][personnage.positionY]
            if region.objets != []:
                print("Objets:")
                for objet in region.objets:
                    if objet[1][0] in [1,2]: print("- "+objet[0].nom)
            if region.creatures != []:
                print("Creatures:")
                for creature in region.creatures:
                    if creature[1][0] in [1,2]: print("- "+creature[0].nom+' ('+creature[0].id+')')
            if region.portails != []:
                print("Portails:")
                for portail in region.portails:
                    if portail[1][0] in [1,2]: print("- "+portail[0].nom)
        elif action == "cacher":
            idObjet = commande.split()[1]
            liste = [obj for obj in personnage.inventaire if obj.id == idObjet]
            if liste != []:
                objet = liste[0]
                if interactions.VerifJeterObjet(univers,personnage,objet): personnage,univers = interactions.CacherObjet(personnage,univers,objet)
                else: print(textes.TrouverTexte(univers,personnage,'erreur action_non_autorisee'))
            else: print(textes.TrouverTexte(univers,personnage,'erreur objet_non_possede'))
        elif action == "jeter":
            idObjet = commande.split()[1]
            liste = [obj for obj in personnage.inventaire if obj.id == idObjet]
            if liste != []:
                objet = liste[0]
                if interactions.VerifJeterObjet(univers,personnage,objet): personnage,univers = interactions.JeterObjet(personnage,univers,objet)
                else: print(textes.TrouverTexte(univers,personnage,'erreur action_non_autorisee'))
            else: print(textes.TrouverTexte(univers,personnage,'erreur objet_non_possede'))
        elif action == "ramasser":
            idObjet = commande.split()[1]
            liste = [obj[0] for obj in personnage.mapUnivers[personnage.positionX][personnage.positionY].objets if obj[0].id == idObjet]
            if liste != []:
                objet = liste[0]
                if interactions.VerifRamasserObjet(personnage,univers,objet): personnage,univers = interactions.RamasserObjet(personnage,univers,objet)
                else: print(textes.TrouverTexte(univers,personnage,'erreur action_non_autorisee'))
            else: print(textes.TrouverTexte(univers,personnage,'erreur objet_non_trouvable'))
        elif action == "equiper":
            idObjet = commande.split()[1]
            liste = [obj for obj in personnage.inventaire if obj.id == idObjet]
            if liste != []:
                objet = liste[0]
                if interactions.VerifEquiperObjet(personnage,univers,objet): personnage = interactions.EquiperObjet(personnage,objet,univers)
                else: print(textes.TrouverTexte(univers,personnage,'erreur action_non_autorisee'))
            else: print(textes.TrouverTexte(univers,personnage,'erreur objet_non_possede'))
        elif action == "desequiper":
            idObjet = commande.split()[1]
            liste = [obj for obj in personnage.inventaire if obj.id == idObjet]
            if liste != []:
                objet = liste[0]
                if interactions.VerifDesequiperObjet(univers,personnage,objet): personnage = interactions.DesequiperObjet(personnage,objet,univers)
                else: print(textes.TrouverTexte(univers,personnage,'erreur action_non_autorisee'))
            else: print(textes.TrouverTexte(univers,personnage,'erreur objet_non_possede'))
        elif action == "utiliser":
            idObjet = commande.split()[1]
            liste = [obj for obj in personnage.inventaire if obj.id == idObjet]
            if liste != []:
                objet = liste[0]
                if interactions.VerifUtiliserObjet(univers,personnage,objet): personnage = interactions.UtiliserObjet(univers,personnage,objet)
                else: print(textes.TrouverTexte(univers,personnage,'erreur action_non_autorisee'))
            else: print(textes.TrouverTexte(univers,personnage,'erreur objet_non_possede'))
        elif action == "inventaire":
            console.printInventaire(personnage.inventaire)
        elif action == "emplacements":
            console.printEmplacements(personnage.emplacements)
        elif action == "personnage":
            print('PV : '+str(personnage.caracteristiques['pv'])+'/'+str(personnage.caracteristiques['pvBase']))
            print('Poids : '+str(personnage.caracteristiques['poidsPortes'])+'/'+str(personnage.caracteristiques['poidsPortable']))
            print('Vitesse : '+str(personnage.caracteristiques['vitesse']))
            print('Niveau : '+str(personnage.niveau))
            print('Fatigue : '+str(personnage.fatigue))
            for caract in personnage.caracteristiques: 
                if caract not in ['pv','pvBase','poidsPortes','poidsPortable','vitesse']: print(caract[0].capitalize()+caract[1:]+' : '+str(personnage.caracteristiques[caract])+'/'+str(univers.reglages.maxCaract))
        elif action == "parler":
            cible = commande.split()[1]
            liste = [crea[0] for crea in personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures if crea[0].id == cible]
            if liste != []:
                creature = liste[0]
                if creature.dialogue != None:
                    dialogue = creature.dialogue
                    while True:
                        personnage = effets.AjoutListeEffets(personnage,univers,dialogue.effetsChoix)
                        print(creature.nom+' : '+dialogue.text)
                        repUtil = []
                        for reponse in dialogue.reponses:
                            if conditions.VerifListConditions(personnage,univers,dialogue.reponses[reponse].conditionsChoix): repUtil.append(reponse)
                        time.sleep(1)
                        if repUtil != []:
                            for rep in repUtil: print(str(repUtil.index(rep)+1)+': '+rep)
                        else: print('0: Quitter le dialogue.')
                        entree = input("rep: ")
                        if entree == '0': break
                        elif entree == '' or entree == ' ' or int(entree) > len(repUtil): continue
                        else: 
                            dialogue = dialogue.reponses[repUtil[int(entree)-1]]
                else: print(creature.nom+' : ...')
            else: print(textes.TrouverTexte(univers,personnage,'erreur creature_non_trouvable'))
        elif action == "quete":
            for quete in personnage.quetesActives:
                print("- "+quete.nom)
                for objectif in quete.objectifs:
                    etat = ""
                    if objectif.etat == 0: etat = "*Non débuté : "
                    elif objectif.etat == 1: etat = "*En cours : "
                    elif objectif.etat == 2: etat = "*Terminé : "
                    compteur = "("+str(objectif.compteur)+")" 
                    print("    "+etat+' '+objectif.description+' '+compteur)
        elif action == "depouiller":
            if len(commande.split()) > 1:
                cible = commande.split()[1]
                liste = [crea[0] for crea in personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures if crea[0].id == cible]
                if liste != []:
                    if len(commande.split()) == 2:
                        drop = liste[0].inventaire
                        for objet in drop:
                            print("- %s (%s)"%(objet.nom,objet.id)) 
                    if len(commande.split()) == 3:
                        idObjet = commande.split()[2]
                        personnage = interactions.DepouillerCreature(univers,personnage,cible,idObjet) 
                else: print(textes.TrouverTexte(univers,personnage,'erreur depouille_non_trouvable'))
        elif action == "fuir":
            direction = commande.split()[1]
            if not direction in ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']: print(textes.TrouverTexte(univers,personnage,'erreur mauvaise_direction'))
            else:
                listeCreatures = []
                for crea in personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures:
                    listeCreatures.append(crea[0])
                if interactions.JetFuite(univers,listeCreatures,personnage) == True: univers,personnage = interactions.FuiteJoueur(univers,personnage,direction)
                else: 
                    print(textes.TrouverTexte(univers,personnage,"fuite_echec "+"!PLAYER "+str(personnage.positionX) + ',' + str(personnage.positionY)+' '+temps.MomentJournee(personnage.heure),{'auteur':personnage.nom,'lieu':personnage.mapUnivers[personnage.positionX][personnage.positionY].nom}))

        elif action == "test":
            print(personnage.effets)
            print(personnage.enCombatAvec)
            for creature in personnage.mapUnivers[personnage.positionX][personnage.positionY].creatures:
                print("-------------"+creature[0].nom+'('+creature[0].id+')'+'-----------------')
                print("Etat: "+str(creature[1][0]))
                print("En combat avec:")
                for crea in creature[0].enCombatAvec: print("- "+crea)
                print("Cible: "+creature[0].cible)
                print("PV :"+str(creature[0].caracteristiques['pv']))
            print("----------------Elendil-----------------")
            print("En combat avec: "+", ".join(personnage.enCombatAvec))       
            print("PV: "+str(personnage.caracteristiques['pv']))

        return univers,personnage