#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Différentes classes et algo."""

from random import shuffle

PRIORITY = {
    "AND": 1,
    "OR": 2,
    "THEN": 3,
    "NOT": 4,
    "(": 0,  # PARENTHESE
    ")": 0,  # PARENTHESE
    }

CARDS = {"A": 4, "B": 4, "C": 4, "D": 4,
         "AND": 4, "OR": 4, "THEN": 4,
         "NOT": 6, "(": 4, ")": 4,
#         "Fallacy": 3, "Justification": 3,
#         "TabulaRasa": 1, "Revolution": 1,
#         "WildVar": 1, "WildOp": 1,
#         "Ergo": 3,
        }


class Card(object):
    "Les cartes du jeu."
    def __init__(self, name: str):
        """Constructeur de la classe

         :param name: nom de la carte (ET, OU, AND, NOT, ...)
         :type name: string

         :return: Objet Card
         :rtype: Card
        """
        assert name in CARDS
        self.name = name

    def priority(self):
        """Renvoie le niveau de priorité de la carte.
        Si la carte n'a pas de niveau de priorité, renvoie une exception.

         :return: niveau de priorité
         :rtype: int
        """
        try:
            return PRIORITY[self.name]
        except KeyError:
            raise Exception("Card '{}' as no priority".format(self.name))

    def is_letter(self):
        """Indique si la carte est une lettre ou non.

         :rtype: boolean
        """
        return self.name in ["A", "B", "C", "D"]

    def is_operator(self) -> bool:
        """Indique si la carte est un opérateur

         :rtype: boolean
        """
        return self.name in ["AND", "OR", "THEN"]

    def is_open(self):
        """Indique si la carte est une parenthèse ouvrante."""
        return self.name == "("

    def is_close(self):
        """Indique si la carte est une parenthèse fermante."""
        return self.name == ")"

    def is_not(self):
        """Indique si la carte est un "NOT"."""
        return self.name == "NOT"

    def __repr__(self):
        return self.name


class CardList(list):
    """Liste de cartes, avec la Notation Polonaise Inversée associée.
    Si la liste ne correspond pas à une preuve syntaxiquement correcte,
    NPI vaut None."""
    def __init__(self, *args):
        """Initialisation de la liste."""
        super().__init__(*args)
        self.npi = self.to_npi()

    def append(self, card):
        """Ajoute la carte card à la  fin de la liste."""
        super().append(card)
        self.npi = self.to_npi()

    def insert(self, index, card):
        """Insère card à la position index."""
        super().insert(index, card)
        self.npi = self.to_npi()

    def pop(self, index=-1):
        """Supprime la carte en position index (par défaut la dernière)
        et la renvoie."""
        card = super().pop(index)
        self.npi = self.to_npi()
        return card

    def is_syntactically_correct(self):
        """Indique si la liste de cartes est syntaxiquement correcte,
        sans s'occuper de la correspondance des parenthèses."""
        if self == []:
            return True
        if len(self) == 1:
            return self[0].is_letter()
        if not (self[0].is_open() or self[0].is_letter() or self[0].is_not()):
            return False
        if self[-1].is_not() or self[-1].is_operator():
            return False
        for i_card in range(len(self)-1):
            card1, card2 = self[i_card], self[i_card+1]
            if card1.is_letter() or card1.is_close():
                if card2.is_letter() or card2.is_not():
                    return False
            if card1.is_operator():
                if card2.is_operator() or card2.is_close():
                    return False
            if card1.is_not():
                if card2.is_operator() or card2.is_close() or card2.is_not():
                    return False
            if card1.is_open():
                if card2.is_operator():
                    return False
        return not card2.is_operator()

    def to_npi(self):
        """Renvoie

         * None si la syntaxe de la liste n'est pas correcte

         * une liste de carte correspondant à la notation polonaise inversée de
           la liste de départ sinon."""
        if not self.is_syntactically_correct():
            return None
        npi_card_lst = []
        stack = []
        for card in self:
            if card.is_letter():
                npi_card_lst.append(card)
            elif card.is_open():
                stack.append(card)
            elif card.is_close():
                while stack != [] and not stack[-1].is_open():
                    npi_card_lst.append(stack.pop())
                if stack == []:  # PARENTHESE
                    return None
                else:
                    stack.pop()
            else:
                while stack != [] and stack[-1].priority() >= card.priority():
                    npi_card_lst.append(stack.pop())
                stack.append(card)
        while stack != []:
            card = stack.pop()
            if card.is_open():
                return None
            npi_card_lst.append(card)
        return npi_card_lst

    def evalue(self, model):
        """Évalue la liste en fonction du modèle. npi doit être calculé.
        :param model: liste de 4 booléens correspondant aux valeurs de
        A, B, C et D
        :type model: list
        :return: Valeur de la liste de carte en fonction du modèle.
        :rtype: boolean
        """
        assert self.npi is not None
        if self.npi == []:
            return True
        pile = []
        for carte in self.npi:
            if carte.is_letter():
                valeur = model[ord(carte.name)-ord('A')]
                pile.append(valeur)
            elif carte.is_operator():
                val2 = pile.pop()
                val1 = pile.pop()
                if carte.name == "AND":
                    val = val1 and val2
                elif carte.name == "OR":
                    val = val1 or val2
                else:  # "THEN"
                    val = (not val1) or val2
                pile.append(val)
            else:  # "NOT"
                pile.append(not pile.pop())
        val = pile.pop()
        assert pile == []
        return val


class Deck(list):
    """Le paquet de cartes."""
    def __init__(self):
        """Initialise le paquet de cartes."""
        super().__init__()
        for carte, nb in CARDS.items():
            self.extend([Card(carte)]*nb)
        shuffle(self)

    def draw(self, number):
        """Renvoie number cartes du paquet s'il en reste assez, la fin du
        paquet ou une liste vide sinon."""
        res = []
        while len(res) < number and self != []:
            res.append(self.pop())
        return res

    def append(self, card):
        """Ajoute une carte (possible avec Tabula Rasa)."""
        self.append(card)

    def reset(self):
        """Réinitialise le paquet de cartes."""
        self.__init__()

    def is_finished(self):
        """Indique si la paquet est terminé."""
        return self == []


class Proof(object):
    """Classe gérant les prémisses et la preuve."""
    def __init__(self):
        """Initialisation des attributs :

        * premises : liste de 4 CardList correspondant aux 4 lignes de
          prémisses;

        * currently_added : liste de cartes venant d'être ajoutées aux
          prémisses, et pas encore validées.
        """
        super().__init__()
        self.premises = [CardList() for _ in range(4)]
        self.currently_added = []

    def insert(self, premise, index, card):
        """Insère la carte card dans la prémisse premise en position index
        et actualise currently_added.

        Renvoie True si l'insertion est possible, False sinon."""
        if len(self.currently_added) >= 2:
            return False
        self.premises[premise].insert(index, card)
        if index >= len(self.premises[premise]):
            index = len(self.premises[premise])-1
        if self.currently_added != []:
            (premise1, index1) = self.currently_added.pop()
            if premise1 == premise and index1 >= index:
                index1 += 1
            self.currently_added.append((premise1, index1))
        self.currently_added.append((premise, index))
        return True

    def pop(self, premise, index):
        """Enlève la carte en position index de la prémisse premise à
        condition qu'elle vienne d'être ajoutée. Renvoie la carte en
        question ou None si on ne peut pas l'enlever."""
        try:
            self.currently_added.remove((premise, index))
        except ValueError:
            return None
        if self.currently_added != []:
            (premise1, index1) = self.currently_added.pop()
            if premise1 == premise and index1 >= index:
                index1 -= 1
            self.currently_added.append((premise1, index1))
        card = self.premises[premise].pop(index)
        return card

    def reset_added(self):
        """Remise à zéro de currently_added pour le prochain tour."""
        self.currently_added = []

    def is_all_correct(self):
        """Indique si toutes les prémisses sont correctes ou pas."""
        for premise in self.premises:
            if premise.to_npi() is None:
                return False
        return True

    def conclusion(self):
        """Renvoie None si les prémisses conduisent à une contradiction,
        ou une liste associant à chaque variable 'A', 'B', 'C' et 'D' soit True
        si elle est prouvée, False si la négation est prouvée, on None si on ne
        peut rien conclure."""
        possible = []
        for code in range(16):
            model = _to_bin(code)
            for premise in self.premises:
                if not premise.evalue(model):
                    break
            else:  # modele valable pour toutes les prémisses
                possible.append(model)
        if possible == []:
            return None
        result = possible[0]
        # il faut déterminer pour chaque lettre si toutes les valeurs possibles
        # sont les mêmes
        for model in possible:
            for i_lettre in range(4):
                if result[i_lettre] != model[i_lettre]:
                    result[i_lettre] = None
        return result


def _to_bin(n):
    """
    :param n: Un entier entre 0 et 15
    :type n: int
    :return: l'écriture booléenne en binaire sur 4 bits de n.
    :rtype: list
    Renvoie une liste de booléens correspondant à l'écriture en binaire sur 4
    bits de l'entier n."""
    res = [False]*4
    i = 3
    while n > 0:
        res[i] = (n % 2 == 1)
        n //= 2
        i -= 1
    return res


def _tests():
    """Des tests..."""
    card_list = CardList([Card("NOT"), Card("("), Card("A"), Card("AND"),
                          Card("NOT"), Card("B"), Card(")"), Card("AND"),
                          Card("D")])
    p = Proof()
    p.premises[0] = card_list
    p.premises[1] = CardList([Card("NOT"), Card("B")])
    p.premises[2] = CardList([Card("D"), Card("THEN"), Card("C")])
    print(p.conclusion())


if __name__ == '__main__':
    print("Bienvenue dans Ergo, le jeu où vous prouvez votre existence.")
    _tests()
