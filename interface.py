from tkinter import *
from tkinter import ttk
import Personnage
from Action import *
from Objet import *
from Univers import *
from Region import *
from Portail import *
from Creature import *
from Dialogue import *
from Quete import *
from Univers import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import pickle
import os
import copy
import time
import math
import warnings
from PIL import Image, ImageTk
from tkinter.colorchooser import *
from tkinter import simpledialog


        
class notebook:
    
    
    # initialization. receives the master widget
    # reference and the notebook orientation
    def __init__(self, master, side=LEFT):
        
        self.active_fr = None
        self.count = 0
        self.choice = IntVar(0)

        # allows the TOP and BOTTOM
        # radiobuttons' positioning.
        if side in (TOP, BOTTOM):
            self.side = LEFT
        else:
            self.side = TOP

        # creates notebook's frames structure
        self.rb_fr = Frame(master, borderwidth=2, relief=RIDGE)
        self.rb_fr.pack(side=side, fill=BOTH)
        self.screen_fr = Frame(master, borderwidth=2, relief=RIDGE)
        self.screen_fr.pack(fill=BOTH, expand=1)
        

    # return a master frame reference for the external frames (screens)
    def __call__(self):

        return self.screen_fr

        
    # add a new frame (screen) to the (bottom/left of the) notebook
    def add_screen(self, fr, title):
        
        b = Radiobutton(self.rb_fr, text=title, indicatoron=0, \
            variable=self.choice, value=self.count, \
            command=lambda: self.display(fr))
        b.pack(fill=BOTH, side=self.side)
        
        # ensures the first frame will be
        # the first selected/enabled
        if not self.active_fr:
            fr.pack(fill=BOTH, expand=1)
            self.active_fr = fr
        self.count += 1
        return b
        
        
    # hides the former active frame and shows 
    # another one, keeping its reference
    def display(self, fr):
        self.active_fr.refresh()
        self.active_fr.forget()
        fr.pack(fill=BOTH,expand=1)
        self.active_fr = fr
        self.active_fr.refresh()
        if not self.choice.get()==7:
            if menubar.index('end')==2:
                menubar.delete(2)
        else:
            if not menubar.index('end')==2:
                menubar.add_cascade(label="Editeur",menu=menuEditeur)
        


def Enregistrer():
    path = asksaveasfilename(defaultextension='.univedit',initialfile='univers')
    if path:
        if not os.path.splitext(path)[1]==".univedit": 
            showinfo('Erreur','Mauvaise extension')
            return
        output = open(path,'wb')
        pickle.dump(univers,output)
        output.close()
        showinfo('','Univers enregistré !')
def Exporter():
    path = asksaveasfilename(defaultextension='.univ',initialfile='univers')
    if path:
        if not os.path.splitext(path)[1]==".univ": 
            showinfo('Erreur','Mauvaise extension')
            return
        for creature in univers.creatures:
            inventaireObj=[]
            for objet in creature.inventaire:
                obj=findObjectFromID(univers.objets,objet)
                if obj is not None: inventaireObj.append(obj)
            creature.inventaire=inventaireObj
            actionObj=[]
            for action in creature.actions:
                action=findObjectFromID(univers.actions,action)
                if action is not None: actionObj.append(action)
            if creature.dialogue is not None and creature.dialogue.id not in univers.dialogues.keys(): creature.dialogue=None
        output = open(path,'wb')
        pickle.dump(univers,output)
        output.close()
        showinfo('','Univers enregistré !')
def Charger():
    path = askopenfilename()
    if path:
        if not os.path.splitext(path)[1]==".univedit": 
            showinfo('Erreur','Mauvaise extension')
            return
        output = open(path,'rb')
        global univers
        univers = pickle.load(output)
        output.close()
        onglet_reglages.load(univers.reglages)
        onglet_actions.listObject = univers.actions
        onglet_objets.listObject = univers.objets
        onglet_creatures.listObject = univers.creatures
        onglet_actions.ChargerList()
        onglet_objets.ChargerList()
        onglet_creatures.ChargerList()
        onglet_dialogues.loadDialogs()


class FrameReglages(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        
        self.f1=LabelFrame(self,text="Mode de calcul du malus de déplacement")
        self.f1.pack(fill=BOTH)
        self.modeCalculDeplacement = StringVar()
        self.bradioCalculAbsolu = Radiobutton(self.f1, text="Absolu", variable = self.modeCalculDeplacement, value="absolu", command=lambda: self.ModifValeur('ModeCalculDeplacement','absolu'))
        self.bradioCalculRelatif = Radiobutton(self.f1, text="Relatif", variable = self.modeCalculDeplacement, value="relatif", command=lambda: self.ModifValeur('ModeCalculDeplacement','relatif'))
        self.modeCalculDeplacement.set("relatif")
        self.bradioCalculAbsolu.pack(fill=BOTH, expand=1)
        self.bradioCalculRelatif.pack(fill=BOTH, expand=1)

        self.f2=LabelFrame(self,text="Rencontres par niveau")
        self.f2.pack(fill=BOTH)
        self.valRencontreNiveau = BooleanVar()
        self.bradioRencontreNiveauTrue = Radiobutton(self.f2, text="Oui", variable = self.valRencontreNiveau, value=True, command=lambda: self.ModifValeur('RencontreNiveau',True))
        self.bradioRencontreNiveauFalse = Radiobutton(self.f2, text="Non", variable = self.valRencontreNiveau, value=False, command=lambda: self.ModifValeur('RencontreNiveau',False))
        self.valRencontreNiveau.set(True)
        self.bradioRencontreNiveauTrue.pack(fill=BOTH, expand=1)
        self.bradioRencontreNiveauFalse.pack(fill=BOTH, expand=1)

        self.f3=LabelFrame(self,text="Autoriser l'esquive")
        self.f3.pack(fill=BOTH)
        self.valAutoriserEsquive = BooleanVar()
        self.bradioAutoriserEsquiveTrue = Radiobutton(self.f3, text="Oui", variable = self.valAutoriserEsquive, value=True, command=lambda: self.ModifValeur('AutoriserEsquive',True))
        self.bradioAutoriserEsquiveFalse = Radiobutton(self.f3, text="Non", variable = self.valAutoriserEsquive, value=False, command=lambda: self.ModifValeur('AutoriserEsquive',False))
        self.valAutoriserEsquive.set(True)
        self.bradioAutoriserEsquiveTrue.pack(fill=BOTH, expand=1)
        self.bradioAutoriserEsquiveFalse.pack(fill=BOTH, expand=1)

        self.f4=LabelFrame(self,text="Caractéristiques")
        self.f4.pack(fill=BOTH)
        self.lBoxCaract=Listbox(self.f4,height=6)
        self.lBoxCaract.pack(side = TOP, expand=1)
        self.buttonAddCaract = Button(self.f4,text="Ajouter",command=self.ajoutCaract)
        self.buttonSupCaract = Button(self.f4,text="Supprimer",command=self.supCaract)
        self.buttonAddCaract.pack()
        self.buttonSupCaract.pack()

        self.f5=LabelFrame(self,text="Attribution des caractéristiques")
        self.f5.pack(fill=BOTH)
        self.lCaractEsquive=Label(self.f5,text="Esquive : ").grid(row=1,column=0)
        self.lCaractFouille=Label(self.f5,text="Fouille : ").grid(row=2,column=0)
        self.lCaractNegociation1=Label(self.f5,text="Negociation (premier) : ").grid(row=3,column=0)
        self.lCaractNegociation2=Label(self.f5,text="Negociation (second) : ").grid(row=4,column=0)
        self.lCaractFuite=Label(self.f5,text="Fuite : ").grid(row=5,column=0)
        self.lCaractInitiative=Label(self.f5,text="Initiative : ").grid(row=6,column=0)
        self.lCaractAttaque=Label(self.f5,text="Attaque : ").grid(row=7,column=0)
        self.lCaractSoin=Label(self.f5,text="Soin : ").grid(row=8,column=0)
        self.caractEsquive=StringVar()
        self.caractFouille=StringVar()
        self.caractNegociation1=StringVar()
        self.caractNegociation2=StringVar()
        self.caractFuite=StringVar()
        self.caractInitiative=StringVar()
        self.caractAttaque=StringVar()
        self.caractSoin=StringVar()
        self.lDeroulEsquive=OptionMenu(self.f5,self.caractEsquive,[],command=lambda value:self.ModifValeur('CaractEsquive',value))
        self.lDeroulFouille=OptionMenu(self.f5,self.caractFouille,[],command=lambda value:self.ModifValeur('CaractFouille',value))
        self.lDeroulNegociation1=OptionMenu(self.f5,self.caractNegociation1,[],command=lambda value:self.ModifValeur('CaractNegociation1',value))
        self.lDeroulNegociation2=OptionMenu(self.f5,self.caractNegociation2,[],command=lambda value:self.ModifValeur('CaractNegociation2',value))
        self.lDeroulFuite=OptionMenu(self.f5,self.caractFuite,[],command=lambda value:self.ModifValeur('CaractFuite',value))
        self.lDeroulInitiative=OptionMenu(self.f5,self.caractInitiative,[],command=lambda value:self.ModifValeur('CaractInitiative',value))
        self.lDeroulAttaque=OptionMenu(self.f5,self.caractAttaque,[],command=lambda value:self.ModifValeur('CaractAttaque',value))
        self.lDeroulSoin=OptionMenu(self.f5,self.caractSoin,[],command=lambda value:self.ModifValeur('CaractSoin',value))
        self.lDeroulEsquive.grid(row=1,column=1)
        self.lDeroulFouille.grid(row=2,column=1)
        self.lDeroulNegociation1.grid(row=3,column=1)
        self.lDeroulNegociation2.grid(row=4,column=1)
        self.lDeroulFuite.grid(row=5,column=1)
        self.lDeroulInitiative.grid(row=6,column=1)
        self.lDeroulAttaque.grid(row=7,column=1)
        self.lDeroulSoin.grid(row=8,column=1)

        self.f6=LabelFrame(self,text="Valeurs")
        self.f6.pack(fill=BOTH)
        self.lMaxCaract=Label(self.f6,text="Score maximal d'un caractéristique : ")
        self.spinBoxMaxCaract=Spinbox(self.f6,from_=1,to=1000,command=lambda: self.ModifValeur('MaxCaract',int(self.spinBoxMaxCaract.get())))
        self.spinBoxMaxCaract.delete(0,END)
        self.spinBoxMaxCaract.insert(0,'0')
        self.spinBoxMaxCaract.bind("<Key>",lambda e: "break")
        self.lFreqRencontre=Label(self.f6,text="Fréquence de rencontre : ")
        self.spinBoxFreqRencontre=Spinbox(self.f6,from_=0.0,to=100,increment=0.1,command=lambda: self.ModifValeur('FreqRencontre',float(self.spinBoxFreqRencontre.get())))
        self.spinBoxFreqRencontre.bind("<Key>",lambda e: "break")
        self.spinBoxFreqRencontre.delete(0,END)
        self.spinBoxFreqRencontre.insert(0,'0')
        self.lMaxCaract.grid(row=0,column=0)
        self.lFreqRencontre.grid(row=1,column=0)
        self.spinBoxMaxCaract.grid(row=0,column=1)
        self.spinBoxFreqRencontre.grid(row=1,column=1)
        
    def ajoutCaract(self):
        caract = askCaracteristique(self).result
        if caract:
            caract=transformNom(caract)
            if caract in univers.reglages.caracts: 
                showinfo('Erreur','Caractéristique déjà existant')
                return
            self.lBoxCaract.insert(1,caract)
            univers.reglages.caracts.append(caract)
            self.ActualiserCaract()
    def supCaract(self):
        if self.lBoxCaract.curselection() != (): 
            sel=self.lBoxCaract.get(self.lBoxCaract.curselection()[0])
            univers.reglages.caracts.remove(sel)
            if sel == self.caractEsquive.get(): self.caractEsquive.set('')
            if sel == self.caractFouille.get(): self.caractFouille.set('')
            if sel == self.caractNegociation1.get(): self.caractNegociation1.set('')
            if sel == self.caractNegociation2.get(): self.caractNegociation2.set('')
            if sel == self.caractFuite.get(): self.caractFuite.set('')
            if sel == self.caractInitiative.get(): self.caractInitiative.set('')
            if sel == self.caractAttaque.get(): self.caractAttaque.set('')
            if sel == self.caractSoin.get(): self.caractSoin.set('')
            
            self.lBoxCaract.delete(self.lBoxCaract.curselection())    

    def ModifValeur(self,variable,valeur):
        if variable == "ModeCalculDeplacement": univers.reglages.modeCalculMalusDeplacement = valeur
        elif variable == "RencontreNiveau": univers.reglages.rencontresParNiveau = valeur
        elif variable == "AutoriserEsquive": univers.reglages.autoriserEsquive = valeur
        elif variable == "CaractEsquive": 
            univers.reglages.caractEsquive = valeur
            self.caractEsquive.set(valeur)
        elif variable == "CaractFouille": 
            univers.reglages.caractFouille = valeur
            self.caractFouille.set(valeur)
        elif variable == "CaractNegociation1": 
            univers.reglages.caractNegociation1 = valeur
            self.caractNegociation1.set(valeur)
        elif variable == "CaractNegociation2": 
            univers.reglages.caractNegociation2 = valeur
            self.caractNegociation2.set(valeur)
        elif variable == "CaractFuite": 
            univers.reglages.caractFuite = valeur
            self.caractFuite.set(valeur)
        elif variable == "CaractInitiative": 
            univers.reglages.caractInitiative = valeur
            self.caractInitiative.set(valeur)
        elif variable == "CaractAttaque": 
            univers.reglages.caractAttaque = valeur
            self.caractAttaque.set(valeur)
        elif variable == "CaractSoin": 
            univers.reglages.caractSoin = valeur
            self.caractSoin.set(valeur)
        elif variable == "MaxCaract": univers.reglages.maxCaract = valeur
        elif variable == "FreqRencontre": univers.reglages.frequenceRencontre = valeur
            
    def refresh(self): pass
        
    def ActualiserCaract(self):
        self.lDeroulEsquive['menu'].delete(0,END)
        self.lDeroulFouille['menu'].delete(0,END)
        self.lDeroulNegociation1['menu'].delete(0,END)
        self.lDeroulNegociation2['menu'].delete(0,END)
        self.lDeroulFuite['menu'].delete(0,END)
        self.lDeroulInitiative['menu'].delete(0,END)
        self.lDeroulAttaque['menu'].delete(0,END)
        self.lDeroulSoin['menu'].delete(0,END)
        for caract in univers.reglages.caracts: 
            self.lDeroulEsquive['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractEsquive',value))
            self.lDeroulFouille['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractFouille',value))
            self.lDeroulNegociation1['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractNegociation1',value))
            self.lDeroulNegociation2['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractNegociation2',value))
            self.lDeroulFuite['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractFuite',value))
            self.lDeroulInitiative['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractInitiative',value))
            self.lDeroulAttaque['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractAttaque',value))
            self.lDeroulSoin['menu'].add_command(label=caract, command=lambda value=caract: self.ModifValeur('CaractSoin',value))
    
    def load(self,reglages):
        if reglages.modeCalculMalusDeplacement=="relatif": self.modeCalculDeplacement.set("relatif")
        elif reglages.modeCalculMalusDeplacement=="absolu": self.modeCalculDeplacement.set("absolu")
        if reglages.rencontresParNiveau==True: self.valRencontreNiveau.set(True)
        else: self.valRencontreNiveau.set(False)
        if reglages.autoriserEsquive==True: self.valAutoriserEsquive.set(True)
        else: self.valAutoriserEsquive.set(False)
        self.lBoxCaract.delete(0,END)
        for caract in reglages.caracts: self.lBoxCaract.insert(1,caract)
        self.ActualiserCaract()
        self.caractEsquive.set(univers.reglages.caractEsquive)
        self.caractFouille.set(univers.reglages.caractFouille)
        self.caractNegociation1.set(univers.reglages.caractNegociation1)
        self.caractNegociation2.set(univers.reglages.caractNegociation2)
        self.caractFuite.set(univers.reglages.caractFuite)
        self.caractInitiative.set(univers.reglages.caractInitiative)
        self.caractAttaque.set(univers.reglages.caractAttaque)
        self.caractSoin.set(univers.reglages.caractSoin)
        self.spinBoxMaxCaract.delete(0,END)
        self.spinBoxFreqRencontre.delete(0,END)
        self.spinBoxMaxCaract.insert(0,str(reglages.maxCaract))
        self.spinBoxFreqRencontre.insert(0,str(reglages.frequenceRencontre))
 
class AutocompleteCombobox(ttk.Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(INSERT), END)
                        self.position = self.index(END)
                if event.keysym == "Left":
                        if self.position < self.index(END): # delete the selection
                                self.delete(self.position, END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, END)
                if event.keysym == "Right":
                        self.position = self.index(END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion
class FrameInterdictions(LabelFrame):
    def __init__(self,parent,text=None):
        LabelFrame.__init__(self,parent,text=text)
        self.createWidgets()
        
    def createWidgets(self):
        self.interdiction=''
        self.oldType=''
        self.labelType=Label(self,text='Type :')
        self.labelType.grid(row=0,column=0)
        self.listType=AutocompleteCombobox(self)
        self.listType.set_completion_list(['poss','unposs','equip','unequip','ramasser','jeter','utiliser','entrer','sortir','rencontrer'])
        self.listType.bind('<<ComboboxSelected>>',self.gererType)
        self.listType.grid(row=0,column=1)
        self.labelObjet=Label(self,text='Objet :')
        self.listObjet=AutocompleteCombobox(self)
        self.listObjet.set_completion_list([objet.id for objet in univers.objets])
        self.labelRegion=Label(self,text='Région/Emplacement :')
        self.listRegion=AutocompleteCombobox(self)
        self.listRegion.set_completion_list([region.id for region in univers.regions])
        self.labelCreature=Label(self,text='Créature :')
        self.listCreature=AutocompleteCombobox(self)
        self.listCreature.set_completion_list([creature.id for creature in univers.creatures])
    def gererType(self,event):
        self.clean()
        type=self.listType.get()
        self.oldType=type
        if type in ['poss','unposs','equip','unequip','ramasser','jeter','utiliser']:
            self.labelObjet.grid(row=0,column=2)
            self.listObjet.grid(row=0,column=3)
        elif type in ['entrer','sortir']:
            self.labelRegion.grid(row=0,column=2)
            self.listRegion.grid(row=0,column=3)
        elif type == 'rencontrer':
            self.labelCreature.grid(row=0,column=2)
            self.listCreature.grid(row=0,column=3)
    def clean(self):
        type=self.oldType
        if type in ['poss','unposs','equip','unequip','ramasser','jeter','utiliser']:
            self.labelObjet.grid_forget()
            self.listObjet.grid_forget()
        elif type in ['entrer','sortir']:
            self.labelRegion.grid_forget()
            self.listRegion.grid_forget()
        elif type == 'rencontrer':
            self.labelCreature.grid_forget()
            self.listCreature.grid_forget()
    def createInterdiction(self):
        type=self.listType.get()
        if type in ['poss','unposs','equip','unequip','ramasser','jeter','utiliser']: self.interdiction="{0} {1}".format(type,self.listObjet.get())
        elif type in ['entrer','sortir']:
            if re.match(r'^\d+,\d+$',self.listRegion.get()): self.interdiction="{0} {1}".format(type,self.listRegion.get())
            else: self.interdiction="{0} {1}".format(type,self.listRegion.get())
        elif type=='rencontrer': self.interdiction="{0} {1}".format(type,self.listCreature.get())
class FrameEffets(LabelFrame):
    def __init__(self,parent,text=None):
        LabelFrame.__init__(self,parent,text=text)
        self.createWidgets()
    def createWidgets(self):
        self.effets=[]
        self.listEffets=Listbox(self)
        self.listEffets.pack(side=LEFT,expand=1,fill=BOTH)
        self.boutonAjouter=Button(self,text='Ajouter',command=self.AjoutEffet)
        self.boutonSupprimer=Button(self,text='Supprimer',command=self.SupprimerEffet)
        self.boutonAjouter.pack(side=TOP,fill=BOTH)
        self.boutonSupprimer.pack(side=BOTTOM,fill=BOTH)
    def AjoutEffet(self):
        result = askEffet(self).result
        
        if result:
            self.listEffets.insert(1,result)
            self.effets.append(result)
    def SupprimerEffet(self):
        if self.listEffets.curselection() != (): 
            self.effets.remove(self.listEffets.get(self.listEffets.curselection()[0]))
            self.listEffets.delete(self.listEffets.curselection())
    def clear(self):
        self.listEffets.delete(0,END)
        del self.effets
        self.effets=[]
    def update(self,list):
        self.listEffets.insert(0,*list)
        self.effets.extend(list)

class FrameObjetOrCrea(LabelFrame):
    def __init__(self,parent,text=None,type=""):
        LabelFrame.__init__(self,parent,text=text)
        self.type=type
        self.createWidgets()
    def createWidgets(self):
        self.items=[]
        self.listObjects=Listbox(self)
        self.listObjects.pack(side=LEFT,expand=1,fill=BOTH)
        self.boutonAjouter=Button(self,text='Ajouter',command=self.Ajout)
        self.boutonSupprimer=Button(self,text='Supprimer',command=self.Supprimer)
        self.boutonModifier=Button(self,text="Modifier",command=self.Modifier)
        self.boutonAjouter.pack(side=TOP,fill=BOTH)
        self.boutonSupprimer.pack(side=BOTTOM,fill=BOTH)
        self.boutonModifier.pack(side=RIGHT,fill=X)
    def Ajout(self):
        result = askObjetOrCrea(self,type=self.type).result
        if result:
            self.listObjects.insert(END,result[0].id+'||Etat: '+['Caché','Découvert'][result[1][0]]+'||Multiplicateur de fouille: '+str(result[1][1]))
            self.items.append([result[0],[result[1][0],result[1][1]]])
    def Supprimer(self):
        if self.listObjects.curselection() != (): 
            itemSelected=self.listObjects.get(self.listObjects.curselection()[0])
            item=[it for it in self.items if it[0].id == itemSelected.split('||')[0]][0]
            self.items.remove(item)
            self.listObjects.delete(self.listObjects.curselection())
    def Modifier(self):
        if self.listObjects.curselection() != ():
            selection=self.listObjects.curselection()
            itemSelected=self.listObjects.get(self.listObjects.curselection()[0])
            item=[it for it in self.items if it[0].id == itemSelected.split('||')[0]][0]
            result = askObjetOrCrea(self,type=self.type,item=item).result
            if result:
                self.items[self.items.index(item)]=result
                self.listObjects.delete(selection)
                self.listObjects.insert(selection[0],result[0].id+'||Etat: '+['Caché','Découvert'][result[1][0]]+'||Multiplicateur de fouille: '+str(result[1][1]))
    def clear(self):
        self.listObjects.delete(0,END)
        del self.items
        self.items=[]
    def update(self,list):
        for element in list:
            self.listObjects.insert(END,element[0].id+'||Etat: '+['Caché','Découvert'][element[1][0]]+'||Multiplicateur de fouille: '+str(element[1][1]))
        self.items.extend(list)
class FrameDescription(LabelFrame):
    def __init__(self,parent,text=None):
        LabelFrame.__init__(self,parent,text=text)
        self.createWidgets()
    def createWidgets(self):
        self.motsCles=[]
        self.labelNom = Label(self,text='Nom :')
        self.labelId = Label(self,text='ID :')
        self.labelMotsCles = Label(self,text='Mots clés :')
        self.labelDescription = Label(self,text='Description :')
        self.nom=StringVar()
        self.id=StringVar()
        self.entryNom=Entry(self,textvariable=self.nom)
        self.entryId=Entry(self,textvariable=self.id)
        self.textDescription=Text(self,width=25,height=10)
        self.listMotsCles=Listbox(self)
        self.boutonAddMotCle=Button(self,text='Ajouter mot clé',command=self.addMotCle)
        self.boutonSuppMotCle=Button(self,text='Supprimer mot clé',command=self.suppMotCle)
        self.labelNom.grid(row=0,column=1)
        self.entryNom.grid(row=0,column=2,columnspan=1)
        self.labelId.grid(row=0,column=7)
        self.entryId.grid(row=0,column=8,columnspan=1)
        self.labelDescription.grid(row=2,column=2)
        self.textDescription.grid(row=3,column=1,columnspan=2,rowspan=6)
        self.labelMotsCles.grid(row=2,column=8)
        self.listMotsCles.grid(row=3,column=6,columnspan=3,rowspan=6)
        self.boutonAddMotCle.grid(row=4,column=9,columnspan=1,sticky='S')
        self.boutonSuppMotCle.grid(row=5,column=9,columnspan=1,sticky='N')
        
    def addMotCle(self):
        result = askCaracteristique(self).result
        if result:
            if re.match(r'^#\w+$',result)!=None:
                self.listMotsCles.insert(1,result)
                self.motsCles.append(result)
            else: showinfo('Erreur','Entrée invalide. Doit commencer par # et peut contenir des caractères alpha-numériques ainsi que _.')
    def suppMotCle(self):
        if self.listMotsCles.curselection() != (): 
            self.motsCles.remove(self.listMotsCles.get(self.listMotsCles.curselection()[0]))
            self.listMotsCles.delete(self.listMotsCles.curselection())
class Caract(Frame):
    def __init__(self,parent,nom='',x=0,y=0):
        Frame.__init__(self,parent)
        self.nom=nom
        self.valeur=StringVar()
        self.labelCaract = Label(self,text=nom)
        self.compteurCaract = Spinbox(self,from_=0.0,to=100000,increment=0.1,textvariable=self.valeur)
        self.compteurCaract.delete(0,END)
        self.compteurCaract.insert(0,'0.0')
        self.labelCaract.grid(row=0,column=0)
        self.compteurCaract.grid(row=0,column=1)
        self.grid(row=y,column=x)       
    def Destroy(self):
        self.labelCaract.destroy()
        self.compteurCaract.destroy()
        self.destroy()
class FrameCaract(LabelFrame):
    def __init__(self,parent,text=None,type='Creature'):
        LabelFrame.__init__(self,parent,text=text)
        self.createWidgets(type)
    def createWidgets(self,type):
        self.listFrame = []
        i=0
        x=0
        y=0
        caractEnPlus = []
        if type=='Creature': caractEnPlus = ['pv','pvBase']
        elif type=='Joueur': caractEnPlus = ['pv','pvBase','poidsPortable','poidsPortes']
        for caract in univers.reglages.caracts+caractEnPlus:
            i+=1
            self.listFrame.append(Caract(self,caract,x,y))
            if i%2==0: 
                y+=1
                x=0
            else: x=1
    def refresh(self):
        for caract in self.listFrame: 
            caract.Destroy()
        del self.listFrame
        self.createWidgets('Creature')
class FrameList(LabelFrame):
    def __init__(self,parent,text=None,type='',listObjectifs=[]):
        LabelFrame.__init__(self,parent,text=text)
        if type=='action': self.listObject=univers.actions
        elif type=='objet': self.listObject=univers.objets
        elif type=='creature': self.listObject=univers.creatures
        elif type=='objectif': self.listObject=listObjectifs
        self.items = []
        self.type=type
        self.createWidgets()
    def createWidgets(self):
        self.list=Listbox(self,selectmode=EXTENDED)
        self.frameButtons=Frame(self)
        self.combobox = AutocompleteCombobox(self.frameButtons)
        self.combobox.set_completion_list([element.id if type(element) is not str else element for element in self.listObject])
        self.boutonAjouter = Button(self.frameButtons,text="Ajouter",command=self.AddItem)
        self.boutonRetirer = Button(self.frameButtons,text="Retirer",command=self.SuppItem)
        self.list.pack(fill=BOTH,expand=1,side=LEFT)
        self.frameButtons.pack(side=RIGHT,fill=Y)
        self.combobox.pack(pady=10)
        self.boutonAjouter.pack(pady=10)
        self.boutonRetirer.pack(pady=10)
    def AddItem(self):
        id = self.combobox.get()
        if id:
            if self.validate():
                self.items.append(id)
                self.list.insert(0,id)
    def SuppItem(self):
        if self.list.curselection():
            selection=self.list.curselection()
            for i in selection:        
                id = self.list.get(i)
                self.items.remove(id)   
            i=0
            for e in selection:
                self.list.delete(e-i)
                i+=1
    def clear(self):
        self.list.delete(0,END)
        self.items = []
    def updateChoices(self,listObjectifs=[]):    
        if self.type=='creature':    
            listCrea=[crea.id for crea in univers.creatures]
            items=set(self.items)-set(listCrea)
            for item in items: 
                if item[0]!='#': 
                    self.items.remove(item)
                    self.list.delete(self.list.get(0,END).index(item))
            self.combobox.set_completion_list(listCrea)
        elif self.type=='objet' or self.type=='action': 
            listItems=[item.id for item in self.listObject]
            items=set(self.items)-set(listItems)
            for item in items:
                self.items.remove(item)
                self.list.delete(self.list.get(0,END).index(item))
            self.combobox.set_completion_list(listItems)
        elif self.type=='objectif':
            for item in self.items:
                if item not in listObjectifs: 
                    self.list.delete(self.list.get(0,END).index(item))   
                    self.items.remove(item)   
            self.combobox.set_completion_list(listObjectifs)
        self.combobox.set("")
    def update(self, list):
        self.list.insert(0,*list)
        self.items.extend(list)
    def validate(self):
        if self.type=='creature':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.combobox.get())==None:
                showinfo('Erreur',"Entrée invalide. Contient l'id d'une créature (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
            if self.combobox.get()[0]!='#' and findObjectFromID(self.listObject,self.combobox.get())==None:
                showinfo('Erreur',"Créature inexistante.")
                return False
        elif self.type=='objet':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+)$",self.combobox.get())==None:
                showinfo('Erreur',"Entrée invalide. Contient l'id d'un objet.")
                return False
            if findObjectFromID(self.listObject,self.combobox.get())==None:
                showinfo('Erreur',"Objet inexistant.")
                return False
        elif self.type=='action':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+)$",self.combobox.get())==None:
                showinfo('Erreur',"Entrée invalide. Contient l'id d'une action.")
                return False
            if findObjectFromID(self.listObject,self.combobox.get())==None:
                showinfo('Erreur',"Action inexistante.")
                return False
        elif self.type=='objectif':
            if self.combobox.get() not in self.listObject:
                showinfo('Erreur','Objectif inexistant pour cette quête')
                return False
            if self.combobox.get() in self.items:
                showinfo('Erreur','Objectif déjà ajouté')
                return False
        return True
class FrameObjectifs(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.objectif=''
        self.createWidgets()
    def createWidgets(self):
        self.type=''
        self.labelType=Label(self,text='Action :')
        self.labelObjet=Label(self,text='Objet :')
        self.labelLieu=Label(self,text='Lieu :')
        self.labelCreature=Label(self,text='Creature :')
        self.labelQuantite=Label(self,text='Quantité :')
        self.labelHeure=Label(self,text='Heure :')
        self.listType=AutocompleteCombobox(self)
        self.listType.set_completion_list(['ramasser', 'tuer', 'entrer', 'parler'])
        self.listType.bind('<<ComboboxSelected>>',self.gererType)
        self.listObjet=AutocompleteCombobox(self)
        self.listObjet.set_completion_list([objet.id for objet in univers.objets]+['*'])
        self.listRegion=AutocompleteCombobox(self)
        self.listRegion.set_completion_list([region.id for region in univers.regions]+['*'])
        self.listCrea=AutocompleteCombobox(self)
        self.listCrea.set_completion_list([crea.id for crea in univers.creatures]+['*'])
        self.compteurQuantite=Spinbox(self,from_=0,to=10000000000)
        self.heure=StringVar()
        self.heure.set('*')
        self.listHeure=OptionMenu(self,self.heure,*['jour','nuit','*'])
        self.labelType.grid(row=0,column=0)
        self.listType.grid(row=0,column=1)
    def clean(self):
        type=self.type
        if type=='ramasser':
            self.labelObjet.grid_forget()
            self.listObjet.grid_forget()
            self.labelQuantite.grid_forget()
            self.compteurQuantite.grid_forget()
            self.labelLieu.grid_forget()
            self.listRegion.grid_forget()
            self.labelHeure.grid_forget()
            self.listHeure.grid_forget()
        elif type=='entrer':
            self.labelLieu.grid_forget()
            self.listRegion.grid_forget()
            self.labelQuantite.grid_forget()
            self.compteurQuantite.grid_forget()
            self.labelHeure.grid_forget()
            self.listHeure.grid_forget()
        elif type=='tuer':
            self.labelCreature.grid_forget()
            self.listCrea.grid_forget()
            self.labelQuantite.grid_forget()
            self.compteurQuantite.grid_forget()
            self.labelLieu.grid_forget()
            self.listRegion.grid_forget()
            self.labelHeure.grid_forget()
            self.listHeure.grid_forget()
        elif type=='parler':
            self.labelCreature.grid_forget()
            self.listCrea.grid_forget()
            self.labelQuantite.grid_forget()
            self.compteurQuantite.grid_forget()
            self.labelHeure.grid_forget()
            self.listHeure.grid_forget()
    def gererType(self,event=None):
        self.clean()
        self.type=self.listType.get()
        type=self.type
        if type=='ramasser':
            self.labelObjet.grid(row=0,column=2)
            self.listObjet.grid(row=0,column=3)
            self.labelQuantite.grid(row=0,column=4)
            self.compteurQuantite.grid(row=0,column=5)
            self.labelLieu.grid(row=0,column=6)
            self.listRegion.grid(row=0,column=7)
            self.labelHeure.grid(row=0,column=8)
            self.listHeure.grid(row=0,column=9)
        elif type=='entrer':
            self.labelLieu.grid(row=0,column=2)
            self.listRegion.grid(row=0,column=3)
            self.labelQuantite.grid(row=0,column=4)
            self.compteurQuantite.grid(row=0,column=5)
            self.labelHeure.grid(row=0,column=6)
            self.listHeure.grid(row=0,column=7)
        elif type=='tuer':
            self.labelCreature.grid(row=0,column=2)
            self.listCrea.grid(row=0,column=3)
            self.labelQuantite.grid(row=0,column=4)
            self.compteurQuantite.grid(row=0,column=5)
            self.labelLieu.grid(row=0,column=6)
            self.listRegion.grid(row=0,column=7)
            self.labelHeure.grid(row=0,column=8)
            self.listHeure.grid(row=0,column=9)
        elif type=='parler':
            self.labelCreature.grid(row=0,column=2)
            self.listCrea.grid(row=0,column=3)
            self.labelQuantite.grid(row=0,column=4)
            self.compteurQuantite.grid(row=0,column=5)
            self.labelHeure.grid(row=0,column=6)
            self.listHeure.grid(row=0,column=7)
    def validate(self):
        if self.listType.get() not in ['ramasser','tuer','parler','entrer']:
            showinfo('Erreur','Type inconnu')
            return False
        if re.match(r'^\d+$',self.compteurQuantite.get())==None:
            showinfo('Erreur','Quantité invalide, doit être un nombre entier positif')
            return False
        type = self.listType.get()
        if type=='ramasser':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+|\*)$",self.listObjet.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'un objet (caractères alpha-numériques et underscore), un mot clé (commencant par #) ou * symbolisant tous les objets possibles.")
                return False
            if self.listObjet.get()[0] not in ['#','*'] and findObjectFromID(univers.objets,self.listObjet.get())==None:
                showinfo('Erreur',"Objet inexistant")
                return False
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+|\*)$",self.listRegion.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'une région (caractères alpha-numériques et underscore), un mot clé (commencant par #) ou * symbolisant toutes les régions possibles.")
                return False
            if self.listRegion.get()[0] not in ['#','*'] and findObjectFromID(univers.regions,self.listRegion.get())==None:
                showinfo('Erreur',"Région inexistante")
                return False
        elif type=='entrer':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+|\*)$",self.listRegion.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'une région (caractères alpha-numériques et underscore), un mot clé (commencant par #) ou * symbolisant toutes les régions possibles.")
                return False
            if self.listRegion.get()[0] not in ['#','*'] and findObjectFromID(univers.regions,self.listRegion.get())==None:
                showinfo('Erreur',"Région inexistante")
                return False
        elif type=='parler':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+|\*)$",self.listCrea.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'une créature (caractères alpha-numériques et underscore), un mot clé (commencant par #) ou * symbolisant toutes les créatures possibles.")
                return False
            if self.listCrea.get()[0] not in ['#','*'] and findObjectFromID(univers.creatures,self.listCrea.get())==None:
                showinfo('Erreur',"Créature inexistante")
                return False
        elif type=='tuer':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+|\*)$",self.listCrea.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'une créature (caractères alpha-numériques et underscore), un mot clé (commencant par #) ou * symbolisant toutes les créatures possibles.")
                return False
            if self.listCrea.get()[0] not in ['#','*'] and findObjectFromID(univers.creatures,self.listCrea.get())==None:
                showinfo('Erreur',"Créature inexistante")
                return False
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+|\*)$",self.listRegion.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'une région (caractères alpha-numériques et underscore), un mot clé (commencant par #) ou * symbolisant toutes les régions possibles.")
                return False
            if self.listRegion.get()[0] not in ['#','*'] and findObjectFromID(univers.regions,self.listRegion.get())==None:
                showinfo('Erreur',"Région inexistante")
                return False
        return True
    def createObjectif(self):
        type=self.type
        if type=='ramasser': self.objectif="ramasser {0} {1} {2} {3}".format(self.listObjet.get(),self.compteurQuantite.get(),self.listRegion.get(),self.heure.get())
        elif type=='entrer': self.objectif="entrer {0} {1} {2}".format(self.listRegion.get(),self.compteurQuantite.get(),self.heure.get())
        elif type=='tuer': self.objectif="tuer {0} {1} {2} {3}".format(self.listCrea.get(),self.compteurQuantite.get(),self.listRegion.get(),self.heure.get())
        elif type=='parler': self.objectif="parler {0} {1} {2}".format(self.listCrea.get(),self.compteurQuantite.get(),self.heure.get())
    def charger(self,objectif):
        if objectif:
            objectif_split = objectif.split()
            self.listType.set(objectif_split[0])
            self.gererType()
            
            if self.type=='ramasser':
                objetID=objectif_split[1]
                self.listObjet.set(objetID)
                quantite=objectif_split[2]
                self.compteurQuantite.delete(0,END)
                self.compteurQuantite.insert(0,quantite)
                regionID=objectif_split[3]
                self.listRegion.set(regionID)
                moment=objectif_split[4]
                self.heure.set(moment)
            elif self.type=='entrer':
                regionID=objectif_split[1]
                self.listRegion.set(regionID)
                quantite=objectif_split[2]
                self.compteurQuantite.delete(0,END)
                self.compteurQuantite.insert(0,quantite)
                moment=objectif_split[3]
                self.heure.set(moment)
            elif self.type=='parler':
                creatureID=objectif_split[1]
                self.listCrea.set(creatureID)
                quantite=objectif_split[2]
                self.compteurQuantite.delete(0,END)
                self.compteurQuantite.insert(0,quantite)
                moment=objectif_split[3]
                self.heure.set(moment)
            elif self.type=='tuer':
                creatureID=objectif_split[1]
                self.listCrea.set(creatureID)
                quantite=objectif_split[2]
                self.compteurQuantite.delete(0,END)
                self.compteurQuantite.insert(0,quantite)
                regionID=objectif_split[3]
                self.listRegion.set(regionID)
                moment=objectif_split[4]
                self.heure.set(moment)            
class AutoScrollbar(ttk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed. Works only for grid geometry manager """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        raise tk.TclError('Cannot use place with the widget ' + self.__class__.__name__)
class CanvasImage:
    """ Display and zoom image """
    def __init__(self, placeholder, path, cell_size):
    
        self.rectangles_IDs=[]
        self.region_selected=""
        self.colors={}
        self.bitmap=StringVar()
        self.mode=""
        self.start_ID=0
        self.size=cell_size
        self.null=False
        
        """ Initialize the ImageFrame """
        self.imscale = 1.0  # scale for the canvas image zoom, public for outer classes
        self.__delta = 2.0  # zoom magnitude
        self.__filter = Image.ANTIALIAS  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS
        self.__previous_state = 0  # previous state of the keyboard
        self.path = path  # path to the image, should be public for outer classes
        # Create ImageFrame in placeholder widget
        self.__imframe = ttk.Frame(placeholder)  # placeholder of the ImageFrame object
        # Vertical and horizontal scrollbars for canvas
        hbar = AutoScrollbar(self.__imframe, orient='horizontal')
        vbar = AutoScrollbar(self.__imframe, orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')
        # Create canvas and bind it with scrollbars. Public for outer classes
        self.canvas = Canvas(self.__imframe, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        hbar.configure(command=self.__scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.__scroll_y)
        
        if path!='':
    
            
            # Bind events to the Canvas
            self.canvas.bind('<Configure>', lambda event: self.__show_image())  # canvas is resized
            self.canvas.bind('<ButtonPress-2>', self.__move_from)  # remember canvas position
            self.canvas.bind('<B2-Motion>',     self.__move_to)  # move canvas to the new position
            self.canvas.bind('<MouseWheel>', self.__wheel)  # zoom for Windows and MacOS, but not Linux
            self.canvas.bind('<Button-5>',   self.__wheel)  # zoom for Linux, wheel scroll down
            self.canvas.bind('<Button-4>',   self.__wheel)  # zoom for Linux, wheel scroll up
            self.canvas.bind("<ButtonPress-1>", self.left_click)
            self.canvas.bind('<B1-Motion>',     self.left_click_motion)
            self.canvas.bind("<ButtonPress-3>", self.right_click)
            self.canvas.bind('<B3-Motion>',     self.right_click_motion)    
            self.canvas.bind('<Motion>',     placeholder.parent.motion)  
            # Handle keystrokes in idle mode, because program slows down on a weak computers,
            # when too many key stroke events in the same time
            self.canvas.bind('<Key>', lambda event: self.canvas.after_idle(self.__keystroke, event))
            # Decide if this image huge or not
            self.__huge = False  # huge or not
            self.__huge_size = 14000  # define size of the huge image
            self.__band_width = 1024  # width of the tile band
            Image.MAX_IMAGE_PIXELS = 1000000000  # suppress DecompressionBombError for the big image
            with warnings.catch_warnings():  # suppress DecompressionBombWarning
                warnings.simplefilter('ignore')
                self.__image = Image.open(self.path)  # open image, but down't load it
            self.imwidth, self.imheight = self.__image.size  # public for outer classes
            if self.imwidth * self.imheight > self.__huge_size * self.__huge_size and \
               self.__image.tile[0][0] == 'raw':  # only raw images could be tiled
                self.__huge = True  # image is huge
                self.__offset = self.__image.tile[0][2]  # initial tile offset
                self.__tile = [self.__image.tile[0][0],  # it have to be 'raw'
                               [0, 0, self.imwidth, 0],  # tile extent (a rectangle)
                               self.__offset,
                               self.__image.tile[0][3]]  # list of arguments to the decoder
            self.__min_side = min(self.imwidth, self.imheight)  # get the smaller image side
            # Create image pyramid
            self.__pyramid = [self.smaller()] if self.__huge else [Image.open(self.path)]
            # Set ratio coefficient for image pyramid
            self.__ratio = max(self.imwidth, self.imheight) / self.__huge_size if self.__huge else 1.0
            self.__curr_img = 0  # current image from the pyramid
            self.__scale = self.imscale * self.__ratio  # image pyramide scale
            self.__reduction = 2  # reduction degree of image pyramid
            w, h = self.__pyramid[-1].size
            while w > 512 and h > 512:  # top pyramid image is around 512 pixels in size
                w /= self.__reduction  # divide on reduction degree
                h /= self.__reduction  # divide on reduction degree
                self.__pyramid.append(self.__pyramid[-1].resize((int(w), int(h)), self.__filter))
            # Put image into container rectangle and use it to set proper coordinates to the image
            self.container = self.canvas.create_rectangle((0, 0, self.imwidth, self.imheight), width=0)
            self.__show_image()  # show image on the canvas
            self.canvas.focus_set()  # set focus on the canvas
            self.build_grid(self.size)
        
        else: self.null=True

        
        
    def smaller(self):
        """ Resize image proportionally and return smaller image """
        w1, h1 = float(self.imwidth), float(self.imheight)
        w2, h2 = float(self.__huge_size), float(self.__huge_size)
        aspect_ratio1 = w1 / h1
        aspect_ratio2 = w2 / h2  # it equals to 1.0
        if aspect_ratio1 == aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(w2)  # band length
        elif aspect_ratio1 > aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(w2 / aspect_ratio1)))
            k = h2 / w1  # compression ratio
            w = int(w2)  # band length
        else:  # aspect_ratio1 < aspect_ration2
            image = Image.new('RGB', (int(h2 * aspect_ratio1), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(h2 * aspect_ratio1)  # band length
        i, j, n = 0, 1, round(0.5 + self.imheight / self.__band_width)
        while i < self.imheight:
            print('\rOpening image: {j} from {n}'.format(j=j, n=n), end='')
            band = min(self.__band_width, self.imheight - i)  # width of the tile band
            self.__tile[1][3] = band  # set band width
            self.__tile[2] = self.__offset + self.imwidth * i * 3  # tile offset (3 bytes per pixel)
            self.__image.close()
            self.__image = Image.open(self.path)  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]  # set tile
            cropped = self.__image.crop((0, 0, self.imwidth, band))  # crop tile band
            image.paste(cropped.resize((w, int(band * k)+1), self.__filter), (0, int(i * k)))
            i += band
            j += 1
        print('\r' + 30*' ' + '\r', end='')  # hide printed string
        return image

    def redraw_figures(self):
        """ Dummy function to redraw figures in the children classes """
        pass

    def grid(self, **kw):
        """ Put CanvasImage widget on the parent widget """
        self.__imframe.grid(**kw)  # place CanvasImage widget on the grid
        self.__imframe.grid(sticky='nswe')  # make frame container sticky
        self.__imframe.rowconfigure(0, weight=1)  # make canvas expandable
        self.__imframe.columnconfigure(0, weight=1)


    def pack(self, **kw):
        """ Exception: cannot use pack with this widget """
        raise Exception('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        """ Exception: cannot use place with this widget """
        raise Exception('Cannot use place with the widget ' + self.__class__.__name__)

    # noinspection PyUnusedLocal
    def __scroll_x(self, *args, **kwargs):
        """ Scroll canvas horizontally and redraw the image """
        self.canvas.xview(*args)  # scroll horizontally
        self.__show_image()  # redraw the image

    # noinspection PyUnusedLocal
    def __scroll_y(self, *args, **kwargs):
        """ Scroll canvas vertically and redraw the image """
        self.canvas.yview(*args)  # scroll vertically
        self.__show_image()  # redraw the image

    def __show_image(self):
        """ Show image on the Canvas. Implements correct image zoom almost like in Google Maps """
        box_image = self.canvas.coords(self.container)  # get image area
        box_canvas = (self.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvas.canvasy(0),
                      self.canvas.canvasx(self.canvas.winfo_width()),
                      self.canvas.canvasy(self.canvas.winfo_height()))
        box_img_int = tuple(map(int, box_image))  # convert to integer or it will not work properly
        # Get scroll region box
        box_scroll = [min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
                      max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]
        # Horizontal part of the image is in the visible area
        if  box_scroll[0] == box_canvas[0] and box_scroll[2] == box_canvas[2]:
            box_scroll[0]  = box_img_int[0]
            box_scroll[2]  = box_img_int[2]
        # Vertical part of the image is in the visible area
        if  box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1]  = box_img_int[1]
            box_scroll[3]  = box_img_int[3]
        # Convert scroll region to tuple and to integer
        self.canvas.configure(scrollregion=tuple(map(int, box_scroll)))  # set scroll region
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = min(box_canvas[2], box_image[2]) - box_image[0]
        y2 = min(box_canvas[3], box_image[3]) - box_image[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            if self.__huge and self.__curr_img < 0:  # show huge image
                h = int((y2 - y1) / self.imscale)  # height of the tile band
                self.__tile[1][3] = h  # set the tile band height
                self.__tile[2] = self.__offset + self.imwidth * int(y1 / self.imscale) * 3
                self.__image.close()
                self.__image = Image.open(self.path)  # reopen / reset image
                self.__image.size = (self.imwidth, h)  # set size of the tile band
                self.__image.tile = [self.__tile]
                image = self.__image.crop((int(x1 / self.imscale), 0, int(x2 / self.imscale), h))
            else:  # show normal image
                image = self.__pyramid[max(0, self.__curr_img)].crop(  # crop current img from pyramid
                                    (int(x1 / self.__scale), int(y1 / self.__scale),
                                     int(x2 / self.__scale), int(y2 / self.__scale)))
            #
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1)), self.__filter))
            imageid = self.canvas.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def __move_from(self, event):
        """ Remember previous coordinates for scrolling with the mouse """
        self.canvas.scan_mark(event.x, event.y)

    def __move_to(self, event):
        """ Drag (move) canvas to the new position """
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.__show_image()  # zoom tile and show it on the canvas

    def outside(self, x, y):
        """ Checks if the point (x,y) is outside the image area """
        bbox = self.canvas.coords(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            return False  # point (x,y) is inside the image area
        else:
            return True  # point (x,y) is outside the image area

    def __wheel(self, event):
        """ Zoom with mouse wheel """
        x = self.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
        y = self.canvas.canvasy(event.y)
        if self.outside(x, y): return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down, smaller
            if round(self.__min_side * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.__delta
            scale        /= self.__delta
        if event.num == 4 or event.delta == 120:  # scroll up, bigger
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height()) >> 1
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.__delta
            scale        *= self.__delta
        # Take appropriate image from the pyramid
        k = self.imscale * self.__ratio  # temporary coefficient
        self.__curr_img = min((-1) * int(math.log(k, self.__reduction)), len(self.__pyramid) - 1)
        self.__scale = k * math.pow(self.__reduction, max(0, self.__curr_img))
        #
        self.canvas.scale('all', x, y, scale, scale)  # rescale all objects
        # Redraw some figures before showing image on the screen
        self.redraw_figures()  # method for child classes
        self.__show_image()

    def __keystroke(self, event):
        """ Scrolling with the keyboard.
            Independent from the language of the keyboard, CapsLock, <Ctrl>+<key>, etc. """
        if event.state - self.__previous_state == 4:  # means that the Control key is pressed
            pass  # do nothing if Control key is pressed
        else:
            self.__previous_state = event.state  # remember the last keystroke state
            # Up, Down, Left, Right keystrokes
            if event.keycode in [68, 39, 102]:  # scroll right, keys 'd' or 'Right'
                self.__scroll_x('scroll',  1, 'unit', event=event)
            elif event.keycode in [65, 37, 100]:  # scroll left, keys 'a' or 'Left'
                self.__scroll_x('scroll', -1, 'unit', event=event)
            elif event.keycode in [87, 38, 104]:  # scroll up, keys 'w' or 'Up'
                self.__scroll_y('scroll', -1, 'unit', event=event)
            elif event.keycode in [83, 40, 98]:  # scroll down, keys 's' or 'Down'
                self.__scroll_y('scroll',  1, 'unit', event=event)

    def crop(self, bbox):
        """ Crop rectangle from the image and return it """
        if self.__huge:  # image is huge and not totally in RAM
            band = bbox[3] - bbox[1]  # width of the tile band
            self.__tile[1][3] = band  # set the tile height
            self.__tile[2] = self.__offset + self.imwidth * bbox[1] * 3  # set offset of the band
            self.__image.close()
            self.__image = Image.open(self.path)  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]
            return self.__image.crop((bbox[0], 0, bbox[2], band))
        else:  # image is totally in RAM
            return self.__pyramid[0].crop(bbox)

    def destroy(self):
        """ ImageFrame destructor """
        if self.null is not True:
            self.__image.close()
            map(lambda i: i.close, self.__pyramid)  # close all pyramid images
            del self.__pyramid[:]  # delete pyramid list
            del self.__pyramid  # delete pyramid variable
        self.canvas.destroy()
        self.__imframe.destroy()

    def build_grid(self, size = 10): 
        height = self.imheight
        width = self.imwidth
        nbr_column=math.ceil(width/size)
        nbr_lines=math.ceil(height/size)
        self.start_ID=nbr_column+nbr_lines+1
        for y in range(0, nbr_lines-1):
            self.rectangles_IDs.append([])
            for x in range(0, nbr_column-1):
                self.rectangles_IDs[y].append(self.canvas.create_rectangle(x*size,y*size,(x+1)*size,(y+1)*size, fill="", outline="",tag="empty",dash=(3, 5)))
    def left_click(self, event):
        if self.mode == "pen" or self.mode =="brush":
            x,y=self.canvas.canvasx(event.x),self.canvas.canvasy(event.y)
            h=self.size*self.imscale
            items=self.canvas.find_enclosed(x-h,y-h,x+h,y+h)
            if len(items) != 1: return
            self.add_region(items[0])
        elif self.mode == "move" : self.__move_from(event)

    def left_click_motion(self, event):
        if self.mode == "move": self.__move_to(event)
        elif self.mode == "brush": self.left_click(event)
        
    def right_click(self, event):
        if self.mode == "pen" or self.mode =="brush":
            x,y=self.canvas.canvasx(event.x),self.canvas.canvasy(event.y)
            h=self.size*self.imscale
            items=self.canvas.find_enclosed(x-h,y-h,x+h,y+h)
            if len(items) != 1: return
            self.remove_region(items[0])
        elif self.mode == "move" : self.__move_from(event)
        
    def right_click_motion(self, event):
        if self.mode == "brush": self.right_click(event)
    
    def find_coord(self, x, y):
        x,y=self.canvas.canvasx(x),self.canvas.canvasy(y)
        if self.outside(x,y) : return 0,0
        h=self.size*self.imscale
        items=self.canvas.find_enclosed(x-h,y-h,x+h,y+h)
        if len(items) != 1: return 0,0
        id=items[0]
        y=0
        for list in self.rectangles_IDs:
            x=0
            for i in self.rectangles_IDs[y]:
                if i == id: return x,y
                x+=1
            y+=1
        return 0,0
    
    def add_region(self,id):
        if self.region_selected in self.colors :
            self.canvas.itemconfig(id, fill=self.colors[self.region_selected],stipple=self.bitmap.get(),tag=(self.region_selected,"rectangle"))
        else : showinfo('','Veuillez sélectionner une couleur pour cette région')
    def remove_region(self,id):
        self.canvas.itemconfig(id, fill="",tag=("empty"))
    
    def change_regionColor(self):
        if self.region_selected!="": self.canvas.itemconfig(self.region_selected, fill=self.colors[self.region_selected],stipple=self.bitmap.get(),tag=(self.region_selected,"rectangle"))
   
    def remove_regions(self):
        self.canvas.itemconfig(self.region_selected, fill="",tag="empty")
            
    def remove_all(self):
        self.canvas.itemconfig("rectangle", fill="",tag="empty")  
class MapEditor(Frame):
      
    def __init__(self,parent,**kw):
        Frame.__init__(self,master=parent, **kw)
        self.frameViewer=Frame(self)
        self.frameViewer.rowconfigure(0, weight=1)
        self.frameViewer.columnconfigure(0, weight=1)
        self.frameViewer.pack(side=LEFT,fill=BOTH,expand=1)
        self.frameViewer.parent=self
        self.viewer=CanvasImage(self.frameViewer, "", 0)
        self.viewer.grid(row=0,column=0)
        self.frameEdit=Frame(self,width=700)
        self.frameEdit.pack(side=RIGHT,fill=Y)
        self.frameTools=LabelFrame(self.frameEdit,text="Outils")
        self.frameTools.pack(pady=5)
        self.frameTools1=Frame(self.frameTools)
        self.frameTools1.pack(side=TOP)
        self.frameTools2=Frame(self.frameTools)
        self.frameTools2.pack(side=BOTTOM)
        self.button_move = Button(self.frameTools1,text="Déplacer",command=self.modeMove)
        self.button_move.pack(side=LEFT)
        self.button_pen = Button(self.frameTools1,text="Crayon",command=self.modePen,state="disabled")
        self.button_pen.pack(side=LEFT)
        self.button_brush = Button(self.frameTools1,text="Pinceau",command=self.modeBrush,state="disabled")        
        self.button_brush.pack(side=LEFT)
        self.label_coord = Label(self.frameTools2,text="0.0",state="disabled")
        self.label_coord.pack(side=RIGHT)
        self.frameSelect=LabelFrame(self.frameEdit,text="Région selectionnée")
        self.frameSelect.pack(pady=5,padx=5)
        self.frameSelect1=Frame(self.frameSelect)
        self.frameSelect1.pack(side=TOP)
        self.frameSelect2=Frame(self.frameSelect)
        self.frameSelect2.pack(side=BOTTOM)
        self.region_list=AutocompleteCombobox(self.frameSelect1)
        self.region_list.set_completion_list([region.id for region in univers.regions])
        self.region_list.bind('<<ComboboxSelected>>',self.region_select)
        self.region_list.pack(side=LEFT)
        self.button_color = Button(self.frameSelect1,text="Color",background="grey",command=self.changeColor,state="disabled")
        self.button_color.pack(side=RIGHT)
        self.viewer.bitmap.set('gray12')
        self.button_gray12 = Radiobutton(self.frameSelect2,text="",bitmap='gray12',variable=self.viewer.bitmap,value="gray12",indicatoron=0,command=self.changeBitmap)
        self.button_gray12.pack(side=LEFT,padx=5)
        self.button_gray25 = Radiobutton(self.frameSelect2,text="",bitmap='gray25',variable=self.viewer.bitmap,value="gray25",indicatoron=0,command=self.changeBitmap)
        self.button_gray25.pack(side=LEFT,padx=5)
        self.button_gray50 = Radiobutton(self.frameSelect2,text="",bitmap='gray50',variable=self.viewer.bitmap,value="gray50",indicatoron=0,command=self.changeBitmap)
        self.button_gray50.pack(side=LEFT,padx=5)
        self.button_gray75 = Radiobutton(self.frameSelect2,text="",bitmap='gray75',variable=self.viewer.bitmap,value="gray75",indicatoron=0,command=self.changeBitmap)
        self.button_gray75.pack(side=LEFT,padx=5)
        self.button_reinitializeRegion = Button(self.frameEdit,text="Supprimer les emplacements",command=self.viewer.remove_regions)
        self.button_reinitializeRegion.pack(pady=5)
        self.button_modify = Button(self.frameEdit,text="Modifier les régions",command=self.modifyRegions)
        self.button_modify.pack(pady=5)
        self.showGrid=BooleanVar()
        self.showGrid.set(False)
        self.button_hideGrid = Checkbutton(self.frameEdit,text="Afficher la grille",variable=self.showGrid,offvalue=False,onvalue=True,command=self.hideGrid)
        self.button_hideGrid.pack(pady=5)
        
    def hideGrid(self):
        if self.showGrid.get()==False:
            self.viewer.canvas.itemconfig('empty',outline='')
            self.viewer.canvas.itemconfig('rectangle',outline='')
        else:
            self.viewer.canvas.itemconfig('empty',outline='black')
            self.viewer.canvas.itemconfig('rectangle',outline='black')
        
    def changeBitmap(self): self.viewer.change_regionColor()
        
    def newImg(self): 
        path = askopenfilename()
        if path:
            if re.match(r"^([A-z0-9-_:]+\/)([A-z0-9-_ +]+\/)+([A-z0-9-_ +]+\.(png|ppm|jpg|jpeg|gif|tiff|bmp))$",path):
                cell_size=simpledialog.askinteger("Taille (en px)","Choisissez la taille d'une région",parent=self,minvalue=1)
                if cell_size is not None:
                    for i in self.viewer.canvas.find_all(): self.viewer.canvas.delete(i)
                    self.viewer.destroy()
                    self.viewer.__init__(self.frameViewer,path,cell_size)
                    self.viewer.grid(row=0,column=0)
                    self.viewer.bitmap=StringVar()
                    self.viewer.bitmap.set("gray50")
                    self.button_gray12.config(variable=self.viewer.bitmap)
                    self.button_gray25.config(variable=self.viewer.bitmap)
                    self.button_gray50.config(variable=self.viewer.bitmap)
                    self.button_gray75.config(variable=self.viewer.bitmap)
                    self.button_brush.config(state="disabled",relief="raised")
                    self.button_pen.config(state="disabled",relief="raised")
                    self.button_move.config(relief="raised")
                    self.button_color.config(background="grey",state="disabled")
                    self.viewer.mode=""
                    self.region_list.set("")
                    self.showGrid.set(False)
    def region_select(self,event):
        if self.region_list.get()== "":
            self.viewer.mode=""
            self.viewer.region_selected=""
            self.button_brush.config(state="disabled")
            self.button_pen.config(state="disabled")
            self.button_pen.config(relief="raised")
            self.button_brush.config(relief="raised")
            self.button_move.config(relief="raised")
        else:
            self.button_brush.config(state="normal")
            self.button_pen.config(state="normal")
            self.button_color.config(state="normal")
            self.viewer.region_selected=self.region_list.get()
            if self.viewer.region_selected in self.viewer.colors : self.button_color.config(background=self.viewer.colors[self.viewer.region_selected])
            else : self.button_color.config(background="grey")
            
    def modeMove(self):
        self.button_pen.config(relief="flat")
        self.button_brush.config(relief="flat")
        self.button_move.config(relief="ridge")
        self.viewer.mode="move"
    def modePen(self):
        self.button_pen.config(relief="ridge")
        self.button_brush.config(relief="flat")
        self.button_move.config(relief="flat")
        self.viewer.mode="pen"
    def modeBrush(self):
        self.button_pen.config(relief="flat")
        self.button_brush.config(relief="ridge")
        self.button_move.config(relief="flat")
        self.viewer.mode="brush"
    def rgb2hex(self,r,g,b):
        return "#{:02x}{:02x}{:02x}".format(r,g,b)
    def changeColor(self): 
        color = askcolor(title="Choix d'une couleur",initialcolor=self.button_color['background'])
        if color[0]:
            r,g,b=int(color[0][0]),int(color[0][1]),int(color[0][2])
            colorhexa=self.rgb2hex(r,g,b)
            self.viewer.colors[self.viewer.region_selected]=colorhexa
            self.button_color.config(background=colorhexa)
            self.viewer.change_regionColor()
    def motion(self,event):
        coords=self.viewer.find_coord(event.x,event.y)
        self.label_coord.config(text=str(coords[0])+','+str(coords[1]))
        
    def modifyRegions(self):
        result=windowRegion(self).result

        id_regions=list(self.region_list['values'])
        for region in univers.regions:
            if region.id not in id_regions:
                id_regions.append(region.id)
        for region in id_regions:
            if findObjectFromID(univers.regions,region)==None:
                self.viewer.remove_region(region)
                id_regions.remove(region)
        self.region_list.set_completion_list(id_regions)
        self.viewer.mode=""
        self.button_move.config(state="disabled")
        self.button_pen.config(state="disabled")
        self.button_brush.config(state="disabled")
            
    def refresh(self): pass    
    def buildUnivers(self): pass  
class FrameDialog(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.dialogues = {}
        self.createWidgets()
        self.childList=[]
    def createWidgets(self):
        self.frameTop=Frame(self)
        self.frameTop.pack(side=TOP,fill=BOTH,expand=1)
        self.listDialogue=ttk.Treeview(self.frameTop,height=25,columns=['rep'])
        self.listDialogue.heading('#0',text="Dialogues")
        self.listDialogue.column('#0',width=150)
        self.listDialogue.column('#1',width=250)
        self.listDialogue.heading('rep',text="Texte réponse")
        self.listDialogue.bind('<<TreeviewSelect>>',self.Charger)
        self.listDialogue.pack(side=LEFT,fill=BOTH,expand=1)
        self.frameDial = LabelFrame(self.frameTop,text="Dialogue")
        self.frameDial.pack(side=LEFT,fill=BOTH,expand=1)
        self.labelText=Label(self.frameDial,text="Texte")
        self.text=Text(self.frameDial,width=50,height=15)
        self.frameConditions=FrameConditions(self.frameDial,text="Conditions du choix")
        self.frameEffets=FrameEffets(self.frameDial,text="Effets du choix")
        self.labelText.pack(fill=BOTH)
        self.text.pack(fill=BOTH)
        self.frameConditions.pack(fill=BOTH)
        self.frameEffets.pack(fill=BOTH)
        self.frameBoutons=Frame(self)
        self.frameBoutons.pack(side=TOP,expand=1)
        self.boutonSupprimer=Button(self.frameBoutons,text="Supprimer",command=self.Supp)
        self.boutonEnregistrer=Button(self.frameBoutons,text="Enregistrer",command=self.Enregistrer)
        self.boutonAjouterDial=Button(self.frameBoutons,text="Ajouter un dialogue",command=self.AjouterDial)
        self.boutonAjouterReponse=Button(self.frameBoutons,text="Ajouter une réponse",command=self.AjouterRep)
        self.boutonModifierReponse=Button(self.frameBoutons,text="Modifier la réponse",command=self.ModifierRep)
        self.boutonSaveDial=Button(self.frameBoutons,text="Sauvegarder les dialogues",command=self.saveDialogs)
        self.boutonSupprimer.pack(side=LEFT)
        self.boutonEnregistrer.pack(side=LEFT)
        self.boutonAjouterDial.pack(side=LEFT)
        self.boutonAjouterReponse.pack(side=LEFT)
        self.boutonModifierReponse.pack(side=LEFT)
        self.boutonSaveDial.pack(side=LEFT)
    def Supp(self): 
        sel = self.listDialogue.selection()
        if sel: 
            if askokcancel('',"Supprimer ce dialogue supprimera également les dialogues qu'il contient. Continuer ?"):
                self.childList=[]
                self.get_Child(sel[0])
                for iid in self.childList:
                    del self.dialogues[iid]
                self.listDialogue.delete(sel)
                
    def buildDialog(self,parent):
        dialog=copy.deepcopy(self.dialogues[parent])
        for item in self.listDialogue.get_children(parent):
            dialog.reponses[self.listDialogue.item(item)['values'][0]]=self.buildDialog(item)
        return dialog
    def saveDialogs(self):
        del univers.dialogues
        univers.dialogues = {}
        for dial in self.listDialogue.get_children(''):
            univers.dialogues[dial]=self.buildDialog(dial)
            univers.dialogues[dial].id=dial
        '''for id,dialogue in univers.dialogues.items():
            for reponse,dial in dialogue.reponses.items():
                print("    "+reponse+dial.text)
                for rep,d in dial.reponses.items():
                    print("        "+rep+d.text)'''
    def loadDialogs(self):
        self.dialogues={}
        for item in self.listDialogue.get_children(''): self.listDialogue.delete(item)
        for ID,dial in univers.dialogues.items():
            self.listDialogue.insert("",END,ID,text=ID)
            self.dialogues[ID]=dial
            self.create_dialog(ID,dial)
    def create_dialog(self,parent,dial):
        for reponse,dialogue in dial.reponses.items(): 
            ID=self.listDialogue.insert(parent,END,values=[reponse])
            self.listDialogue.item(ID,text=ID)
            self.dialogues[ID]=dialogue
            self.create_dialog(ID,dialogue)
    def get_Child(self,iid):
        self.childList.append(iid)
        if self.listDialogue.get_children(iid):
            for children in self.listDialogue.get_children(iid):
                self.get_Child(children)
    def Enregistrer(self):
        sel = self.listDialogue.selection()
        if sel:
            self.dialogues[sel[0]].text=self.text.get(0.0,END)
            self.dialogues[sel[0]].conditionsChoix=self.frameConditions.conditions
            self.dialogues[sel[0]].effetsChoix=self.frameEffets.effets
        else: showinfo('','Veuillez sélectionner le dialogue à modifier.')
    def Charger(self,event):
        sel = self.listDialogue.selection()
        self.text.delete(0.0,END)
        self.text.insert(0.0,self.dialogues[sel[0]].text)
        self.frameConditions.clear()
        if self.dialogues[sel[0]].conditionsChoix: self.frameConditions.update(self.dialogues[sel[0]].conditionsChoix)
        self.frameEffets.clear()
        if self.dialogues[sel[0]].effetsChoix: self.frameEffets.update(self.dialogues[sel[0]].effetsChoix)
    def AjouterDial(self): 
        result = askCaracteristique(self).result
        if result:
            self.listDialogue.insert('',END,result,text=result)
            self.dialogues[result]=Dialogue()
    def AjouterRep(self):
        sel = self.listDialogue.selection()
        if sel: 
            result = askReponse(self).result
            if result: 
                iid=self.listDialogue.insert(sel[0],END,text="#",values=[result])
                self.listDialogue.item(iid,text=iid)
                self.dialogues[iid]=Dialogue()
    def ModifierRep(self):
        sel = self.listDialogue.selection()
        if sel and self.listDialogue.parent(sel)!='':
            result = askReponse(self).result
            if result: self.listDialogue.item(sel,values=[result])
    def refresh(self): 
        self.saveDialogs()
class FrameObject(Frame):
    def __init__(self,parent,type=''):
        LabelFrame.__init__(self,parent)
        if type=='action': self.listObject=univers.actions
        elif type=="objet": self.listObject=univers.objets
        elif type=="creature": self.listObject=univers.creatures
        elif type=="region":self.listObject=univers.regions
        self.type=type
        self.object=None
        self.sel=None
        self.mode="nouveau"
        self.createWidgets()
        self.ChargerList()
    def refresh(self):
        if self.type=="creature": 
            self.frameAmisAvec.updateChoices()
            self.frameInventaire.updateChoices()
            self.frameActions.updateChoices()
            listDial=[""]+[id for id in univers.dialogues.keys()]
            if self.listDialogue.get() not in listDial: self.listDialogue.set("")
            self.listDialogue.set_completion_list(listDial)
        elif self.type=="region":
            self.frameCreaR.updateChoices()
            self.listParent.set_completion_list(["Aucune"]+[region.id for region in univers.regions])
    def createWidgets(self):
        self.zoneList=LabelFrame(self)
        self.zoneList.pack(side=LEFT,fill=Y)

        self.list=Listbox(self.zoneList,width=50,height=40)
        self.list.bind('<<ListboxSelect>>',self.SelectionnerElement)
        self.list.pack(fill=Y,expand=1)

        self.frameBoutons = Frame(self)
        self.frameBoutons.pack(fill=BOTH,expand=1)
        self.boutonSupprimer=Button(self.zoneList,text='Supprimer',command=self.Supprimer,state=DISABLED)
        self.boutonEnregistrer=Button(self.zoneList,text='Enregistrer',command=self.Enregistrer)
        self.boutonNouveau=Button(self.zoneList,text='Nouveau',command=self.Nouveau,state=DISABLED)
        self.boutonSupprimer.pack(side=LEFT)
        self.boutonEnregistrer.pack(side=LEFT,padx=85)
        self.boutonNouveau.pack(side=RIGHT)
    
        self.zoneEditeur=Frame(self)
        self.zoneEditeur.pack(side=LEFT,expand=1,fill=BOTH)

        self.frameDescription = FrameDescription(self.zoneEditeur,text="Description")
        self.frameDescription.pack(fill=BOTH,expand=1)
        
        if self.type=="action":
            self.frameEffCond=Frame(self.zoneEditeur)
            self.frameEffCond.pack(fill=BOTH,expand=1)
            self.frameEffets=FrameEffets(self.frameEffCond,text='Effets')
            self.frameEffets.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameConditions=FrameConditions(self.frameEffCond,text='Conditions')
            self.frameConditions.pack(side=RIGHT,expand=1,fill=BOTH)
        elif self.type=="objet":
            self.frameEffCond=Frame(self.zoneEditeur)
            self.frameEffCond.pack(fill=BOTH,expand=1)
            self.frameEffets=Frame(self.frameEffCond)
            self.frameEffets.pack(side=TOP,fill=BOTH,expand=1)
            self.frameEffetsPoss=FrameEffets(self.frameEffets,text="Effets de possession")
            self.frameEffetsPoss.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameEffetsEquip=FrameEffets(self.frameEffets,text="Effets en l'équipant")
            self.frameEffetsEquip.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameEffetsUtil=FrameEffets(self.frameEffets,text="Effets en l'utilisant")
            self.frameEffetsUtil.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameConditions=Frame(self.frameEffCond)
            self.frameConditions.pack(side=TOP,fill=BOTH,expand=1)
            self.frameConditionsPoss=FrameConditions(self.frameConditions,text="Conditions de possession")
            self.frameConditionsPoss.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameConditionsEquip=FrameConditions(self.frameConditions,text="Conditions d'équipement")
            self.frameConditionsEquip.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameConditionsUtil=FrameConditions(self.frameConditions,text="Conditions d'utilisation")
            self.frameConditionsUtil.pack(side=LEFT,expand=1,fill=BOTH)
            
            self.frameEffetsEquip.boutonAjouter.config(state=DISABLED)
            self.frameEffetsEquip.boutonSupprimer.config(state=DISABLED)
            self.frameConditionsEquip.boutonAjouter.config(state=DISABLED)
            self.frameConditionsEquip.boutonSupprimer.config(state=DISABLED)
            self.frameEffetsUtil.boutonAjouter.config(state=DISABLED)
            self.frameEffetsUtil.boutonSupprimer.config(state=DISABLED)
            self.frameConditionsUtil.boutonAjouter.config(state=DISABLED)
            self.frameConditionsUtil.boutonSupprimer.config(state=DISABLED)
        elif self.type=="creature":
            self.frameCaract = FrameCaract(self.zoneEditeur,text="Caractéristique",type='Creature')
            self.frameCaract.pack(fill=BOTH,expand=1)
            self.frameInvActions = Frame(self.zoneEditeur)
            self.frameInvActions.pack(fill=BOTH,expand=1,side=TOP)
            self.frameInventaire = FrameList(self.frameInvActions,text="Inventaire",type='objet')
            self.frameActions = FrameList(self.frameInvActions,text="Actions",type='action')
            self.frameInventaire.pack(side=LEFT,fill=BOTH,expand=1)
            self.frameActions.pack(side=LEFT,fill=BOTH,expand=1)
            self.frameAmDial=Frame(self.zoneEditeur)
            self.frameAmDial.pack(fill=BOTH,expand=1,side=TOP)
            self.frameAmisAvec = FrameList(self.frameAmDial,text="Affinités",type='creature')
            self.frameAmisAvec.pack(side=LEFT,fill=BOTH,expand=1)
            self.frameDialogue = LabelFrame(self.frameAmDial,text="Dialogue")
            self.frameDialogue.pack(side=LEFT,fill=BOTH,expand=1)
            self.listDialogue = AutocompleteCombobox(self.frameDialogue)
            self.listDialogue.set_completion_list([""]+[id for id in univers.dialogues.keys()])
            self.listDialogue.pack(expand=1)
        elif self.type=="region":
            self.frameConditions=Frame(self.zoneEditeur)
            self.frameConditions.pack(side=TOP,fill=BOTH,expand=1)
            self.frameConditionsEntrer=FrameConditions(self.frameConditions,text="Conditions d'entrée")
            self.frameConditionsEntrer.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameConditionsSortir=FrameConditions(self.frameConditions,text="Conditions de sortie")
            self.frameConditionsSortir.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameEffetsCrea=Frame(self.zoneEditeur)
            self.frameEffetsCrea.pack(side=TOP,fill=BOTH,expand=1)
            self.frameEffets=FrameEffets(self.frameEffetsCrea,text="Effets d'entrée")
            self.frameEffets.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameCreaR=FrameList(self.frameEffetsCrea,text="Créatures rencontrables",type="creature")
            self.frameCreaR.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameRegionContent=Frame(self.zoneEditeur)
            self.frameRegionContent.pack(side=TOP,fill=BOTH,expand=1)
            self.frameObjets=FrameObjetOrCrea(self.frameRegionContent,type="objet",text="Objets")
            self.frameObjets.pack(side=LEFT,expand=1,fill=BOTH)
            self.frameCreatures=FrameObjetOrCrea(self.frameRegionContent,type="creature",text="Créatures")
            self.frameCreatures.pack(side=LEFT,expand=1,fill=BOTH)
            self.framePortails=FrameObjetOrCrea(self.frameRegionContent,type="portail",text="Portails")
            self.framePortails.pack(side=LEFT,expand=1,fill=BOTH)
            
        self.frameOptions=LabelFrame(self.zoneEditeur,text='Options')
        self.frameOptions.pack(fill=BOTH,expand=1)

        if self.type=="action":
            self.labelTypeAction = Label(self.frameOptions,text='Type :')
            self.labelCibleAction = Label(self.frameOptions,text='Cible :')
            self.labelUtilAction = Label(self.frameOptions,text='Utilisation :')
            self.labeltIncantAction = Label(self.frameOptions,text="Temps d'incantation :")
            self.labelEtatIncantAction = Label(self.frameOptions,text="Etat d'incantation :")
            self.RatableAction=BooleanVar()
            self.RatableAction.set(True)
            self.boutonRatableAction=Checkbutton(self.frameOptions,text='Ratable ?',onvalue=True,offvalue=False,variable=self.RatableAction)
            self.EsquivableAction=BooleanVar()
            self.EsquivableAction.set(True)
            self.boutonEsquivableAction=Checkbutton(self.frameOptions,text="Permettre l'esquive ?",onvalue=True,offvalue=False,variable=self.EsquivableAction)
            self.typeAction=StringVar()
            self.cibleAction=StringVar()
            self.utilAction=StringVar()
            self.etatIncantAction=StringVar()
            self.listTypeAction=OptionMenu(self.frameOptions,self.typeAction,*['0: Attaque', '1: Soin', '2: Buff'])
            self.typeAction.set('0: Attaque')
            self.listCibleAction=OptionMenu(self.frameOptions,self.cibleAction,*['0: Lanceur', '1: Autre'])
            self.cibleAction.set('0: Lanceur')
            self.listUtilAction=OptionMenu(self.frameOptions,self.utilAction,*["0: N'importe quand", "1: En dehors d'un combat", '2: En combat'])
            self.utilAction.set("0: N'importe quand")
            self.listEtatIncantAction=OptionMenu(self.frameOptions,self.etatIncantAction,*['-1: aucun changement','0: mort','1: en forme','2: fatigué','3: immobilisé','4: gelé','5: inconscient'])
            self.etatIncantAction.set('-1: aucun changement')
            self.compteurtIncantAction=Spinbox(self.frameOptions,from_=0,to=100)
            self.labelTypeAction.grid(row=0,column=0)
            self.listTypeAction.grid(row=0,column=1)
            self.labelCibleAction.grid(row=0,column=2)
            self.listCibleAction.grid(row=0,column=3)
            self.labelUtilAction.grid(row=0,column=4)
            self.listUtilAction.grid(row=0,column=5)
            self.labelEtatIncantAction.grid(row=1,column=0)
            self.listEtatIncantAction.grid(row=1,column=1)
            self.labeltIncantAction.grid(row=1,column=2)
            self.compteurtIncantAction.grid(row=1,column=3)
            self.boutonRatableAction.grid(row=1,column=4)
            self.boutonEsquivableAction.grid(row=1,column=5)
        elif self.type=="objet":
            self.labelPoidsObjet = Label(self.frameOptions,text="Poids :")
            self.labelPrixObjet = Label(self.frameOptions,text="Prix :")
            self.labelFonctionObjet = Label(self.frameOptions,text="Fonction :")
            self.labelNbrUtilObjet = Label(self.frameOptions,text="Nombre d'utilisation")
            self.labelEmplacementObjet = Label(self.frameOptions,text="Emplacement d'équipement")
            self.compteurPoidsObjet = Spinbox(self.frameOptions,from_=0.0,to=100000.0,increment=0.1)
            self.compteurPrixObjet = Spinbox(self.frameOptions,from_=0.0,to=1000000.0,increment=1)
            self.fonctionObjet=StringVar()
            self.fonctionObjet.set('0: Non équipable et non utilisable (ex: tableau)')
            self.listFonctionObjet=OptionMenu(self.frameOptions,self.fonctionObjet,*['0: Non équipable et non utilisable (ex: tableau)',"1: Equipable mais non utilisable (ex: armure)","2: Non équipable mais utilisable (ex: potion)"],command=self.GererFonctionObjet)
            self.compteurNbrUtilObjet = Spinbox(self.frameOptions,from_=0,to=1000,state=DISABLED)
            self.emplacementObjet=StringVar()
            self.entryEmplacementObjet=Entry(self.frameOptions,textvariable=self.emplacementObjet,state=DISABLED)
            self.labelFonctionObjet.grid(row=0,column=0)
            self.listFonctionObjet.grid(row=0,column=1)
            self.labelPrixObjet.grid(row=0,column=2)
            self.compteurPrixObjet.grid(row=0,column=3)
            self.labelPoidsObjet.grid(row=0,column=4)
            self.compteurPoidsObjet.grid(row=0,column=5)
            self.labelNbrUtilObjet.grid(row=1,column=0)
            self.compteurNbrUtilObjet.grid(row=1,column=1)
            self.labelEmplacementObjet.grid(row=1,column=3)
            self.entryEmplacementObjet.grid(row=1,column=4)
        elif self.type=="creature":
            self.labelNiveauCrea=Label(self.frameOptions,text="Niveau :")
            self.labelExpWinCrea=Label(self.frameOptions,text="Expérience gagnée en le tuant :")
            self.labelCorruptibleCrea=Label(self.frameOptions,text="Corruptible :")
            self.labelEtatCrea=Label(self.frameOptions,text="Etat :")
            self.labelStratOff=Label(self.frameOptions,text="Stratégie offensive :")
            self.labelStratDef=Label(self.frameOptions,text="Stratégie défensive :")
            self.rompreIncantCrea=BooleanVar()
            self.rompreIncantCrea.set(True)
            self.checkRompreIncantCrea=Checkbutton(self.frameOptions,text="Peut rompre une incantation ?",onvalue=True,offvalue=False,variable=self.rompreIncantCrea)
            self.labelHostilCrea=Label(self.frameOptions,text="Hostilité :")
            self.labelMalusFuiteCrea=Label(self.frameOptions,text="Malus de fuite infligé :")
            self.compteurLvlCrea=Spinbox(self.frameOptions,from_=1,to=1000000,increment=1)
            self.compteurLvlCrea.delete(0,END)
            self.compteurLvlCrea.insert(0,"0")
            self.compteurExpWinCrea=Spinbox(self.frameOptions,from_=1,to=1000000,increment=1)
            self.compteurExpWinCrea.delete(0,END)
            self.compteurExpWinCrea.insert(0,"0")
            self.corruptibleCrea=StringVar()
            self.etatCrea=StringVar()
            self.stratOffCrea=StringVar()
            self.stratDefCrea=StringVar()
            self.hostilCrea=StringVar()
            self.listCorruptibleCrea=OptionMenu(self.frameOptions,self.corruptibleCrea,*["0: non", "1: par l'argent", "2: par la séduction", "3: par l'argent et la séduction"])
            self.listEtatCrea=OptionMenu(self.frameOptions,self.etatCrea,*['0: mort','1: en forme','2: fatigué','3: immobilisé','4: gelé','5: inconscient'])
            self.listStratOffCrea=OptionMenu(self.frameOptions,self.stratOffCrea,*["0: lâche - attaque toujours les plus faibles", "1: honorable - attaque toujours les plus forts", "2: ciblée - attaque toujours un même créature choisie au hasard", "3: hasardeuse - attaque les créatures au hasard"])
            self.listStratDefCrea=OptionMenu(self.frameOptions,self.stratDefCrea,*["0: sacrifice - la créature n'hésite pas à mourir tant qu'elle inflige le plus de dommage possible", "1: offensive - la créature utilise des sorts de soins dès qu'il lui reste -20% de sa vie", "2: équilibrée - la créature utilise des sorts de soins dès qu'il lui reste -50% de sa vie", "3: défensive - la créature utilise des sorts de soins dès qu'elle n'a pas toute sa vie", "4: totale - la créature utilise tout le temps des sorts de soins"])
            self.listHostilCrea=OptionMenu(self.frameOptions,self.hostilCrea,*["0: très farouche - s'enfuit à vue du joueur", "1: farouche - s'enfuit à vue de comba", "2: peureux - s'enfuit en combat", "3: passif - n'attaque jamais et ne fuie pas", "4: neutre - attaque de représaille", "5: défenseur - attaque à vue de combat", "6: hostile - attaque le joueur à vue", "7: agressif - attaque tout le monde à vue"])
            self.compteurMalusFuiteCrea=Spinbox(self.frameOptions,from_=1,to=1000000,increment=1)
            self.compteurMalusFuiteCrea.delete(0,END)
            self.compteurMalusFuiteCrea.insert(0,"0")
            
            self.listStratOffCrea.config(width=15)
            self.listStratDefCrea.config(width=15)
            self.listEtatCrea.config(width=15)
            self.listCorruptibleCrea.config(width=15)
            self.listHostilCrea.config(width=15)
            self.stratOffCrea.set("2: ciblée - attaque toujours un même créature choisie au hasard")
            self.stratDefCrea.set("2: équilibrée - la créature utilise des sorts de soins dès qu'il lui reste -50% de sa vie")
            self.etatCrea.set("1: en forme")
            self.corruptibleCrea.set("0: non")
            self.hostilCrea.set("4: neutre - attaque de représaille")
            
            self.labelNiveauCrea.grid(row=0,column=0)
            self.compteurLvlCrea.grid(row=0,column=1)
            self.labelExpWinCrea.grid(row=0,column=2)
            self.compteurExpWinCrea.grid(row=0,column=3)
            self.labelMalusFuiteCrea.grid(row=0,column=4)
            self.compteurMalusFuiteCrea.grid(row=0,column=5)
            self.labelEtatCrea.grid(row=1,column=0)
            self.listEtatCrea.grid(row=1,column=1)
            self.labelHostilCrea.grid(row=1,column=2)
            self.listHostilCrea.grid(row=1,column=3)
            self.labelCorruptibleCrea.grid(row=1,column=4)
            self.listCorruptibleCrea.grid(row=1,column=5)
            self.labelStratOff.grid(row=2,column=0)
            self.listStratOffCrea.grid(row=2,column=1)
            self.labelStratDef.grid(row=2,column=2)
            self.listStratDefCrea.grid(row=2,column=3)
            self.checkRompreIncantCrea.grid(row=2,column=4,columnspan=2,sticky='nsew')
        elif self.type=="region":
            self.frameFactDep=Frame(self.frameOptions)
            self.frameFactDep.pack(side=LEFT,expand=1)
            self.labelFactDep=Label(self.frameFactDep,text="Modificateur de vitesse")
            self.compteurFactDep=Spinbox(self.frameFactDep,from_=0.00001,to=1000000,increment=0.1)
            self.compteurFactDep.delete(0,END)
            self.compteurFactDep.insert(0,"1.0")
            self.labelFactDep.pack(side=LEFT,padx=5)
            self.compteurFactDep.pack(side=LEFT,padx=5)
            self.labelParent=Label(self.frameFactDep,text="Région parente")
            self.listParent=AutocompleteCombobox(self.frameFactDep)
            self.listParent.set_completion_list(["Aucune"]+[region.id for region in univers.regions])
            self.labelParent.pack(side=LEFT,padx=5)
            self.listParent.pack(side=LEFT,padx=5)
            self.labelDir=Label(self.frameFactDep,text="Directions empruntables")
            self.labelDir.pack(side=LEFT,padx=5)
            self.frameDir=Frame(self.frameOptions)
            self.frameDir.pack(side=LEFT,expand=1)
            self.direction=[BooleanVar(value=True) for i in range(0,8)]
            chemin="@"+"\\".join(__file__.split('\\')[0:-1])
            self.buttonUp=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\up.xbm",variable=self.direction[0],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonUp.grid(row=0,column=1)
            self.buttonUpRight=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\up-right.xbm",variable=self.direction[1],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonUpRight.grid(row=0,column=2)
            self.buttonRight=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\right.xbm",variable=self.direction[2],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonRight.grid(row=1,column=2)
            self.buttonDownRight=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\down-right.xbm",variable=self.direction[3],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonDownRight.grid(row=2,column=2)
            self.buttonDown=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\down.xbm",variable=self.direction[4],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonDown.grid(row=2,column=1)
            self.buttonDownLeft=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\down-left.xbm",variable=self.direction[5],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonDownLeft.grid(row=2,column=0)
            self.buttonLeft=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\left.xbm",variable=self.direction[6],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonLeft.grid(row=1,column=0)
            self.buttonUpLeft=Checkbutton(self.frameDir,text="",bitmap=chemin+"\\bitmap\\up-left.xbm",variable=self.direction[7],onvalue=True,indicatoron=0,offvalue=False)
            self.buttonUpLeft.grid(row=0,column=0)           
    def GererFonctionObjet(self,event=None):
        fonction=self.fonctionObjet.get()[0]
        self.frameEffetsEquip.boutonAjouter.config(state=DISABLED)
        self.frameEffetsEquip.boutonSupprimer.config(state=DISABLED)
        self.frameConditionsEquip.boutonAjouter.config(state=DISABLED)
        self.frameConditionsEquip.boutonSupprimer.config(state=DISABLED)
        self.frameEffetsUtil.boutonAjouter.config(state=DISABLED)
        self.frameEffetsUtil.boutonSupprimer.config(state=DISABLED)
        self.frameConditionsUtil.boutonAjouter.config(state=DISABLED)
        self.frameConditionsUtil.boutonSupprimer.config(state=DISABLED)
        self.entryEmplacementObjet.config(state=DISABLED)
        self.compteurNbrUtilObjet.config(state=DISABLED)
        if fonction=='1':
            self.frameEffetsEquip.boutonAjouter.config(state=NORMAL)
            self.frameEffetsEquip.boutonSupprimer.config(state=NORMAL)
            self.frameConditionsEquip.boutonAjouter.config(state=NORMAL)
            self.frameConditionsEquip.boutonSupprimer.config(state=NORMAL)
            self.entryEmplacementObjet.config(state=NORMAL)
        elif fonction=='2':
            self.frameEffetsUtil.boutonAjouter.config(state=NORMAL)
            self.frameEffetsUtil.boutonSupprimer.config(state=NORMAL)
            self.frameConditionsUtil.boutonAjouter.config(state=NORMAL)
            self.frameConditionsUtil.boutonSupprimer.config(state=NORMAL)
            self.compteurNbrUtilObjet.config(state=NORMAL)          
    def SelectionnerElement(self,event): 
        if self.sel is None or self.Enregistrer(): self.Charger()
        self.sel=""
        
    def validate(self):
        if re.match(r"^[\w \-éèà'çäâëêÿüûïîöô]+$",self.frameDescription.nom.get()) == None:
            showinfo('Erreur',"Nom invalide. Peut contenir des caractères alpha-numériques et underscore.")
            return False
        if re.match((r"^\w+$"),self.frameDescription.id.get()) == None:
            showinfo('Erreur',"ID invalide. Peut contenir des caractères alpha-numériques et underscore.")
            return False
        if self.type=='action':
            if (re.match(r'^\d+$',self.compteurtIncantAction.get()) == None) or (int(self.compteurtIncantAction.get()) < 0):
                showinfo('Erreur',"Durée d'incantation invalide, doit contenir des entier supérieur à 0.")
                return False
        elif self.type=='objet':
            if (re.match(r"^\d+(\.\d+)?$",self.compteurPoidsObjet.get())) == None:
                showinfo('Erreur',"Poids de l'objet invalide, doit contenir un nombre supérieur à 0.")
                return False
            if (re.match(r"^\d+(\.\d+)?$",self.compteurPrixObjet.get())) == None:
                showinfo('Erreur',"Prix de l'objet invalide, doit contenir un nombre supérieur à 0.")
                return False
            if (self.fonctionObjet.get()[0]=='1') and (all([False if re.match(r'^(\w)+(;\w+)*$',emp)==None else True for emp in self.emplacementObjet.get().split(';')])==False):
                showinfo('Erreur',"Emplacement de l'objet invalide. Peut contenir des caractères alpha-numériques et underscore.")
                
                return False
            if (self.fonctionObjet.get()[0]=='2') and (re.match(r'^\d+$',self.compteurNbrUtilObjet.get()) == None):
                showinfo('Erreur',"Nombre d'utilisation de l'objet invalide. Peut contenir un nombre entier supérieur à 0.")
                return False
        elif self.type=='creature': 
            for caract in self.frameCaract.listFrame:
                if re.match(r"^\d+(\.\d+)?$",caract.valeur.get()) == None:
                    showinfo('Erreur','Caractéristique invalide, peut être un nombre positif entier ou décimal sous la forme 5.25.')
                    return False
                if not caract.nom in ['pv','pvBase','poidsPortes','poidsPortable'] and float(caract.valeur.get()) > univers.reglages.maxCaract:
                    showinfo('Erreur','Un caractéristique dépasse la limite définie dans les réglages: '+str(univers.reglages.maxCaract))
                    return False
            if re.match(r"^\d+$",self.compteurLvlCrea.get()) == None:
                showinfo('Erreur','Niveau invalide, doit être un nombre entier positif.')
                return False
            if re.match(r"^\d+$",self.compteurExpWinCrea.get()) == None:
                showinfo('Erreur','Expérience gagnée invalide, doit être un nombre entier positif.')
                return False
            if re.match(r"^\d+$",self.compteurMalusFuiteCrea.get()) == None:
                showinfo('Erreur','Malus de fuite invalide, doit être un nombre entier positif.')
                return False
        elif self.type=='region':
            if (re.match(r"^\d+(\.\d+)?$",self.compteurFactDep.get())) == None:
                showinfo('Erreur',"Le facteur de déplacement doit contenir un nombre supérieur à 0.")
                return False
            if self.listParent.get()!="Aucune" and findObjectFromID(univers.regions,self.listParent.get())==None:
                showinfo('Erreur',"Région parente inexistante.")
                return False
                
        return True          
    def Supprimer(self):
        if self.list.curselection()!=():
            result = askokcancel('',"Supprimer l'élément sélectionné ?")
            if result:
                id = self.list.get(self.list.curselection()[0])
                for object in self.listObject:
                    if object.id==id:
                        self.listObject.remove(object)
                        break
                self.list.delete(self.list.curselection()[0])
                self.Nouveau()   
                self.sel=None
    def Charger(self):
    
        self.mode="modifier"
        self.frameDescription.entryId.config(state=DISABLED)
        self.boutonNouveau.config(state=NORMAL)
        self.boutonSupprimer.config(state=NORMAL)
        selection = self.list.get(self.list.curselection()[0])
        for obj in self.listObject:
            if obj.id == selection: self.object = obj   
        self.frameDescription.nom.set(self.object.nom)
        self.frameDescription.id.set(self.object.id)
        self.frameDescription.textDescription.delete(0.0,END)
        self.frameDescription.textDescription.insert(0.0,self.object.description)
        self.frameDescription.motsCles = self.object.motsCles[:]
        self.frameDescription.listMotsCles.delete(0,END)
        self.frameDescription.listMotsCles.insert(0,*self.object.motsCles)
        
        if self.type=='action':
            self.typeAction.set(['0: Attaque', '1: Soin', '2: Buff'][self.object.type])
            self.cibleAction.set(['0: Lanceur', '1: Autre'][self.object.cible])
            self.utilAction.set(["0: N'importe quand", "1: En dehors d'un combat", '2: En combat'][self.object.util])
            if self.object.etatIncant == -1: self.etatIncantAction.set(['-1: aucun changement','0: mort','1: en forme','2: fatigué','3: immobilisé','4: gelé','5: inconscient'][0])
            else: self.etatIncantAction.set(['-1: aucun changement','0: mort','1: en forme','2: fatigué','3: immobilisé','4: gelé','5: inconscient'][self.object.etatIncant+1])
            self.compteurtIncantAction.delete(0,END)
            self.compteurtIncantAction.insert(0,self.object.tIncant)
            self.EsquivableAction.set(self.object.ratable)
            self.RatableAction.set(self.object.esquive)
            self.frameConditions.clear()
            self.frameConditions.update(self.object.conditions)
            self.frameEffets.clear()
            self.frameEffets.update(self.object.effets)
        elif self.type=='objet':
            self.fonctionObjet.set(['0: Non équipable et non utilisable (ex: tableau)',"1: Equipable mais non utilisable (ex: armure)","2: Non équipable mais utilisable (ex: potion)"][self.object.fonction])
            self.compteurNbrUtilObjet.delete(0,END)
            self.compteurPoidsObjet.delete(0,END)
            self.compteurPrixObjet.delete(0,END)
            self.compteurNbrUtilObjet.insert(0,self.object.nbrUse)
            self.compteurPoidsObjet.insert(0,self.object.poids)
            self.compteurPrixObjet.insert(0,self.object.prix)
            self.emplacementObjet.set(";".join(self.object.empEquip))
            self.frameConditionsPoss.clear()
            self.frameConditionsPoss.update(self.object.conditionsPoss)
            self.frameConditionsEquip.clear()
            self.frameConditionsEquip.update(self.object.conditionsEquip)
            self.frameConditionsUtil.clear()
            self.frameConditionsUtil.update(self.object.conditionsUtil)
            self.frameEffetsPoss.clear()
            self.frameEffetsPoss.update(self.object.effetsPoss)
            self.frameEffetsEquip.clear()
            self.frameEffetsEquip.update(self.object.effetsEquip)
            self.frameEffetsUtil.clear()
            self.frameEffetsUtil.update(self.object.effetsUtil)
            self.GererFonctionObjet()
        elif self.type=='creature':
            self.frameCaract.refresh()
            for caract in self.frameCaract.listFrame: 
                if caract.nom in self.object.caracteristiques.keys(): self.frameCaract.listFrame[self.frameCaract.listFrame.index(caract)].valeur.set(self.object.caracteristiques[caract.nom])
                else: self.object.caracteristiques[caract.nom]=0.0
            self.frameInventaire.clear()
            self.frameInventaire.update(self.object.inventaire)
            self.frameActions.clear()
            self.frameActions.update(self.object.actions)
            self.frameAmisAvec.clear()
            self.frameAmisAvec.update(self.object.amisAvec)
            self.listDialogue.set(([id for id,dial in univers.dialogues.items() if (self.object.dialogue is not None and id == self.object.dialogue.id)]+[''])[0])
            self.compteurLvlCrea.delete(0,END)
            self.compteurLvlCrea.insert(0,self.object.niveau)
            self.compteurExpWinCrea.delete(0,END)
            self.compteurExpWinCrea.insert(0,self.object.exp_win)
            self.corruptibleCrea.set(["0: non", "1: par l'argent", "2: par la séduction", "3: par l'argent et la séduction"][self.object.corruptible])
            self.etatCrea.set(['0: mort','1: en forme','2: fatigué','3: immobilisé','4: gelé','5: inconscient'][self.object.etat])
            self.stratOffCrea.set(["0: lâche - attaque toujours les plus faibles", "1: honorable - attaque toujours les plus forts", "2: ciblée - attaque toujours un même créature choisie au hasard", "3: hasardeuse - attaque les créatures au hasard"][self.object.strategieOffensive])
            self.stratDefCrea.set(["0: sacrifice - la créature n'hésite pas à mourir tant qu'elle inflige le plus de dommage possible", "1: offensive - la créature utilise des sorts de soins dès qu'il lui reste -20% de sa vie", "2: équilibrée - la créature utilise des sorts de soins dès qu'il lui reste -50% de sa vie", "3: défensive - la créature utilise des sorts de soins dès qu'elle n'a pas toute sa vie", "4: totale - la créature utilise tout le temps des sorts de soins"][self.object.strategieDefensive])
            self.hostilCrea.set(["0: très farouche - s'enfuit à vue du joueur", "1: farouche - s'enfuit à vue de comba", "2: peureux - s'enfuit en combat", "3: passif - n'attaque jamais et ne fuie pas", "4: neutre - attaque de représaille", "5: défenseur - attaque à vue de combat", "6: hostile - attaque le joueur à vue", "7: agressif - attaque tout le monde à vue"][self.object.hostil])
            self.rompreIncantCrea.set(self.object.rompreIncant)
            self.compteurMalusFuiteCrea.delete(0,END)
            self.compteurMalusFuiteCrea.insert(0,self.object.malusFuite)
        elif self.type=='region':
            self.compteurFactDep.delete(0,END)
            self.compteurFactDep.insert(0,self.object.facteurDep)
            for i in range(0,8): 
                if self.object.directionUtil[i]=='0': self.direction[i].set(False)
                else: self.direction[i].set(True)
            if self.object.regionParent==self.object.id or findObjectFromID(univers.regions,self.object.regionParent) is None: self.listParent.set("Aucune")
            else : self.listParent.set(self.object.regionParent)
            self.frameEffets.clear()
            self.frameEffets.update(self.object.effets)
            self.frameConditionsEntrer.clear()
            self.frameConditionsEntrer.update(self.object.conditionsEntrer)
            self.frameConditionsSortir.clear()
            self.frameConditionsSortir.update(self.object.conditionsSortir)
            self.frameCreaR.clear()
            self.frameCreaR.update(self.object.creaturesRencontrables)
            self.frameCreatures.clear()
            self.frameCreatures.update(self.object.creatures)
            self.frameObjets.clear()
            self.frameObjets.update(self.object.objets)
            self.framePortails.clear()
            self.framePortails.update(self.object.portails)
    
        self.boutonSupprimer.config(state=NORMAL)
        self.boutonEnregistrer.config(state=NORMAL)
        self.refresh()                
    def Enregistrer(self):
        if self.validate():
            already=False
            if self.mode != "modifier":
                for i in range(0,self.list.size()):
                    if self.list.get(i)==self.frameDescription.id.get(): 
                        already=True
                        showinfo('Erreur',"Elément déjà existant. Choisissez un autre ID")
                        
            if not already:   
                if self.type=='action':
                    if self.mode=="modifier": action = findObjectFromID(univers.actions,self.frameDescription.id.get())
                    else: action = Action()
                    action.nom = self.frameDescription.nom.get()
                    action.id = self.frameDescription.id.get()
                    action.motsCles = self.frameDescription.motsCles[:]
                    action.description = self.frameDescription.textDescription.get(0.0,END)
                    action.type = int(self.typeAction.get()[0])
                    action.cible = int(self.cibleAction.get()[0])
                    action.util = int(self.utilAction.get()[0])
                    action.tIncant = int(self.compteurtIncantAction.get())
                    etatIncant = self.etatIncantAction.get()
                    if etatIncant[0]=='-': action.etatIncant = int(etatIncant[0:2])
                    else: action.etatIncant = int(etatIncant[0])
                    action.ratable = self.RatableAction.get()
                    action.esquive = self.EsquivableAction.get()
                    action.conditions = self.frameConditions.conditions[:]
                    action.effets = self.frameEffets.effets[:]
                    self.object=action
                elif self.type=='objet':
                    if self.mode=="modifier": objet = findObjectFromID(univers.objets,self.frameDescription.id.get())
                    else: objet = Objet()
                    objet.nom = self.frameDescription.nom.get()
                    objet.id = self.frameDescription.id.get()
                    objet.motsCles = self.frameDescription.motsCles[:]
                    objet.description = self.frameDescription.textDescription.get(0.0,END)
                    objet.fonction = int(self.fonctionObjet.get()[0])
                    objet.poids = float(self.compteurPoidsObjet.get())
                    objet.prix = float(self.compteurPrixObjet.get())
                    objet.nbrUse = int(self.compteurNbrUtilObjet.get())
                    objet.empEquip = self.emplacementObjet.get().split(';')
                    objet.conditionsPoss = self.frameConditionsPoss.conditions[:]
                    objet.conditionsUtil = self.frameConditionsUtil.conditions[:]
                    objet.conditionsEquip = self.frameConditionsEquip.conditions[:]
                    objet.effetsPoss = self.frameEffetsPoss.effets[:]
                    objet.effetsUtil = self.frameEffetsUtil.effets[:]
                    objet.effetsEquip = self.frameEffetsEquip.effets[:]
                    self.object=objet
                elif self.type=="creature":
                    if self.mode=="modifier": creature = findObjectFromID(univers.creatures,self.frameDescription.id.get())
                    else: creature = Creature()
                    creature.nom=self.frameDescription.nom.get()
                    creature.id=self.frameDescription.id.get()
                    creature.motsCles=list(set(self.frameDescription.motsCles))
                    creature.description=self.frameDescription.textDescription.get(0.0,END)
                    for caract in self.frameCaract.listFrame:
                        creature.caracteristiques[caract.nom]=float(caract.valeur.get())
                    creature.inventaire=self.frameInventaire.items[:]
                    creature.niveau=int(self.compteurLvlCrea.get())
                    creature.exp_win=int(self.compteurExpWinCrea.get())
                    creature.actions=list(set(self.frameActions.items))
                    creature.corruptible=int(self.corruptibleCrea.get()[0])
                    creature.etat=int(self.etatCrea.get()[0])
                    creature.strategieOffensive=int(self.stratOffCrea.get()[0])
                    creature.strategieDefensive=int(self.stratDefCrea.get()[0])
                    creature.rompreIncant=self.rompreIncantCrea.get()
                    creature.hostil=int(self.hostilCrea.get()[0])
                    creature.amisAvec=list(set(self.frameAmisAvec.items))
                    if self.listDialogue.get()!='':creature.dialogue=univers.dialogues[self.listDialogue.get()]
                    creature.malusFuite=int(self.compteurMalusFuiteCrea.get())
                    self.object=creature
                elif self.type=="region":
                    if self.mode=="modifier": region = findObjectFromID(univers.regions,self.frameDescription.id.get())
                    else: region = Region()
                    region.nom=self.frameDescription.nom.get()
                    region.id=self.frameDescription.id.get()
                    region.motsCles=list(set(self.frameDescription.motsCles))
                    region.description=self.frameDescription.textDescription.get(0.0,END)
                    if not self.listParent.get() == "Aucune": region.regionParent=self.listParent.get()
                    else: region.regionParent=region.id
                    region.facteurDep=float(self.compteurFactDep.get())
                    region.directionUtil=''.join(['1' if self.direction[i].get()==True else '0' for i in range(0,8)])
                    region.creaturesRencontrables=list(set(self.frameCreaR.items))
                    region.conditionsEntrer = self.frameConditionsEntrer.conditions[:]
                    region.conditionsSortir = self.frameConditionsSortir.conditions[:]
                    region.effets = self.frameEffets.effets[:]
                    region.objets = self.frameObjets.items[:]
                    region.creatures = self.frameCreatures.items[:]
                    region.portails = self.framePortails.items[:]
                    self.object=region
                
                if self.mode=="nouveau":
                    self.listObject.append(self.object)
                    self.list.insert(0,self.object.id) 
                    self.mode="modifier"
                    self.frameDescription.entryId.config(state=DISABLED)
                   
            self.refresh()
            return True 
        return False
    def Nouveau(self):
        self.mode="nouveau"
        self.boutonSupprimer.config(state=DISABLED)
        self.boutonNouveau.config(state=DISABLED)
        self.frameDescription.entryNom.delete(0,END)
        self.frameDescription.entryId.config(state=NORMAL)
        self.frameDescription.entryId.delete(0,END)
        self.frameDescription.textDescription.delete(0.0,END)
        self.frameDescription.motsCles=[]
        self.frameDescription.listMotsCles.delete(0,END)
        
        if self.type=='action':
            self.typeAction.set('0: Attaque')
            self.cibleAction.set('0: Lanceur')
            self.utilAction.set('2: En combat')
            self.etatIncantAction.set('-1: aucun changement')
            self.compteurtIncantAction.delete(0,END)
            self.EsquivableAction.set(True)
            self.RatableAction.set(True)
            self.frameConditions.clear()
            self.frameEffets.clear()
        elif self.type=='objet':
            self.fonctionObjet.set("1: Equipable mais non utilisable (ex: armure)")
            self.compteurNbrUtilObjet.delete(0,END)
            self.compteurPoidsObjet.delete(0,END)
            self.compteurPrixObjet.delete(0,END)
            self.compteurNbrUtilObjet.insert(0,"1")
            self.compteurPrixObjet.insert(0,"0.0")
            self.compteurPoidsObjet.insert(0,"0.0")
            self.emplacementObjet.set("")
            self.frameConditionsPoss.clear()
            self.frameConditionsEquip.clear()
            self.frameConditionsUtil.clear()
            self.frameEffetsPoss.clear()
            self.frameEffetsEquip.clear()
            self.frameEffetsUtil.clear()
            self.GererFonctionObjet()
        elif self.type=='creature':
            for caract in self.frameCaract.listFrame: caract.valeur.set("0")
            self.frameInventaire.clear()
            self.frameActions.clear()
            self.frameAmisAvec.clear()
            self.listDialogue.set("")
            self.compteurLvlCrea.delete(0,END)
            self.compteurExpWinCrea.delete(0,END)
            self.compteurLvlCrea.insert(0,"0")
            self.compteurExpWinCrea.insert(0,"0")
            self.corruptibleCrea.set("0: non")
            self.etatCrea.set('1: en forme')
            self.stratOffCrea.set("2: ciblée - attaque toujours un même créature choisie au hasard")
            self.stratDefCrea.set("1: offensive - la créature utilise des sorts de soins dès qu'il lui reste -20% de sa vie")
            self.hostilCrea.set("4: neutre - attaque de représaille")
            self.rompreIncantCrea.set(True)
            self.compteurMalusFuiteCrea.delete(0,END)
            self.compteurMalusFuiteCrea.insert(0,"0")
            
        elif self.type=='region':
            self.compteurFactDep.delete(0,END)
            self.compteurFactDep.insert(0,"1.0")
            for i in range(0,8): self.direction[i].set(True)
            self.listParent.set("Aucune")
            self.frameEffets.clear()
            self.frameConditionsEntrer.clear()
            self.frameConditionsSortir.clear()
            self.frameCreaR.clear()
            self.frameCreatures.clear()
            self.frameObjets.clear()
            self.framePortails.clear()   
    def ChargerList(self):
        self.list.delete(0,END)
        self.list.insert(0,*[obj.id for obj in self.listObject])
        self.sel=None
class FrameQuest(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.mode=''
        self.sel=None
        self.createWidgets()
        self.switchMode()
    def createWidgets(self):
        self.frameTop=Frame(self)
        self.frameTop.pack(side=TOP,fill=BOTH,expand=1)
        self.tree=ttk.Treeview(self.frameTop,height=25)
        self.tree.pack(side=LEFT,expand=1,fill=Y)
        self.tree.bind('<<TreeviewSelect>>',self.Select)
        self.LoadQuest()
        self.zoneEditeur=Frame(self.frameTop)
        self.zoneEditeur.pack(side=LEFT,fill=BOTH,expand=1)
        self.labelNom=Label(self.zoneEditeur,text='Nom :')
        self.labelID=Label(self.zoneEditeur,text='ID :')
        self.nom=StringVar()
        self.ID=StringVar()
        self.entryNom=Entry(self.zoneEditeur,textvariable=self.nom)
        self.entryID=Entry(self.zoneEditeur,textvariable=self.ID,state=DISABLED)
        self.labelTempsRestant=Label(self.zoneEditeur,text='Temps restant :')
        self.compteurTempsRestant=Spinbox(self.zoneEditeur,from_=-1,to=10000000)
        self.labelDescription=Label(self.zoneEditeur,text='Description')
        self.textDescription=Text(self.zoneEditeur,width=50,height=15)
        self.frameObjectifsAchevement=FrameList(self.zoneEditeur,type='objectif',text="Objectifs nécessaires à l'achèvement")
        self.frameObjObj=Frame(self.zoneEditeur)
        self.frameObjectifsAchevementObjectif=FrameList(self.frameObjObj,type='objectif',text="Objectifs nécessaires à l'achèvement")
        self.frameObjectifsLancementObjectif=FrameList(self.frameObjObj,type='objectif',text="Objectifs à achever pour lancer l'objectif")
        self.frameObjectifsLancementObjectif.pack(side=LEFT,fill=BOTH,expand=1)
        self.frameObjectifsAchevementObjectif.pack(side=LEFT,fill=BOTH,expand=1)
        self.frameCondEff=Frame(self.zoneEditeur)
        self.frameConditionsLancement=FrameConditions(self.frameCondEff,text="Conditions de lancement")
        self.frameConditionsAchevement=FrameConditions(self.frameCondEff,text="Conditions d'achèvement")
        self.frameConditionsLancement.pack(side=LEFT,fill=BOTH,expand=1)
        self.frameConditionsAchevement.pack(side=LEFT,fill=BOTH,expand=1)
        self.frameEffetsSucces=FrameEffets(self.frameCondEff,text="Effets en cas de succès")
        self.frameEffetsEchec=FrameEffets(self.frameCondEff,text="Effets en cas d'échec")
        self.frameObjectifs=FrameObjectifs(self.zoneEditeur)
        self.labelNom.pack(expand=1)
        self.entryNom.pack(expand=1)
        self.labelID.pack(expand=1)
        self.entryID.pack(expand=1)
        self.labelDescription.pack(expand=1)
        self.textDescription.pack(expand=1)
        self.frameBoutons=Frame(self)
        self.frameBoutons.pack(side=TOP,expand=1,pady=10)
        self.boutonAjouterQuete=Button(self.frameBoutons,text='Ajouter une quête',command=self.AddQuete)
        self.boutonAjouterObjectif=Button(self.frameBoutons,text='Ajouter un objectif',command=self.AddObjectif,state=DISABLED)
        self.boutonSupprimer=Button(self.frameBoutons,text='Supprimer',command=self.Supprimer,state=DISABLED)
        self.boutonEnregistrer=Button(self.frameBoutons,text='Enregistrer',command=self.Enregistrer,state=DISABLED)
        self.boutonAjouterQuete.pack(side=LEFT)
        self.boutonAjouterObjectif.pack(side=LEFT)
        self.boutonSupprimer.pack(side=LEFT)
        self.boutonEnregistrer.pack(side=LEFT)
    def AddQuete(self):
        result = askCaracteristique(self).result
        if result:
            self.tree.insert('',END,iid=transformNom(result),text=result)
            quete = Quete()
            quete.nom=result
            quete.id=transformNom(result)
            univers.quetes.append(quete)
            if self.mode=='objectif': self.switchMode()
            self.ChargerQuete(quete)
    def AddObjectif(self):
        sel = self.tree.selection()
        if sel:
            result = askCaracteristique(self,label='ID :').result
            if result:
                self.tree.insert(sel[0],END,iid=transformNom(result),text=transformNom(result))
                objectif=Objectif()
                objectif.id=transformNom(result)
                univers.quetes[univers.quetes.index([quete for quete in univers.quetes if quete.id==sel[0]][0])].objectifs.append(objectif)
                if self.mode=='quete': self.switchMode()
                self.ChargerObjectif(objectif)
    def Supprimer(self):
        sel=self.tree.selection()
        result = askokcancel('Attention','Supprimer cet élément ?')
        if result:
            if self.tree.parent(sel[0])=='':
                del univers.quetes[univers.quetes.index(findObjectFromID(univers.quetes,sel[0]))]
            else:
                queteParent=findObjectFromID(univers.quetes,self.tree.parent(sel[0]))
                del univers.quetes[univers.quetes.index(queteParent)].objectifs[univers.quetes[univers.quetes.index(queteParent)].objectifs.index(findObjectFromID(queteParent.objectifs,sel[0]))]
            self.tree.delete(sel[0])    
            self.boutonEnregistrer.config(state=DISABLED)
    def Enregistrer(self):
        if self.validate():
            if self.mode=='quete':
                quete=univers.quetes[univers.quetes.index(findObjectFromID(univers.quetes,self.ID.get()))]
                quete.nom=self.nom.get()
                self.tree.item(self.ID.get(),text=self.nom.get())
                quete.description=self.textDescription.get(0.0,END)
                quete.objectifsAchevement=self.frameObjectifsAchevement.items[:]
                quete.conditionsLancement=self.frameConditionsLancement.conditions[:]
                quete.conditionsAchevement=self.frameConditionsAchevement.conditions[:]
                quete.effetsEchec=self.frameEffetsEchec.effets[:]
                quete.effetsSucces=self.frameEffetsSucces.effets[:]
                quete.tempsRestant=int(self.compteurTempsRestant.get())
            else:
                queteParent=findObjectFromID(univers.quetes,self.tree.parent(self.ID.get()))
                objectif=univers.quetes[univers.quetes.index(queteParent)].objectifs[queteParent.objectifs.index(findObjectFromID(queteParent.objectifs,self.ID.get()))]
                objectif.description=self.textDescription.get(0.0,END)
                objectif.conditionsLancement=self.frameConditionsLancement.conditions[:]
                objectif.conditionsAchevement=self.frameConditionsAchevement.conditions[:]
                self.frameObjectifs.createObjectif()
                objectif.objectif=str(self.frameObjectifs.objectif)
                objectif.ordreAchevement=self.frameObjectifsAchevementObjectif.items[:]
                objectif.ordreLancement=self.frameObjectifsLancementObjectif.items[:]
            return True
        return False
    def validate(self):
        if self.mode=='quete':
            if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.nom.get()) == None:
                showinfo('Erreur',"Nom invalide. Peut contenir des caractères alpha-numériques et underscore.")
                return False
            if re.match(r"^-?\d+$",self.compteurTempsRestant.get()) == None:
                showinfo('Erreur','Temps restant invalide, doit être un nombre entier positif.')
                return False
        else:
            if not self.frameObjectifs.validate(): return False
        return True
    def Select(self,event=None):
        self.boutonSupprimer.config(state=NORMAL)
        self.boutonEnregistrer.config(state=NORMAL)
        if self.sel==None or self.Enregistrer():
            self.sel=self.tree.selection()
            if self.tree.parent(self.sel[0])=='': 
                self.boutonAjouterObjectif.config(state=NORMAL)
                if self.mode=='objectif': self.switchMode()
                self.ChargerQuete(findObjectFromID(univers.quetes,self.sel[0]))
            else: 
                self.boutonAjouterObjectif.config(state=DISABLED)
                if self.mode=='quete': self.switchMode()
                self.ChargerObjectif(findObjectFromID(findObjectFromID(univers.quetes,self.tree.parent(self.sel[0])).objectifs,self.sel[0]))
    def LoadQuest(self):
        for quete in univers.quetes:
            self.tree.insert('',END,iid=quete.id,text=quete.nom)
            for objectif in quete.objectifs:
                self.tree.insert(quete.id,END,iid=objectif.id,text=objectif.id)
    def ChargerQuete(self,quete):
        self.nom.set(quete.nom)
        self.ID.set(quete.id)
        self.textDescription.delete(0.0,END)
        self.textDescription.insert(0.0,quete.description)
        self.frameObjectifsAchevement.clear()
        self.frameObjectifsAchevement.update(quete.objectifsAchevement)
        self.frameObjectifsAchevement.listObject=[objectif.id for objectif in quete.objectifs]
        self.frameObjectifsAchevement.updateChoices(self.frameObjectifsAchevement.listObject)
        self.frameEffetsSucces.clear()
        self.frameEffetsSucces.update(quete.effetsSucces)
        self.frameEffetsEchec.clear()
        self.frameEffetsEchec.update(quete.effetsEchec)
        self.frameConditionsLancement.clear()
        self.frameConditionsLancement.update(quete.conditionsLancement)
        self.frameConditionsAchevement.clear()
        self.frameConditionsAchevement.update(quete.conditionsAchevement)
        self.compteurTempsRestant.delete(0,END)
        self.compteurTempsRestant.insert(0,quete.tempsRestant)
    def ChargerObjectif(self,objectif):
        self.ID.set(objectif.id)
        self.textDescription.delete(0.0,END)
        self.textDescription.insert(0.0,objectif.description)
        self.frameObjectifs.charger(objectif.objectif)
        self.frameObjectifsAchevementObjectif.clear()
        self.frameObjectifsAchevementObjectif.update(objectif.ordreAchevement)
        list=[obj.id for obj in univers.quetes[univers.quetes.index([quete for quete in univers.quetes if quete.id==self.tree.parent(objectif.id)][0])].objectifs if obj.id!=objectif.id]
        self.frameObjectifsAchevementObjectif.listObject=list
        self.frameObjectifsAchevementObjectif.updateChoices(list)
        self.frameObjectifsLancementObjectif.clear()
        self.frameObjectifsLancementObjectif.update(objectif.ordreLancement)
        self.frameObjectifsLancementObjectif.listObject=list
        self.frameObjectifsLancementObjectif.updateChoices(list)
        self.frameConditionsLancement.clear()
        self.frameConditionsLancement.update(objectif.conditionsLancement)
        self.frameConditionsAchevement.clear()
        self.frameConditionsAchevement.update(objectif.conditionsAchevement)
        self.frameObjectifs.listObjet.set_completion_list([objet.id for objet in univers.objets]+['*'])
        self.frameObjectifs.listCrea.set_completion_list([crea.id for crea in univers.creatures]+['*'])
        self.frameObjectifs.listRegion.set_completion_list([region.id for region in univers.regions]+['*'])
    def switchMode(self):
        if self.mode=='objectif':
            self.frameObjectifs.pack_forget()
            self.frameCondEff.pack_forget()
            self.frameObjObj.pack_forget()
            self.mode='quete'
        elif self.mode=='quete':
            self.frameObjectifsAchevement.pack_forget()
            self.frameEffetsSucces.pack_forget()
            self.frameEffetsEchec.pack_forget()
            self.frameCondEff.pack_forget()
            self.labelTempsRestant.pack_forget()
            self.compteurTempsRestant.pack_forget()
            self.mode='objectif'
        if self.mode=='': self.mode='quete'
        if self.mode=='quete':
            self.entryNom.config(state=NORMAL)
            self.frameObjectifsAchevement.pack(expand=1)
            self.labelTempsRestant.pack(expand=1)
            self.compteurTempsRestant.pack(expand=1)
            self.frameCondEff.pack(fill=BOTH,expand=1)
            self.frameEffetsSucces.pack(side=LEFT,fill=BOTH,expand=1)
            self.frameEffetsEchec.pack(side=LEFT,fill=BOTH,expand=1)
        elif self.mode=='objectif':
            self.entryNom.config(state=DISABLED)
            self.frameObjectifs.pack(fill=BOTH,expand=1,pady=5)
            self.frameCondEff.pack(fill=BOTH,expand=1)
            self.frameObjObj.pack(fill=BOTH,expand=1)
    def refresh(self): pass
class FrameText(Frame):
  def __init__(self,parent):
      Frame.__init__(self,parent)
      self.createWidgets()
      self.type=""
  def createWidgets(self):
    self.tree=ttk.Treeview(self)
    self.tree["columns"]=("number")
    self.tree.column("#0", width=800,minwidth=250)
    self.tree.heading("#0",text="Entrée")
    self.tree.column("#1",width=120,stretch=NO)
    self.tree.heading("#1", text="Nombre d'entrées")
    self.tree.pack(side=TOP,expand=1,fill=BOTH)
    self.tree.bind('<<TreeviewSelect>>',self.Select)
    self.frameBoutons=Frame(self)
    self.frameBoutons.pack(side=TOP,expand=1)
    self.boutonSupprimer=Button(self.frameBoutons,text='Supprimer',command=self.Supprimer)
    self.boutonSupprimer.pack(side=LEFT)
    self.boutonNouveau=Button(self.frameBoutons,text="Nouveau",command=self.Nouveau)
    self.boutonNouveau.pack(side=RIGHT)
    self.framePhrase=Frame(self)
    self.framePhrase.pack(expand=1,fill=BOTH)
    if "Contenu de framePhrase":
      self.labelType = Label(self.framePhrase,text='Type')
      self.listType = AutocompleteCombobox(self.framePhrase)
      self.listType.set_completion_list(['entrer','decrire','rencontre','fuite','fuite_echec','mort','action','action_ratee','incantation','esquive','equive_ratee','buff','aller','ramasser','equiper','ajout','enlever','jeter','cacher','desequiper','utiliser','erreur','achever_quete','ajouter_quete','retirer_quete'])
      self.listType.bind('<<ComboboxSelected>>',self.gererType)
      self.labelType.grid(row=0,column=0)
      self.listType.grid(row=0,column=1)
      self.labelRegion = Label(self.framePhrase,text='Région')
      self.listRegion = AutocompleteCombobox(self.framePhrase)
      self.listRegion.set_completion_list([region.id for region in univers.regions])
      self.labelCreature = Label(self.framePhrase,text='Créature')
      self.listCreature = AutocompleteCombobox(self.framePhrase)
      self.listCreature.set_completion_list([creature.id for creature in univers.creatures])
      self.labelCreatureCible = Label(self.framePhrase,text='Cible')
      self.listCreatureCible = AutocompleteCombobox(self.framePhrase)
      self.listCreatureCible.set_completion_list([creature.id for creature in univers.creatures])
      self.labelObjet = Label(self.framePhrase,text='Objet')
      self.listObjet = AutocompleteCombobox(self.framePhrase)
      self.listObjet.set_completion_list([objet.id for objet in univers.objets])
      self.labelAction = Label(self.framePhrase,text='Action')
      self.listAction = AutocompleteCombobox(self.framePhrase)
      self.listAction.set_completion_list([action.id for action in univers.actions])
      self.labelQuete = Label(self.framePhrase,text='Quete')
      self.listQuete = AutocompleteCombobox(self.framePhrase)
      self.listQuete.set_completion_list([quete.id for quete in univers.quetes])
      self.labelQuete = Label(self.framePhrase,text='Quête')
      self.labelHeure = Label(self.framePhrase, text='Heure')
      self.heure=StringVar()
      self.listHeure=OptionMenu(self.framePhrase,self.heure,*['jour','nuit','*'])
      self.heure.set('*')
      self.labelOp = Label(self.framePhrase,text='Opérateur')
      self.op=StringVar()
      self.listOp=OptionMenu(self.framePhrase,self.op,*["gain","perte","*"])
      self.op.set('*')
      self.labelCaract = Label(self.framePhrase,text='Caractéristique')
      self.caract=StringVar()
      self.listCaract=OptionMenu(self.framePhrase,self.caract,*univers.reglages.caracts+['*'])
      self.caract.set('*')
      self.labelDirection = Label(self.framePhrase,text='Direction')
      self.direction=StringVar()
      self.listDirection=OptionMenu(self.framePhrase,self.direction,*['N','S','E','O','NE','NO','SE','SO','*'])
      self.direction.set('*')
      self.labelErreur = Label(self.framePhrase,text='Erreur')
      self.erreur=StringVar()
      self.listErreur=OptionMenu(self.framePhrase,self.erreur,*['objet_non_possede','objet_non_trouvable','creature_non_trouvable','action non_autorisee','objet_non_trouvable_depouille','depouille_non_trouvable','mauvaise_direction','*'])
      self.erreur.set('*')
    self.frameBottom=Frame(self)
    self.frameBottom.pack(expand=1,fill=BOTH)
    self.frameEditeur=Frame(self.frameBottom)
    self.frameEditeur.pack(side=LEFT,expand=1,fill=BOTH)
    self.editeur=Text(self.frameEditeur,width=30)
    self.editeur.pack(side=RIGHT,expand=1)
    self.frameVariables=LabelFrame(self.frameEditeur,text='Variables')
    self.frameVariables.pack(side=RIGHT,expand=1)
    self.labelVariables=Label(self.frameVariables,text="%auteur: auteur d'une action\n%cible: cible d'une action\n%action: action utilisé\n"
        "%caract: caractéristique concerné\n%valeur: valeur d'un buff\n%operateur: type d'opération\n%direction: direction empruntée\n"
        "%lieu: localisation du personnage\n%duree: durée d'une incantation")
    self.labelVariables.pack(expand=1,fill=BOTH)
    self.listPhrases=Listbox(self.frameBottom)
    self.listPhrases.pack(side=RIGHT,expand=1,fill=BOTH)
  def Select(self,event=None): 
    sel = self.tree.selection()[0]
    if not self.tree.get_children(sel):
        self.Clean()
        self.text=sel.split()
        self.type=self.text[0]
        self.gererType()
        self.Charger()
  def Enregistrer(self): pass
  def Supprimer(self): pass
  def Nouveau(self): pass
  def Charger(self): 
  
    self.listType.set(self.text[0])
    if self.type in ['entrer','decrire'] :
      #L/H
      self.listRegion.set(self.text[1])
      self.heure.set(self.text[2])
    elif self.type in ['rencontre','fuite','fuite_echec','mort']:
      #C/L/H
      self.listCreature.set(self.text[1])
      self.listRegion.set(self.text[2])
      self.heure.set(self.text[3])
    elif self.type in ['action','action_ratee','incantation']:
      #C/C/A/L/H
      self.listCreature.set(self.text[1])
      self.listCreatureCible.set(self.text[2])
      self.listAction.set(self.text[3])
      self.listRegion.set(self.text[4])
      self.heure.set(self.text[5])
    elif self.type in ['esquive','esquive_ratee']:
      #C/A/L/H 
      self.listCreature.set(self.text[1])
      self.listAction.set(self.text[2])
      self.listRegion.set(self.text[3])
      self.heure.set(self.text[4])
    elif self.type in ['buff']:
      #C/Op/Crct/L/H 
      self.listCreature.set(self.text[1])
      self.op.set(self.text[2])
      self.caract.set(self.text[3])
      self.listRegion.set(self.text[4])
      self.heure.set(self.text[5])
    elif self.type in ['aller']: 
      #Dir
      self.direction.set(self.text[1])
    elif self.type in ['ramasser','equiper','ajout','enlever','jeter','cacher','desequiper','utiliser']:
      #O/L/H 
      self.listObjet.set(self.text[1])
      self.listRegion.set(self.text[2])
      self.heure.set(self.text[3])
    elif self.type in ['erreur']:
      #Err
      self.erreur.set(self.text[1])
    elif self.type in ['achever_quete','ajouter_quete','retirer_quete']:
      #Q
      self.listQuete.set(self.text[1])
  def gererType(self,event=None): 
    if self.type in ['entrer','decrire'] :
      #L/H
      self.labelRegion.grid(row=0,column=2)
      self.listRegion.grid(row=0,column=3)
      self.labelHeure.grid(row=0,column=4)
      self.listHeure.grid(row=0,column=5)
    elif self.type in ['rencontre','fuite','fuite_echec','mort']:
      #C/L/H
      self.labelCreature.grid(row=0,column=2)
      self.listCreature.grid(row=0,column=3)
      self.labelRegion.grid(row=0,column=4)
      self.listRegion.grid(row=0,column=5)
      self.labelHeure.grid(row=0,column=6)
      self.listHeure.grid(row=0,column=7)
    elif self.type in ['action','action_ratee','incantation']:
      #C/C/A/L/H
      self.labelCreature.grid(row=0,column=2)
      self.listCreature.grid(row=0,column=3)
      self.labelCreatureCible.grid(row=0,column=4)
      self.listCreatureCible.grid(row=0,column=5)
      self.labelAction.grid(row=0,column=6)
      self.listAction.grid(row=0,column=7)
      self.labelRegion.grid(row=0,column=8)
      self.listRegion.grid(row=0,column=9)
      self.labelHeure.grid(row=0,column=10)
      self.listHeure.grid(row=0,column=11)
    elif self.type in ['esquive','esquive_ratee']:
      #C/A/L/H 
      self.labelCreature.grid(row=0,column=2)
      self.listCreature.grid(row=0,column=3)
      self.labelAction.grid(row=0,column=4)
      self.listAction.grid(row=0,column=5)
      self.labelRegion.grid(row=0,column=6)
      self.listRegion.grid(row=0,column=7)
      self.labelHeure.grid(row=0,column=8)
      self.listHeure.grid(row=0,column=9)
    elif self.type in ['buff']:
      #C/Op/Crct/L/H 
      self.labelCreature.grid(row=0,column=2)
      self.listCreature.grid(row=0,column=3)
      self.labelOp.grid(row=0,column=4)
      self.listOp.grid(row=0,column=5)
      self.labelCaract.grid(row=0,column=6)
      self.listCaract.grid(row=0,column=7)
      self.labelRegion.grid(row=0,column=8)
      self.listRegion.grid(row=0,column=9)
      self.labelHeure.grid(row=0,column=10)
      self.listHeure.grid(row=0,column=11)
    elif self.type in ['aller']: 
      #Dir
      self.labelDirection.grid(row=0,column=2)
      self.listDirection.grid(row=0,column=3)
    elif self.type in ['ramasser','equiper','ajout','enlever','jeter','cacher','desequiper','utiliser']:
      #O/L/H 
      self.labelObjet.grid(row=0,column=2)
      self.listObjet.grid(row=0,column=3)
      self.labelRegion.grid(row=0,column=4)
      self.listRegion.grid(row=0,column=5)
      self.labelHeure.grid(row=0,column=6)
      self.listHeure.grid(row=0,column=7)
    elif self.type in ['erreur']:
      #Err
      self.listErreur.grid(row=0,column=3)
      self.labelErreur.grid(row=0,column=2)
    elif self.type in ['achever_quete','ajouter_quete','retirer_quete']:
      #Q
      self.labelQuete.grid(row=0,column=2)
      self.listQuete.grid(row=0,column=3)
  def Clean(self):
    if self.type in ['entrer','decrire'] :
      #L/H
      self.labelRegion.grid_forget()
      self.listRegion.grid_forget()
      self.labelHeure.grid_forget()
      self.listHeure.grid_forget()
    elif self.type in ['rencontre','fuite','fuite_echec','mort']:
      #C/L/H
      self.labelCreature.grid_forget()
      self.listCreature.grid_forget()
      self.labelRegion.grid_forget()
      self.listRegion.grid_forget()
      self.labelHeure.grid_forget()
      self.listHeure.grid_forget()
    elif self.type in ['action','action_ratee','incantation']:
      #C/C/A/L/H
      self.labelCreature.grid_forget()
      self.listCreature.grid_forget()
      self.labelCreatureCible.grid_forget()
      self.listCreatureCible.grid_forget()
      self.labelAction.grid_forget()
      self.listAction.grid_forget()
      self.labelRegion.grid_forget()
      self.listRegion.grid_forget()
      self.labelHeure.grid_forget()
      self.listHeure.grid_forget()
    elif self.type in ['esquive','esquive_ratee']:
      #C/A/L/H 
      self.labelCreature.grid_forget()
      self.listCreature.grid_forget()
      self.labelAction.grid_forget()
      self.listAction.grid_forget()
      self.labelRegion.grid_forget()
      self.listRegion.grid_forget()
      self.labelHeure.grid_forget()
      self.listHeure.grid_forget()
    elif self.type in ['buff']:
      #C/Op/Crct/L/H 
      self.labelCreature.grid_forget()
      self.listCreature.grid_forget()
      self.labelOp.grid_forget()
      self.listOp.grid_forget()
      self.labelCaract.grid_forget()
      self.listCaract.grid_forget()
      self.labelRegion.grid_forget()
      self.listRegion.grid_forget()
      self.labelHeure.grid_forget()
      self.listHeure.grid_forget()
    elif self.type in ['aller']: 
      #Dir
      self.labelDirection.grid_forget()
      self.listDirection.grid_forget()
    elif self.type in ['ramasser','equiper','ajout','enlever','jeter','cacher','desequiper','utiliser']:
      #O/L/H 
      self.labelObjet.grid_forget()
      self.listObjet.grid_forget()
      self.labelRegion.grid_forget()
      self.listRegion.grid_forget()
      self.labelHeure.grid_forget()
      self.listHeure.grid_forget()
    elif self.type in ['erreur']:
      #Err
      self.listErreur.grid_forget()
      self.labelErreur.grid_forget()
    elif self.type in ['achever_quete','ajouter_quete','retirer_quete']:
      #Q
      self.labelQuete.grid_forget()
      self.listQuete.grid_forget()
  def refresh(self): pass
  def calc_nombre(self,parent):
    nombre=0
    for child in self.tree.get_children(parent):
        if self.tree.get_children(child):
            nombre+=self.calc_nombre(child)
        else:
            nombre+=int(self.tree.item(child,option="values")[0])
    self.tree.set(parent,"number",str(nombre))
    return nombre
        
  def load(self): 
    for item in self.tree.get_children(""): self.tree.delete(item)
    for texte,phrases in univers.textes.items():
        mots=texte.split()
        parent=""
        for i in range(len(mots)):
            mot = " ".join(mots[:i+1])
            if not self.tree.exists(mot):
                parent=self.tree.insert(parent,END,iid=mot,text=mot)
                if i == len(mots)-1: self.tree.set(mot,"number",str(len(phrases)))
            elif not i == len(mots):
                parent=mot
                pass
    self.calc_nombre("")
    

class FrameConditions(LabelFrame):
    def __init__(self,parent,text=None):
        LabelFrame.__init__(self,parent,text=text)
        self.createWidgets()
    def createWidgets(self):
        self.conditions=[]
        self.listConditions=Listbox(self)
        self.listConditions.bind('<<ListboxSelect>>',lambda e:self.boutonOU.config(state=NORMAL))
        self.listConditions.pack(side=LEFT,expand=1,fill=BOTH)
        self.boutonAjouter=Button(self,text='Ajouter',command=self.AjoutCondition)
        self.boutonSupprimer=Button(self,text='Supprimer',command=self.SupprimerCondition)
        self.boutonAjouter.pack(side=TOP,fill=BOTH)
        self.boutonSupprimer.pack(side=BOTTOM,fill=BOTH)
        self.boutonOU=Button(self,text='OU',command=self.OU,state=DISABLED)
        self.boutonOU.pack(side=RIGHT,fill=X)
    def AjoutCondition(self):
        result = askCondition(self).result
        if result:
            self.listConditions.insert(1,result)
            self.conditions.append(result)
    def SupprimerCondition(self):
        if self.listConditions.curselection() != (): 
            self.conditions.remove(self.listConditions.get(self.listConditions.curselection()[0]))
            self.listConditions.delete(self.listConditions.curselection())
    def OU(self):
        self.boutonOU.config(state=DISABLED)
        selection = self.listConditions.curselection()
        result = askCondition(self).result
        if result:
            self.conditions[self.conditions.index(self.listConditions.get(selection[0]))]+='||'+result
            oldConditionIndex=selection[0]
            oldCondition=self.listConditions.get(oldConditionIndex)
            newCondition = oldCondition+'||'+result
            self.listConditions.delete(selection)
            self.listConditions.insert(oldConditionIndex,newCondition)
    def clear(self):
        self.listConditions.delete(0,END)
        del self.conditions
        self.conditions=[]
    def update(self,list):
        self.listConditions.insert(0,*list)
        self.conditions.extend(list)
def findIDFromNom(listObjects,nom):
    if nom[0]=='#': return nom
    for object in listObjects: 
        if object.nom == nom: return object.id
    return None        
def findNomFromID(listObjects,id):
    if id[0]=='#': return id
    for object in listObjects: 
        if object.id == id: return object.nom
    return None    
def findObjectFromID(listObjects,id):
    if id[0]=='#': return id
    for object in listObjects:
        if object.id == id: return object
    return None
def findObjectFromNom(listObjects,nom):
    if nom[0]=='#': return nom
    for object in listObjects:
        if object.nom == nom: return object
    return None
def findIDFromObject(listObject,object):
    for obj in listObject:
        if obj == object: return object
    return None
def transformNom(nom=''):
    nom = nom.lower()
    accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'],
                    '_': [' ','-']
                    }
    for char, accented_chars in accents.items():
        for accented_char in accented_chars:
            nom = nom.replace(accented_char, char)
    nom = re.sub(r'\W','',nom)
    if nom[len(nom)-1]=='_': nom = nom[0:-1]
    return nom
                
class Dialog(Toplevel):

    '''Class to open dialogs.

    This class is intended as a base class for custom dialogs
    '''

    def __init__(self, parent, title = None,label='Nom :',item=None,type=None):

        '''Initialize a dialog.

        Arguments:

            parent -- a parent window (the application window)

            title -- the dialog title
        '''
        Toplevel.__init__(self, parent)

        self.withdraw() # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.label=label
        self.result = None
        self.item=item
        self.type=type
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()


        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                      parent.winfo_rooty()+50))

        self.deiconify() # become visibile now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self):
        '''Destroy the window'''
        self.initial_focus = None
        Toplevel.destroy(self)
        del self

    #
    # construction hooks

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        pass

    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        '''validate the data

        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        '''

        return 1 # override

    def apply(self):
        '''process the data

        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        '''

        pass # override
    
class windowRegion(Dialog):
    
    def body(self,master):
        self.frame=Frame(master)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(row=0,column=0)
        self.frameRegions=FrameObject(self.frame,type='region')
        self.frameRegions.pack(fill=BOTH,expand=1)
        
    def apply(self):
        self.result=""
    
class askCondition(Dialog):
    def body(self,master):
        self.oldType=''
        
        self.labelType=Label(master,text='Type : ')
        self.labelType.grid(row=0,column=0)
        self.listTypeCondition=AutocompleteCombobox(master)
        self.listTypeCondition.set_completion_list(['caracteristique','posseder','equiper','etat','localisation','quete','objectif'])
        self.listTypeCondition.bind('<<ComboboxSelected>>',self.gererType)
        self.listTypeCondition.grid(row=0,column=1)
        
        self.labelCaract=Label(master,text='Caractéristique : ')
        self.caractCondition=StringVar()
        self.listCaract=OptionMenu(master,self.caractCondition,*univers.reglages.caracts)
        
        self.labelComparateur=Label(master,text='Comparateur : ')
        self.comparateur=StringVar()
        self.listComparateur=OptionMenu(master,self.comparateur,*['<','>','=',''])
        
        self.labelValeur=Label(master,text='Valeur : ')
        self.valeur=StringVar()
        self.entryValeur=Entry(master,textvariable=self.valeur)
        
        self.labelObjet=Label(master,text='Objet : ')
        self.listObjet=AutocompleteCombobox(master)
        self.listObjet.set_completion_list([objet.id for objet in univers.objets])
        
        self.labelQuantite=Label(master,text='Quantité : ')
        self.compteurQuantite=Spinbox(master,from_=0,to=1000000)
        self.compteurQuantite.delete(0,END)
        self.compteurQuantite.insert(0,'1')
        
        self.labelEtat=Label(master,text='Etat : ')
        self.etatCondition=StringVar()
        self.listEtat=OptionMenu(master,self.etatCondition,*['0: mort','1: en forme','2: fatigué','3: immobilisé','4: gelé','5: inconscient'])
        
        self.labelRegion=Label(master,text='Région/Emplacement : ')
        self.coordCondition=AutocompleteCombobox(master)
        self.coordCondition.set_completion_list([region.id for region in univers.regions])
        
        self.labelQuete=Label(master,text='Quête : ')
        self.listQuete=AutocompleteCombobox(master)
        self.listQuete.set_completion_list([quete.id for quete in univers.quetes])
        self.listQuete.bind('<<ComboboxSelected>>',self.afficherObjectif)
        
        self.labelEtatQuete=Label(master,text='Avancement : ')
        self.etatQuete=StringVar()
        self.listEtatQuete=OptionMenu(master,self.etatQuete,*['0: non débutée','1: en cours','2: achevée'])
        
        self.labelObjectif=Label(master,text='Objectif : ')
        self.listObjectif=AutocompleteCombobox(master)
        
        self.invertCondition=BooleanVar()
        self.invertBouton=Checkbutton(master,text='Inverser ?',offvalue=False,onvalue=True,variable=self.invertCondition)
        self.invertBouton.grid(row=1,column=0)
        
    def afficherObjectif(self,event):
        quete_nom = self.listQuete.get()
        listObjectifs = []
        for quete in univers.quetes:
            if quete.nom==quete_nom: listObjectifs = quete.objectifs
        self.listObjectif.set_completion_list([objectif.id for objectif in listObjectifs])
    def createCondition(self):
        type=self.listTypeCondition.get()
        if type=='caracteristique': self.condition="{0} {1} {2}".format(self.caractCondition.get(),self.comparateur.get(),self.valeur.get())
        elif type=='posseder': 
            if self.comparateur.get()=='': self.condition="poss {0}".format(self.listObjet.get())
            else: self.condition="poss {0} {1} {2}".format(self.listObjet.get(),self.comparateur.get(),self.compteurQuantite.get())
        elif type=='etat': self.condition="etat {0}".format(self.etatCondition.get()[0])
        elif type=='equiper': self.condition="equip {0}".format(self.listObjet.get())
        elif type=='localisation': 
            if (self.coordCondition.get()[0]=='#') or (re.match(r'^\d+,\d+$',self.coordCondition.get()) != None): self.condition="in {0}".format(self.coordCondition.get())
            else: self.condition="in {0}".format(self.coordCondition.get())
        elif type=='quete': self.condition="quete {0} {1}".format(findIDFromNom(univers.quetes,self.listQuete.get()),self.etatQuete.get()[0])
        elif type=='objectif': self.condition="objectif {0} {1} {2}".format(findIDFromNom(univers.quetes,self.listQuete.get()),self.listObjectif.get(),self.etatQuete.get()[0])
        if self.invertCondition.get()==True: self.condition='!'+self.condition
        
    def validate(self):
        type = self.listTypeCondition.get()
        if type=='caracteristique':
            if self.comparateur.get() == '': 
                showinfo('Erreur','Vous devez sélectionner un comparateur.')
                return False
            if re.match(r'^\d+\.?\d*$',self.valeur.get()) == None:
                showinfo('Erreur','Valeur invalide. Ne peut contenir que des nombres entiers ou décimaux sous la forme 1.5.')
                return False
            if (not self.caractCondition.get() in univers.reglages.caracts) or (self.caractCondition.get()==''):
                showinfo('Erreur','Caractéristique invalide.')
                return False
        elif type=='posseder':
            if self.comparateur.get()!='' and re.match(r'^\d+$',self.compteurQuantite.get()) == None:
                showinfo('Erreur','Quantité non valide. Ne doit contenir que des entiers supérieurs ou égales 0.')
                return False
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.listObjet.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'un objet (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
            if self.listObjet.get()[0] != '#' and self.listObjet.get()==None:
                showinfo('Erreur','Objet inexistant.')
                return False
        elif type=='equiper':
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.listObjet.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'un objet (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
            if self.listObjet.get()[0] != '#' and self.listObjet.get()==None:
                showinfo('Erreur','Objet inexistant.')
                return False
        elif type=='etat':
            if self.etatCondition.get()=='':
                showinfo('Erreur','Etat non sélectionné.')
                return False
        elif type=='localisation':
            if re.match(r'^\d+,\d+$',self.coordCondition.get())==None and re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.coordCondition.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit les coordonnées d'un région sous la forme 10,20, l'id d'une région (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
            if self.coordCondition.get()[0] != '#' and re.match(r'^\d+,\d+$',self.coordCondition.get())==None and self.coordCondition.get()==None:
                showinfo('Erreur','Objet inexistant.')
                return False
        elif type=='quete':
            if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.listQuete.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient le nom d'une quete (caractères alpha-numériques et underscore).")
                return False
            if self.etatQuete.get()=='':
                showinfo('Erreur','Etat de la quête non sélectionné.')
                return False
            if findIDFromNom(univers.quetes,self.listQuete.get())==None:
                showinfo('Erreur','Quete inexistante.')
                return False
        elif type=='objectif':
            if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.listQuete.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient le nom d'une quete (caractères alpha-numériques et underscore).")
                return False
            if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.listObjectif.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient l'id d'un objectif (caractères alpha-numériques et underscore).")
                return False
            if self.etatQuete.get()=='':
                showinfo('Erreur',"Etat de l'objectif non sélectionné.")
                return False
            if not self.listObjectif.get() in self.listObjectif['values']:
                showinfo('Erreur','Objectif inexistant.')
                return False
            if findIDFromNom(univers.quetes,self.listQuete.get())==None:
                showinfo('Erreur','Quete inexistante.')
                return False

            
        return True
    def gererType(self,event):
        self.clean()
        type=self.listTypeCondition.get()
        self.oldType=type
        if type=='caracteristique':    
            self.labelCaract.grid(row=0,column=2)
            self.listCaract.grid(row=0,column=3)
            self.labelComparateur.grid(row=0,column=4)
            self.listComparateur.grid(row=0,column=5)
            self.labelValeur.grid(row=0,column=6)
            self.entryValeur.grid(row=0,column=7)
        elif type=='posseder':
            self.labelObjet.grid(row=0,column=2)
            self.listObjet.grid(row=0,column=3)
            self.labelComparateur.grid(row=0,column=4)
            self.listComparateur.grid(row=0,column=5)
            self.labelQuantite.grid(row=0,column=6)
            self.compteurQuantite.grid(row=0,column=7)
        elif type=='localisation': 
            self.labelRegion.grid(row=0,column=2)
            self.coordCondition.grid(row=0,column=3)
        elif type=='equiper': 
            self.labelObjet.grid(row=0,column=2)
            self.listObjet.grid(row=0,column=3)
        elif type=='etat': 
            self.labelEtat.grid(row=0,column=2)
            self.listEtat.grid(row=0,column=3)
        elif type=='quete': 
            self.labelQuete.grid(row=0,column=2)
            self.listQuete.grid(row=0,column=3)
            self.labelEtatQuete.grid(row=0,column=4)
            self.listEtatQuete.grid(row=0,column=5)
        elif type=='objectif':
            self.labelQuete.grid(row=0,column=2)
            self.listQuete.grid(row=0,column=3)
            self.labelObjectif.grid(row=0,column=4)
            self.listObjectif.grid(row=0,column=5)
            self.labelEtatQuete.grid(row=0,column=6)
            self.listEtatQuete.grid(row=0,column=7)
    def clean(self):
        type=self.oldType
        if type=='caracteristique':    
            self.labelCaract.grid_forget()
            self.listCaract.grid_forget()
            self.labelComparateur.grid_forget()
            self.listComparateur.grid_forget()
            self.labelValeur.grid_forget()
            self.entryValeur.grid_forget()
        elif type=='posseder':
            self.labelObjet.grid_forget()
            self.listObjet.grid_forget()
            self.labelComparateur.grid_forget()
            self.listComparateur.grid_forget()
            self.labelQuantite.grid_forget()
            self.compteurQuantite.grid_forget()
        elif type=='localisation': 
            self.labelRegion.grid_forget()
            self.coordCondition.grid_forget()
        elif type=='equiper': 
            self.labelObjet.grid_forget()
            self.listObjet.grid_forget()
        elif type=='etat': 
            self.labelEtat.grid_forget()
            self.listEtat.grid_forget()
        elif type=='quete': 
            self.labelQuete.grid_forget()
            self.listQuete.grid_forget()
            self.labelEtatQuete.grid_forget()
            self.listEtatQuete.grid_forget()
        elif type=='objectif':
            self.labelQuete.grid_forget()
            self.listQuete.grid_forget()
            self.labelObjectif.grid_forget()
            self.listObjectif.grid_forget()
            self.labelEtatQuete.grid_forget()
            self.listEtatQuete.grid_forget()
    def apply(self):
        self.result=self.condition
    def ok(self, event = None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.createCondition()
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
    
class askCaracteristique(Dialog):

    def body(self, master):

        Label(master, text=self.label).grid(row=0)

        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.result=""
        return self.e1 # initial focus

    def apply(self):
        self.result = str(self.e1.get())
class askReponse(Dialog):
    def body(self,master):
        Label(master, text="Réponse:").pack()
        self.text=Text(master,width=25,height=15)
        self.text.pack()
        self.result=""
        return self.text
    def apply(self):
        self.result=self.text.get(0.0,END)
class askEffet(Dialog):
    def body(self, master):
        self.oldType=""
        self.typeEffet=StringVar()
        self.labelType=Label(master,text="Type : ")
        self.labelType.grid(row=0,column=0)
        self.lDeroulType = AutocompleteCombobox(master,width=12)
        self.lDeroulType.set_completion_list(['buff','interdiction','etat','teleportation','objet','action','hostilite','emplacement','quete'])
        self.lDeroulType.grid(row=0,column=1)
        self.lDeroulType.bind('<<ComboboxSelected>>',self.gererType)
        self.labelDuree=Label(master,text="Durée : ")
        self.compteurDuree=Spinbox(master,from_=-2,to=1000000,width=8)
        self.compteurDuree.delete(0,END)
        self.compteurDuree.insert(0,'0')
        self.labelOperateur=Label(master,text="Ajout/Retrait : ")
        self.operateurEffet=StringVar()
        self.operateurList=OptionMenu(master,self.operateurEffet,*['+','-'])
        self.operateurEffet.set('+')
        self.labelValeur=Label(master,text="Valeur du buff : ")
        self.valeurEffet=StringVar()
        self.entryValeur=Entry(master,textvariable=self.valeurEffet,width=5)
        self.labelMaximum=Label(master,text="Dépasser le maximum ? : ")
        self.depasserMaximum=StringVar()
        self.listDepasserMaximum=OptionMenu(master,self.depasserMaximum,*['Oui','Non'])
        self.depasserMaximum.set('Oui')
        self.frameConditions=FrameConditions(master,text='Conditions')
        self.frameConditions.grid(row=1,column=0,columnspan=8,sticky='NSEW')
        
        self.frameInterdictions=FrameInterdictions(master,text='Interdiction')
        
        self.labelCaract=Label(master,text="Caractéristique : ")
        self.caractEffet=StringVar()
        self.listCaract=OptionMenu(master,self.caractEffet,*univers.reglages.caracts+['vitesse','pvBase','pv','poidsPortable','poidsPortes'])
        self.labelAtion=Label(master,text="Action : ")
        self.listAction=AutocompleteCombobox(master,width=15)
        self.listAction.set_completion_list([action.id for action in univers.actions])
        self.labelEtat=Label(master,text="Etat : ")
        self.etatEffet=StringVar()
        self.listEtat=OptionMenu(master,self.etatEffet,*['0: mort','1: en forme','2: fatigué','3: immobilisé','4: gelé','5: inconscient'])
        self.labelCoord=Label(master,text="Coordonnées de l'emplacement : ")
        self.coordTeleport=StringVar()
        self.entryCoord=Entry(master,textvariable=self.coordTeleport,width=7)
        self.labelEmplacement=Label(master,text="ID de l'emplacement")
        self.idEmplacement=StringVar()
        self.entryEmplacement=Entry(master,textvariable=self.idEmplacement,width=15)
        self.labelObjet=Label(master,text="Objet : ")
        self.listObjet=AutocompleteCombobox(master,width=15)
        self.listObjet.set_completion_list([objet.id for objet in univers.objets])
        self.labelQuantite=Label(master,text="Quantité : ")
        self.compteurQuantite=Spinbox(master,from_=0,to=100000,width=8)
        self.compteurQuantite.delete(0,END)
        self.compteurQuantite.insert(0,'0')
        self.labelQueteOperateur=Label(master,text="Opérateur : ")    
        self.operateurQuete=StringVar()
        self.listQueteOperateur=OptionMenu(master,self.operateurQuete,*['Ajouter','Retirer','Achever'])    
        self.operateurQuete.set('Ajouter')
        self.labelQuete=Label(master,text="Quête : ")    
        self.listQuete=AutocompleteCombobox(master,width=15)
        self.listQuete.set_completion_list([quete.nom for quete in univers.quetes])        
        self.labelHostil=Label(master,text="Créature : ")
        self.listHostil=AutocompleteCombobox(master,width=15)
        self.listHostil.set_completion_list([creature.id for creature in univers.creatures])
        
        self.conditions=[]

    def validate(self):
        type = self.lDeroulType.get()
        if type == 'buff':
            if (re.match(r'^-?\d+$',self.compteurDuree.get()) == None) or (int(self.compteurDuree.get()) < -2): 
                showinfo('Erreur','Durée non valide. Ne doit contenir que des nombres supérieurs ou égales à -2.')
                return False
            if (not self.caractEffet.get() in univers.reglages.caracts) or (self.caractEffet.get()==''):
                showinfo('Erreur','Caractéristique invalide.')
                return False
            if re.match(r'^\d+\.?\d*$',self.valeurEffet.get()) == None: 
                showinfo('Erreur','Valeur invalide. Ne peut contenir que des nombres entiers ou décimaux sous la forme 1.5')
                return False
        elif type == 'interdiction':
            if (re.match(r'^-?\d+$',self.compteurDuree.get()) == None) or (int(self.compteurDuree.get()) < -2): 
                showinfo('Erreur','Durée non valide. Ne doit contenir que des nombres supérieurs ou égales à -2.')
                return False
            if self.frameInterdictions.listType.get()=='':
                showinfo('Erreur','Aucune interdiction sélectionnée.')
                return False
            if (self.frameInterdictions.listType.get() in ['poss','unposs','equip','unequip','ramasser','jeter','utiliser']) and (re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.frameInterdictions.listObjet.get()) == None):
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'un objet (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
            if (self.frameInterdictions.listType.get() in ['entrer','sortir']) and ((re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.frameInterdictions.listRegion.get()) == None) and (re.match(r'^\d+,\d+$',self.frameInterdictions.listRegion.get()) == None)):
                showinfo('Erreur',"Entrée invalide. Contient soit les coordonnées d'un région sous la forme 10,20, l'id d'une région (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
            if (self.frameInterdictions.listType.get()=='rencontrer') and (re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.frameInterdictions.listCreature.get()) == None):
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'une créature (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
        elif type=='etat':
            if (re.match(r'^-?\d+$',self.compteurDuree.get()) == None) or (int(self.compteurDuree.get()) < -2): 
                showinfo('Erreur','Durée non valide. Ne doit contenir que des nombres supérieurs ou égales à -2.')
                return False
            if self.etatEffet.get()=='':
                showinfo('Erreur','Etat non sélectionné.')
                return False
        elif type=='teleportation':
            if re.match(r'^\d+,\d+$',self.coordTeleport.get()) == None: 
                showinfo('Erreur','Coordonnées non valides. Doivent être sous la forme 10,20.')
                return False
        elif type=='objet':
            if re.match(r"^[\w \-éèà'çäâëêÿüûïîöô]+$",self.listObjet.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient l'id d'un objet (caractères alpha-numériques et underscore).")
                return False
            if (re.match(r'^\d+$',self.compteurQuantite.get()) == None) or (int(self.compteurQuantite.get()) < 0): 
                showinfo('Erreur','Quantité non valide. Ne doit contenir que des entiers supérieurs ou égales 0.')
                return False
            if findObjectFromID(univers.objets,self.listObjet.get())==None:
                showinfo('Erreur','Objet inexistant.')
                return False
        elif type=='action':
            if (re.match(r'^-?\d+$',self.compteurDuree.get()) == None) or (int(self.compteurDuree.get()) < -2): 
                showinfo('Erreur','Durée non valide. Ne doit contenir que des nombres supérieurs ou égales à -2.')
                return False
            if re.match(r"^[\w \-éèà'çäâëêÿüûïîöô]+$",self.listAction.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient l'id d'une action (caractères alpha-numériques et underscore).")
                return False
            if findObjectFromID(univers.actions,self.listAction.get())==None:
                showinfo('Erreur','Action inexistante.')
                return False
        elif type=='hostilite':
            if (re.match(r'^-?\d+$',self.compteurDuree.get()) == None) or (int(self.compteurDuree.get()) < -2): 
                showinfo('Erreur','Durée non valide. Ne doit contenir que des nombres supérieurs ou égales à -2.')
                return False
            if re.match(r"^([\w \-éèàçäâëê'ÿüûïîöô]+|#\w+)$",self.listHostil.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient soit l'id d'une créature (caractères alpha-numériques et underscore) ou un mot clé (commencant par #).")
                return False
            if self.listHostil.get()[0] != '#' and self.listHostil.get()==None:
                showinfo('Erreur','Créature inexistante.')
                return False
        elif type=='emplacement':
            if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.idEmplacement.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient l'id de emplacement (caractères alpha-numériques et underscore).")
                return False
        elif type=='quete':
            if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.listQuete.get()) == None: 
                showinfo('Erreur',"Entrée invalide. Contient le nom d'une quête (caractères alpha-numériques et underscore).")
                return False
            if findObjectFromID(univers.quetes,self.listQuete.get())==None:
                showinfo('Erreur','Quete inexistante.')
                return False
        return True
    
    def createEffect(self):
        type = self.lDeroulType.get()
        if type == 'buff': self.effet = "buff {0} {1} {2}{3} {4} {5} {6}".format(self.compteurDuree.get(),self.caractEffet.get(),self.operateurEffet.get(),self.valeurEffet.get(),str(self.depasserMaximum == 'Oui').lower(),'['+"/".join(self.frameConditions.conditions)+']',str(time.clock()))
        elif type == 'etat': self.effet = "etat {0} {1} {2} {3}".format(self.compteurDuree.get(),self.etatEffet.get()[0],'['+"/".join(self.frameConditions.conditions)+']',str(time.clock()))
        elif type =='interdiction': self.effet = "interdiction {0} {1}{2} {3} {4}".format(self.compteurDuree.get(),self.operateurEffet.get(),self.frameInterdictions.interdiction,'['+"/".join(self.frameConditions.conditions)+']',str(time.clock()))
        elif type == 'teleportation': self.effet = "teleportation {0} {1}".format(self.coordTeleport.get(),'['+"/".join(self.frameConditions.conditions)+']')
        elif type == 'objet': self.effet = "objet {0}{1} {2} {3}".format(self.operateurEffet.get(),self.listObjet.get(),self.compteurQuantite.get(),'['+"/".join(self.frameConditions.conditions)+']')
        elif type == 'action': self.effet = "action {0} {1}{2} {3} {4}".format(self.compteurDuree.get(),self.operateurEffet.get(),self.listAction.get(),'['+"/".join(self.frameConditions.conditions)+']',str(time.clock()))
        elif type == 'hostilite': self.effet = "hostilite {0} {1}{2} {3} {4}".format(self.compteurDuree.get(),self.operateurEffet.get(),self.listHostil.get(),'['+"/".join(self.frameConditions.conditions)+']',str(time.clock()))
        elif type == 'emplacement': self.effet = "emplacement {0}{1} {2}".format(self.operateurEffet.get(),self.idEmplacement.get(),'['+"/".join(self.frameConditions.conditions)+']')
        elif type == 'quete': self.effet = "quete {0} {1} {2}".format(self.operateurQuete.get(),self.listQuete.get(),'['+"/".join(self.frameConditions.conditions)+']')
    
    def apply(self):
        self.result = self.effet
        
    def ok(self, event = None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        if self.lDeroulType.get()=='interdiction': self.frameInterdictions.createInterdiction()
        self.createEffect()
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
        
    def clean(self):
        type = self.oldType
        if type=="buff":
            self.labelDuree.grid_forget()
            self.compteurDuree.grid_forget()
            self.labelOperateur.grid_forget()
            self.operateurList.grid_forget()
            self.labelValeur.grid_forget()
            self.entryValeur.grid_forget()
            self.labelCaract.grid_forget()
            self.listCaract.grid_forget()
            self.labelMaximum.grid_forget()
            self.listDepasserMaximum.grid_forget()
        elif type=="interdiction": 
            self.labelDuree.grid_forget()
            self.compteurDuree.grid_forget()
            self.labelOperateur.grid_forget()
            self.operateurList.grid_forget()
            self.frameInterdictions.grid_forget()
        elif type=="etat":
            self.labelDuree.grid_forget()
            self.compteurDuree.grid_forget()
            self.labelEtat.grid_forget()
            self.listEtat.grid_forget()
        elif type=="teleportation":
            self.labelCoord.grid_forget()
            self.entryCoord.grid_forget()
        elif type=="objet":
            self.labelOperateur.grid_forget()
            self.operateurList.grid_forget()
            self.labelObjet.grid_forget()
            self.listObjet.grid_forget()
            self.labelQuantite.grid_forget()
            self.compteurQuantite.grid_forget()
        elif type=="action":
            self.labelDuree.grid_forget()
            self.compteurDuree.grid_forget()
            self.labelOperateur.grid_forget()
            self.operateurList.grid_forget()
            self.labelAtion.grid_forget()
            self.listAction.grid_forget()
        elif type=="hostilite":
            self.labelDuree.grid_forget()
            self.compteurDuree.grid_forget()
            self.labelOperateur.grid_forget()
            self.operateurList.grid_forget()
            self.labelHostil.grid_forget()
            self.listHostil.grid_forget()
        elif type=="emplacement":
            self.labelOperateur.grid_forget()
            self.operateurList.grid_forget()
            self.labelEmplacement.grid_forget()
            self.entryEmplacement.grid_forget()
        elif type=="quete":
            self.labelQueteOperateur.grid_forget()
            self.listQueteOperateur.grid_forget()
            self.labelQuete.grid_forget()
            self.listQuete.grid_forget()
        
    def gererType(self,event):
        self.clean()
        type = self.lDeroulType.get()
        self.oldType=type
        if type=="buff":
            self.labelDuree.grid(row=0,column=2)
            self.compteurDuree.grid(row=0,column=3)
            self.labelOperateur.grid(row=0,column=4)
            self.operateurList.grid(row=0,column=5)
            self.labelValeur.grid(row=0,column=6)
            self.entryValeur.grid(row=0,column=7)
            self.labelCaract.grid(row=0,column=8)
            self.listCaract.grid(row=0,column=9)
            self.labelMaximum.grid(row=0,column=10)
            self.listDepasserMaximum.grid(row=0,column=11)
        elif type=="interdiction": 
            self.labelDuree.grid(row=0,column=2)
            self.compteurDuree.grid(row=0,column=3)
            self.labelOperateur.grid(row=0,column=4)
            self.operateurList.grid(row=0,column=5)
            self.frameInterdictions.grid(row=0,column=6)
        elif type=="etat":
            self.labelDuree.grid(row=0,column=2)
            self.compteurDuree.grid(row=0,column=3)
            self.labelEtat.grid(row=0,column=4)
            self.listEtat.grid(row=0,column=5)
        elif type=="teleportation":
            self.labelCoord.grid(row=0,column=2)
            self.entryCoord.grid(row=0,column=3)
        elif type=="objet":
            self.labelOperateur.grid(row=0,column=2)
            self.operateurList.grid(row=0,column=3)
            self.labelObjet.grid(row=0,column=4)
            self.listObjet.grid(row=0,column=5,pady=5)
            self.labelQuantite.grid(row=0,column=6)
            self.compteurQuantite.grid(row=0,column=7)
        elif type=="action":
            self.labelDuree.grid(row=0,column=2)
            self.compteurDuree.grid(row=0,column=3)
            self.labelOperateur.grid(row=0,column=4)
            self.operateurList.grid(row=0,column=5)
            self.labelAtion.grid(row=0,column=6)
            self.listAction.grid(row=0,column=7)
        elif type=="hostilite":
            self.labelDuree.grid(row=0,column=2)
            self.compteurDuree.grid(row=0,column=3)
            self.labelOperateur.grid(row=0,column=4)
            self.operateurList.grid(row=0,column=5)
            self.labelHostil.grid(row=0,column=6)
            self.listHostil.grid(row=0,column=7)
        elif type=="emplacement":
            self.labelOperateur.grid(row=0,column=2)
            self.operateurList.grid(row=0,column=3)
            self.labelEmplacement.grid(row=0,column=4)
            self.entryEmplacement.grid(row=0,column=5)
        elif type=="quete":
            self.labelQueteOperateur.grid(row=0,column=2)
            self.listQueteOperateur.grid(row=0,column=3)
            self.labelQuete.grid(row=0,column=4)
            self.listQuete.grid(row=0,column=5)
'''class askPortail(Dialog):
    def body(self,master):
        self.labelNom=Label(master,text="Nom : ")
        self.nom=StringVar()
        self.entryNom=Entry(master,textvariable=self.nom)
        self.labelID=Label(master,text="ID : ")
        self.ID=StringVar()
        self.entryID=Entry(master,textvariable=self.ID)
        self.frameConditions=FrameConditions(master,text="Conditions d'utilisation")
        self.labelDestination=Label(master,text="Destination")
        self.destination=StringVar()
        self.entryDestination=Entry(master,textvariable=self.destination)
        self.labelEtat=Label(master,text="Etat :")
        self.etat=StringVar()
        self.listEtat=OptionMenu(master,self.etat,*['0: Caché','1: Découvert'])
        self.etat.set('1: Découvert')
        self.labelJet=Label(master,text="Multiplicateur de fouille")
        self.compteurJet=Spinbox(master,from_=0.0,to=1000.0,increment=0.1)
        self.compteurJet.delete(0,END)
        self.compteurJet.insert(0,1)
        self.labelNom.grid(row=0,column=0)
        self.entryNom.grid(row=0,column=1)
        self.labelID.grid(row=0,column=2)
        self.entryID.grid(row=0,column=3)
        self.labelDestination.grid(row=0,column=4)
        self.entryDestination.grid(row=0,column=5)
        self.labelEtat.grid(row=1,column=1)
        self.listEtat.grid(row=1,column=2)
        self.labelJet.grid(row=1,column=3)
        self.compteurJet.grid(row=1,column=4)
        self.frameConditions.grid(row=2,column=0,columnspan=10,sticky='nsew')
        self.charger()
    def charger(self):
        if self.item:
            self.nom.set(self.item[0].nom)
            self.ID.set(self.item[0].id)
            self.destination.set(str(self.item[0].destination[0])+","+str(self.item[0].destination[1]))
            self.etat.set(['0: Caché','1: Découvert'][self.item[1][0]])
            self.compteurJet.delete(0,END)
            self.compteurJet.insert(0,self.item[1][1])
            self.frameConditions.clear()
            self.frameConditions.update(self.item[0].conditionsUtil)
        else: self.item=[None,[0,0]]
    def validate(self):
        if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.nom.get()) == None:
            showinfo('Erreur',"Nom invalide. Peut contenir des caractères alpha-numériques et underscore.")
            return False
        if re.match((r"^\w+$"),self.ID.get()) == None:
            showinfo('Erreur',"ID invalide. Peut contenir des caractères alpha-numériques et underscore.")
            return False
        if re.match(r'^\d+,\d+$',self.destination.get()) == None: 
            showinfo('Erreur','Coordonnées non valides. Doivent être sous la forme 10,20.')
            return False
        if re.match(r'^\d+\.?\d*$',self.compteurJet.get()) == None: 
                showinfo('Erreur','Multiplicateur invalide. Ne peut contenir que des nombres entiers ou décimaux sous la forme 1.5')
                return False
        return True
    def apply(self):
        self.result = self.item
    def ok(self, event = None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.createPortail()
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
    def createPortail(self):
        self.item[0]=Portail()
        self.item[0].nom=self.nom.get()
        self.item[0].id=self.ID.get()
        self.item[0].destination=(int(self.destination.get().split(',')[0]),int(self.destination.get().split(',')[1]))
        self.item[0].conditionsUtil=self.frameConditions.conditions[:]
        self.item[1][0]=int(self.etat.get()[0])
        self.item[1][1]=float(self.compteurJet.get())'''
class askObjetOrCrea(Dialog):
    def body(self,master):
        
        if self.type=="portail":
            self.labelNom=Label(master,text="Nom : ")
            self.nom=StringVar()
            self.entryNom=Entry(master,textvariable=self.nom)
            self.labelID=Label(master,text="ID : ")
            self.ID=StringVar()
            self.entryID=Entry(master,textvariable=self.ID)
            self.frameConditions=FrameConditions(master,text="Conditions d'utilisation")
            self.labelDestination=Label(master,text="Destination")
            self.destination=StringVar()
            self.entryDestination=Entry(master,textvariable=self.destination)
        
        elif self.type=="objet": 
            self.listObject=AutocompleteCombobox(master,width=15)
            self.listObject.set_completion_list([objet.id for objet in univers.objets])
        elif self.type=="creature": 
            self.listObject=AutocompleteCombobox(master,width=15)
            self.listObject.set_completion_list([creature.id for creature in univers.creatures])
        
        self.labelEtat=Label(master,text="Etat :")
        self.etat=StringVar()
        self.listEtat=OptionMenu(master,self.etat,*['0: Caché','1: Découvert'])
        self.etat.set('1: Découvert')
        self.labelJet=Label(master,text="Multiplicateur de fouille")
        self.compteurJet=Spinbox(master,from_=0.0,to=1000.0,increment=0.1)
        self.compteurJet.delete(0,END)
        self.compteurJet.insert(0,1)
        
        if self.type=="portail":
            self.labelNom.grid(row=0,column=0)
            self.entryNom.grid(row=0,column=1)
            self.labelID.grid(row=0,column=2)
            self.entryID.grid(row=0,column=3)
            self.labelDestination.grid(row=0,column=4)
            self.entryDestination.grid(row=0,column=5)
            self.labelEtat.grid(row=1,column=1)
            self.listEtat.grid(row=1,column=2)
            self.labelJet.grid(row=1,column=3)
            self.compteurJet.grid(row=1,column=4)
            self.frameConditions.grid(row=2,column=0,columnspan=10,sticky='nsew')
        else:
            self.listObject.grid(row=0,column=0)
            self.labelEtat.grid(row=0,column=1)
            self.listEtat.grid(row=0,column=2)
            self.labelJet.grid(row=0,column=3)
            self.compteurJet.grid(row=0,column=4)
        
        self.charger()
        
    def charger(self):
        if self.item:
            if self.type=="portail":
                self.nom.set(self.item[0].nom)
                self.ID.set(self.item[0].id)
                self.destination.set(str(self.item[0].destination[0])+","+str(self.item[0].destination[1]))
                self.frameConditions.clear()
                self.frameConditions.update(self.item[0].conditionsUtil)
            
            if self.type in ['creature','objet']: self.listObject.set(self.item[0].id)
            
            self.etat.set(['0: Caché','1: Découvert'][self.item[1][0]])
            self.compteurJet.delete(0,END)
            self.compteurJet.insert(0,self.item[1][1])
        else: self.item=[None,[0,0]]
        
    def validate(self):
        if self.type=="portail":
            if re.match(r"^[\w éèà'çäâëêÿüûïîöô]+$",self.nom.get()) == None:
                showinfo('Erreur',"Nom invalide. Peut contenir des caractères alpha-numériques et underscore.")
                return False
            if re.match((r"^\w+$"),self.ID.get()) == None:
                showinfo('Erreur',"ID invalide. Peut contenir des caractères alpha-numériques et underscore.")
                return False
            if re.match(r'^\d+,\d+$',self.destination.get()) == None: 
                showinfo('Erreur','Coordonnées non valides. Doivent être sous la forme 10,20.')
                return False
        if re.match(r'^\d+\.?\d*$',self.compteurJet.get()) == None: 
            showinfo('Erreur','Multiplicateur invalide. Ne peut contenir que des nombres entiers ou décimaux sous la forme 1.5')
            return False
        if self.type=="objet" and findObjectFromID(univers.objets,self.listObject.get())==None:
            showinfo('Erreur','Objet inexistant.')
            return False
        elif self.type=="creature" and findObjectFromID(univers.creatures,self.listObject.get())==None:
            showinfo('Erreur','Objet inexistant.')
            return False
        return True
        
    def apply(self):
        self.result=self.item
        
    def ok(self, event = None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.createItem()
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
        
    def createItem(self):
        if self.type=="objet": self.item[0]=findObjectFromID(univers.objets,self.listObject.get(),)
        elif self.type=="creature": self.item[0]=findObjectFromID(univers.creatures,self.listObject.get())
        elif self.type=="portail": 
            self.item[0]=Portail()
            self.item[0].nom=self.nom.get()
            self.item[0].id=self.ID.get()
            self.item[0].destination=(int(self.destination.get().split(',')[0]),int(self.destination.get().split(',')[1]))
            self.item[0].conditionsUtil=self.frameConditions.conditions[:]
        self.item[1][0]=int(self.etat.get()[0])
        self.item[1][1]=float(self.compteurJet.get())
        
        
        
        
        

if 1+1==2:

    univers = Univers()
    univers.reglages.caracts=['adresse','force','intelligence','charisme','courage']
    univers.dialogues={}
    univers = univers

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
    morsure.description = "Une vilaine morsure d'une bête avec des dents pointues."
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
    coup_de_cornes.description = "La bête charge et frappe de plein fouet avec ses cornes."
    coup_de_cornes.effets = ['buff -2 pv -4 false [] 669']
    coup_de_cornes.esquive = True
    coup_de_cornes.nom = 'Coup de cornes'
    coup_de_cornes.util = 2
    coup_de_cornes.tIncant = 2
    coup_de_massue_de_troll = Action()
    coup_de_massue_de_troll.id = 'coup_de_massue_de_troll'
    coup_de_massue_de_troll.cible = 1
    coup_de_massue_de_troll.description = "Un redoutable coup donné par la massue d'un troll."
    coup_de_massue_de_troll.effets = ['buff -2 pv -8 false [] 670']
    coup_de_massue_de_troll.esquive = True
    coup_de_massue_de_troll.nom = 'Coup de massue de troll'
    coup_de_massue_de_troll.util = 2
    univers.actions = [coup_de_poignard_en_fer,coup_de_poignard_durandil,morsure,coup_de_cornes,coup_de_massue_de_troll,soin]

    piece_or = Objet()
    piece_or.poids = 0.01
    piece_or.description = "Les pièces d'or sont la monnaie la plus courante en terre de Fangh."
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
    chemise_voleur.description = "Une chemise sans doute disponible au marché noir."
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
    verre_d_eau_de_vie_de_qualite.description = "Un verre de tant en tant, ça fait de mal à personne."
    verre_d_eau_de_vie_de_qualite.effetsUtil = ['buff -2 pv +1 false [] 134529062015']
    verre_d_eau_de_vie_de_qualite.fonction = 2
    verre_d_eau_de_vie_de_qualite.nbrUse = 1
    verre_d_eau_de_vie_de_qualite.id = "verre_d_eau_de_vie_de_qualite"
    verre_d_eau_de_vie_de_qualite.motsCles = ['#boisson','#alcool','#consommable']
    verre_d_eau_de_vie_de_qualite.nom = "Verre d'eau de vie de qualité"
    verre_d_eau_de_vie_de_qualite.prix = 1.5
    poignard_base = Objet()
    poignard_base.poids = 0.5
    poignard_base.description = "Un vulgaire poignard en fer. Légèrement émoussé."
    poignard_base.effetsEquip = ['action -1 +coup_de_poignard_en_fer [] 290620152035','buff -1 attaque -2 false [] 290620152040','buff -1 charisme -1 false [] 290620152041']
    poignard_base.empEquip = ['main_gauche', 'main_droite']
    poignard_base.fonction = 1
    poignard_base.id = "poignard_base"
    poignard_base.motsCles = ['#poignard','#fer','#arme']
    poignard_base.nom = "Poignard de base en fer"
    poignard_base.prix = 10
    poignard_durandil = Objet()
    poignard_durandil.poids = 0.3
    poignard_durandil.description = "Un poignard durandil en acier de qualité."
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

    dialogueChevre = Dialogue(text='Béééééééééééééééééhéhéhéhhé.')
    dialogueChevre.reponses = {'Béhéhééé ?' : Dialogue(text="Béhé...")}
    dialogueChevre.id = "dialogueChevre"
    dialogueVoyageur = Dialogue(text='Bonjour !')
    dialogueVoyageur2 = Dialogue(text='Tout va pour le mieux ! ')
    dialogueVoyageur3 = Dialogue(text='Bonne route.')
    dialogueVoyageur4 = Dialogue(text="Ahhh. Eh bien ma femme m'a quittée, dieu en soit béni mais mes enfants sont partis avec elle. C'est plus silencieux me direz vous, c'est vrai, mais du coup je me retrouve tout seul.")
    dialogueVoyageur5 = Dialogue(text="Oh! Du calme.")
    dialogueVoyageur6 = Dialogue(text="Ca ira pour cette fois, mais soyez plus prudent à l'avenir.")
    dialogueVoyageur7 = Dialogue(text="Je vais te niquez ta mère ptit con !")
    dialogueVoyageur8 = Dialogue(text="Pff... Longue histoire... En bref, j'ai perdu des poignards qui appartenaient à mon héritage familiale. Je fouille la région pour essayer de les retrouver...")
    dialogueVoyageur8.conditionsChoix = ['quete les_poignards_perdus 0']
    dialogueVoyageur9 = Dialogue(text="Effectivement, un petit peu d'aide ne serait pas de refus. C'est très gentil à vous. Ramenez-moi 5 poignards que vous aurez trouvé par terre. Vous serez récompensé.")
    dialogueVoyageur10 = Dialogue(text="Merci à vous, je ne bougerais pas d'ici. Vous savez où me trouver.")
    dialogueVoyageur10.effetsChoix = ['quete ajouter les_poignards_perdus []']
    dialogueVoyageur11 = Dialogue(text = "Vous les avez trouvé ?",conditionsChoix = ['quete les_poignards_perdus 1'])
    dialogueVoyageur12 = Dialogue(text="D'accord. Ils n'ont aucune valeur, si ce n'est une valeur sentimentale. Ils viennent de mon arrière grand-père paternel !")
    dialogueVoyageur13 = Dialogue(text="Merveilleux ! Tenez, voilà votre récompense. Merci encore et bonne route !",conditionsChoix=['poss poignard_base > 9','objectif les_poignards_perdus ramasser_poignards 2'],effetsChoix=['objet -poignard_base 5 []','objet +piece_or 75 []','quete achever les_poignards_perdus []'])
    dialogueVoyageur11.reponses = {"Non, pas encore." : dialogueVoyageur12, "Oui, tenez. (Terminer la quête)" : dialogueVoyageur13}
    dialogueVoyageur.reponses = {"Bonjour, comment ça va ?" : dialogueVoyageur2,"Tu regardes quoi fils de pute ? Tu veux ma photo ?" : dialogueVoyageur5,"Que faites-vous ici ?" : dialogueVoyageur8,"A propos des poignards..." : dialogueVoyageur11}
    dialogueVoyageur8.reponses = {"Vous avez besoin d'aide ?" : dialogueVoyageur9,"Bonne chance." : dialogueVoyageur3}
    dialogueVoyageur9.reponses = {"Si c'est récompensé, alors j'accepte. (Accepter la quête)" : dialogueVoyageur10,"Désolé, je vous aurais bien aidé mais je crains que vos poignards soient définitivement perdus... Bonne chance. (Refuser la quête)" : dialogueVoyageur3}
    dialogueVoyageur2.reponses = {"Tant mieux ! Bonne journée..." : dialogueVoyageur3, "Comment va la famille ?" : dialogueVoyageur4}
    dialogueVoyageur5.reponses = {"Excusez-moi... Je vous ai pris pou quelqu'un d'autre..." : dialogueVoyageur6, "Tu vas faire quoi ?" : dialogueVoyageur7}
    dialogueVoyageur.id="dialogueVoyageur"
    univers.dialogues={'dialogueChevre':dialogueChevre,'dialogueVoyageur':dialogueVoyageur}

    bouc = Creature()
    bouc.id = 'bouc'
    bouc.nom = 'Bouc'
    bouc.actions = ['coup_de_cornes','soin']
    bouc.amisAvec = ['bouc']
    bouc.caracteristiques.update({'courage' : 7, 'adresse' : 13, 'attaque' : 9, 'pvBase' : 15, 'pv' : 15})
    bouc.caracteristiques.setParent(bouc)
    bouc.description = "Une innofensive créature qui passe ses journées à brouter l'herbe verte."
    bouc.dialogue = dialogueChevre
    bouc.motsCles = ['#bouc','#betail','#innofensif']
    bouc.exp_win = 3
    bouc.hostil = 5
    bouc.strategieDefensive = 2
    bouc.strategieOffensive = 2
    bouc.inventaire = ['piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or']
    coyote_affame = Creature()
    coyote_affame.id = 'coyote_affame'
    coyote_affame.nom = 'Coyote affamé'
    coyote_affame.actions = ['morsure']
    coyote_affame.caracteristiques.update({'courage' : 11, 'adresse' : 12, 'attaque' : 19, 'pvBase' : 18, 'pv' : 15})
    coyote_affame.caracteristiques.setParent(coyote_affame)
    coyote_affame.description = "Un dangereux charognard qui chasse la nuit."
    coyote_affame.motsCles = ['#coyote_affame','#charognard','#agressif']
    coyote_affame.exp_win = 4
    coyote_affame.hostil = 7
    coyote_affame.inventaire = ['piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or']
    rat_pesteux = Creature()
    rat_pesteux.id = 'rat_pesteux'
    rat_pesteux.nom = 'Rat pesteux'
    rat_pesteux.actions = ['morsure']
    rat_pesteux.amisAvec = ['rat_pesteux']
    rat_pesteux.caracteristiques.update({'courage' : 5, 'adresse' : 13, 'attaque' : 11, 'pvBase' : 5, 'pv' : 5})
    rat_pesteux.caracteristiques.setParent(rat_pesteux)
    rat_pesteux.description = "Un misérable rat portant toutes les maladies imaginables et couinant à longueur de journée."
    rat_pesteux.motsCles = ['#rat_pesteux','#charognard','#hostil']
    rat_pesteux.exp_win = 4
    rat_pesteux.hostil = 6
    rat_pesteux.strategieOffensive = 0
    orque_miteux = Creature()
    orque_miteux.id = 'orque_miteux'
    orque_miteux.nom = 'Orque miteux'
    orque_miteux.actions = ['coup_de_poignard_en_fer']
    orque_miteux.amisAvec = ['orque_miteux']
    orque_miteux.caracteristiques.update({'courage' : 8, 'adresse' : 9, 'attaque' : 9, 'pvBase' : 15, 'pv' : 15})
    orque_miteux.caracteristiques.setParent(orque_miteux)
    orque_miteux.description = "Un orque ayant quitté sa légion et s'étant reconverti en bandit de bas étage."
    orque_miteux.motsCles = ['#orque_miteux','#humanoide','#orque','#bandit']
    orque_miteux.exp_win = 8
    orque_miteux.hostil = 6
    orque_miteux.niveau = 2
    orque_miteux.strategieDefensive = 1
    orque_miteux.inventaire = ['piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','poignard_base']
    troll_geant_maladroit = Creature()
    troll_geant_maladroit.id = 'troll_geant_maladroit'
    troll_geant_maladroit.nom = 'Troll géant maladroit'
    troll_geant_maladroit.actions = ['coup_de_massue_de_troll']
    troll_geant_maladroit.amisAvec = ['troll_geant_maladroit']
    troll_geant_maladroit.caracteristiques.update({'courage' : 20, 'adresse' : 6, 'attaque' : 7, 'pvBase' : 50, 'pv' : 50})
    troll_geant_maladroit.caracteristiques.setParent(troll_geant_maladroit)
    troll_geant_maladroit.description = "Une innofensive créature qui passe ses journées à brouter l'herbe verte."
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
    voyageur.inventaire = ['piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or','piece_or']
    voyageur.motsCles = ['#voyageur','#humain']
    voyageur.dialogue = dialogueVoyageur

    univers.creatures = [bouc,coyote_affame,rat_pesteux,orque_miteux,troll_geant_maladroit,voyageur]
    plaine_du_ninejaddai = Region()
    plaine_du_ninejaddai.id = 'plaine_du_ninejaddai'
    plaine_du_ninejaddai.nom = 'Plaine du Ninejaddai'
    plaine_du_ninejaddai.regionParent = 'plaine_du_ninejaddai'
    plaine_du_ninejaddai.motsCles = ['#plaine','#ninejaddai']
    plaine_du_ninejaddai.creatures = []
    plaine_du_ninejaddai.creaturesRencontrables = ['bouc','orque_miteux','troll_geant_maladroit','rat_pesteux','coyote_affame']
    plaine_du_ninejaddai.description = "Une plaine sauvage malgré les nombreux pâturages de boucs."
    foret_de_schlipak = Region()
    foret_de_schlipak.id = 'foret_de_schlipak'
    foret_de_schlipak.regionParent = 'foret_de_schlipak'
    foret_de_schlipak.nom = 'Forêt de Schlipak'
    foret_de_schlipak.motsCles = ['#foret']
    foret_de_schlipak.creaturesRencontrables = ['orque_miteux','troll_geant_maladroit']
    foret_de_schlipak.description = "Une grande forêt peuplée de divers peuples et diverses créatures."
    plaine_du_ninejaddai_lisiere_schlipak = Region()
    plaine_du_ninejaddai_lisiere_schlipak.id = 'plaine_du_ninejaddai_lisiere_schlipak'
    plaine_du_ninejaddai_lisiere_schlipak.nom = 'Plaine du Ninejaddai - Lisière de la forêt de Schlipak'
    plaine_du_ninejaddai_lisiere_schlipak.regionParent = 'plaine_du_ninejaddai'
    plaine_du_ninejaddai_lisiere_schlipak.motsCles = ['#plaine','#ninejaddai', '#lisiere','foret']
    plaine_du_ninejaddai_lisiere_schlipak.creatures = []
    plaine_du_ninejaddai_lisiere_schlipak.creaturesRencontrables = ['bouc','orque_miteux','troll_geant_maladroit','rat_pesteux']
    plaine_du_ninejaddai_lisiere_schlipak.description = "La lisière de la forêt de Schlipak avec la plaine du Ninejaddai."
    plaine_du_ninejaddai_route = Region()
    plaine_du_ninejaddai_route.id = 'plaine_du_ninejaddai_route'
    plaine_du_ninejaddai_route.nom = 'Plaine du Ninejaddai - Route de Zoyek'
    plaine_du_ninejaddai_route.regionParent = 'plaine_du_ninejaddai'
    plaine_du_ninejaddai_route.motsCles = ['#plaine','#ninejaddai','#route']
    plaine_du_ninejaddai_route.creatures = []
    plaine_du_ninejaddai_route.creaturesRencontrables = ['bouc','rat_pesteux']
    plaine_du_ninejaddai_route.description = "La route traversant la plaine du Ninejaddai et reliant Zoyek au lac de Zblouf."
    bordure_fleuve_elibed = Region()
    bordure_fleuve_elibed.id = 'bordure_fleuve_elibed'
    bordure_fleuve_elibed.regionParent = 'bordure_fleuve_elibed'
    bordure_fleuve_elibed.nom = 'Bordures du fleuve Elibed'
    bordure_fleuve_elibed.motsCles = ['#fleuve','#ninejaddai','#plaine']
    bordure_fleuve_elibed.creatures = []
    bordure_fleuve_elibed.creaturesRencontrables = ['bouc','orque_miteux','troll_geant_maladroit','rat_pesteux']
    bordure_fleuve_elibed.description = "Les bordures du fleuves Elibed qui sépare la plaine du Ninejaddai des terres sauvages de Kwzprtt."
    univers.regions = [plaine_du_ninejaddai,foret_de_schlipak,plaine_du_ninejaddai_lisiere_schlipak,plaine_du_ninejaddai_route,bordure_fleuve_elibed]
       
    univers.textes = {}
    univers.textes['entrer foret_de_schlipak nuit'] = ["Malgr� l'obscurit� de la nuit, vous p�n�trez dans la sombre for�t de Schlipak. Peu � peu les arbres se font de plus en plus dense et vous vous voyez vite tremp� par l'humidit� des plantes."]
    univers.textes['entrer foret_de_schlipak jour'] = ["Sous un soleil de plomb, vous p�n�trez dans la sombre for�t de Schlipak. Peu � peu l'air se rafraichit et l'humidit� de la for�t se fait sentir. La v�g�tation est tr�s dense et tr�s feuillue."]
    univers.textes['entrer 2,5  *'] = ["Vous p�n�trez dans la sombre for�t de Schlipak. Peu � peu la v�g�tation s'�paissit et vous voyez difficilement � plus de 50m."]
    univers.textes['entrer 2,5  nuit'] = ["Vous p�n�trez dans la sombre for�t de Schlipak EN PLEINE NUIT. Peu � peu la v�g�tation s'�paissit et vous voyez difficilement � plus de 50m."]
    univers.textes['entrer plaine_du_ninejaddai jour'] = ["Vous arrivez dans les vastes plaines du Ninejaddai. Elles s'�tendent � perte de vue et vous observer quelques bosquets par ci par l�."]
    univers.textes['entrer plaine_du_ninejaddai nuit'] = ["Vous remarquez que, malgr� l'obscurit� qui vous entoure, le relief s'est aplati et qu'une plaine se dessine devant vous. Il s'agit de la plaine du Ninejaddai. Au loin, vous entendez des cris de coyotes."]
    univers.textes['entrer plaine_du_ninejaddai_lisiere_schlipak *'] = ["Vous arrivez � la lisi�re de la for�t de Schlipak. D'un côt� l'�paisse silhouette de la for�t, de l'autre le vide de la plaine du Ninejaddai."]
    univers.textes['entrer plaine_du_ninejaddai_route *'] = ["Vous rejoignez une route bien distincte qui traverse la plaine."]
    univers.textes['entrer bordure_fleuve_elibed *'] = ["Vous arrivez au bord du fleuve qui s�pare les terres sauvages de la plaine du Ninejaddai. Le courant est trop fort pour pouvoir franchir le fleuve."]
    univers.textes['decrire plaine_du_ninejaddai_route *'] = ["La route semble aller du sud-ouest au nord-est."]
    univers.textes['decrire 0,0 *'] = ["La route semble aller du sud � l'est."]
    univers.textes['decrire 1,0 *'] = ["La route semble aller de l'ouest au nord-est."]
    univers.textes['decrire 4,3 *'] = ["La route semble aller du sud-ouest au nord."]
    univers.textes['decrire 4,4 *'] = ["La route semble aller du sud au nord-est."]
    univers.textes['aller *'] = ["Vous vous dirigez vers %direction"]
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
    univers.textes['entrer * nuit'] = ["Vous avancez malgr�s l'obscurit� mais ne parvenez � distinguer ce qui vous entoure."]
    univers.textes['entrer * jour'] = ["Vous arrivez dans une nouvelle r�gion sous un soleil �clatant."]
    univers.textes['entrer * *'] = ["Vous arrivez dans une nouvelle r�gion."]
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


os.chdir("/")    
 
frame = Tk()
onglets = notebook(frame, LEFT)

onglet_reglages = FrameReglages(onglets())
onglet_actions = FrameObject(onglets(),type='action')
onglet_objets = FrameObject(onglets(),type='objet')
onglet_creatures = FrameObject(onglets(), type='creature')
onglet_dialogues = FrameDialog(onglets())
onglet_quetes = FrameQuest(onglets())
onglet_portails = FrameObject(onglets(),type="region")
onglet_map = MapEditor(onglets())
onglet_texte = FrameText(onglets())

menubar = Menu(frame)
menuFichier = Menu(menubar,tearoff=0)
menuFichier.add_command(label="Enregistrer",command=Enregistrer)
menuFichier.add_command(label="Charger",command=Charger)
menuEditeur = Menu(menubar,tearoff=0)
menuEditeur.add_command(label="Nouvelle image",command=onglet_map.newImg)
menuEditeur.add_command(label="Réinitialiser la répartition",command=onglet_map.viewer.remove_all)
menubar.add_cascade(label="Fichier", menu=menuFichier)
frame.config(menu=menubar)

# keeps the reference to the radiobutton (optional)
onglets.add_screen(onglet_reglages, "reglages")
onglets.add_screen(onglet_actions, "actions")
onglets.add_screen(onglet_objets, "objets")
onglets.add_screen(onglet_creatures, "creatures")
onglets.add_screen(onglet_dialogues, "dialogues")
onglets.add_screen(onglet_quetes, "quetes")
onglets.add_screen(onglet_portails, "portails")
onglets.add_screen(onglet_map,"map")
onglets.add_screen(onglet_texte,"textes")
onglet_reglages.load(univers.reglages)
onglet_dialogues.loadDialogs()
onglet_texte.load()


frame.mainloop()