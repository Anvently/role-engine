# -*-coding:Latin-1 -*
class Dialogue:
    """Définit un dialgoue. Contient:
    - text (string)(Contient le texte prononcé par la créature.)
    - conditionChoix (list)(Liste de conditions pour que le dialogue puisse être choisi et vu.)
    - effetsChoix (list)(Liste d'effets activés lorsque le dialogue est choisi.)
    - reponses (dict)(Dictionnaire dont les clés représentent le "texte" d'une réponse prononcable et dont les valeurs représentent le dialogue() qu'elle entraine.)
	- id (string)(Permettant au jeu de différencier les dialogues.)"""

    def __init__(self, text = '', conditionsChoix = [], effetsChoix = [], reponses = {}):
        self.text = text
        self.conditionsChoix = conditionsChoix
        self.effetsChoix = effetsChoix
        self.reponses = reponses
        self.id=''


