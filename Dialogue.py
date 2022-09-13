# -*-coding:Latin-1 -*
class Dialogue:
    """D�finit un dialgoue. Contient:
    - text (string)(Contient le texte prononc� par la cr�ature.)
    - conditionChoix (list)(Liste de conditions pour que le dialogue puisse �tre choisi et vu.)
    - effetsChoix (list)(Liste d'effets activ�s lorsque le dialogue est choisi.)
    - reponses (dict)(Dictionnaire dont les cl�s repr�sentent le "texte" d'une r�ponse prononcable et dont les valeurs repr�sentent le dialogue() qu'elle entraine.)
	- id (string)(Permettant au jeu de diff�rencier les dialogues.)"""

    def __init__(self, text = '', conditionsChoix = [], effetsChoix = [], reponses = {}):
        self.text = text
        self.conditionsChoix = conditionsChoix
        self.effetsChoix = effetsChoix
        self.reponses = reponses
        self.id=''


