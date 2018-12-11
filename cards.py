#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Différentes classes et algo."""

from random import shuffle
import constantes as cst


class Card(object):
    "Les cartes du jeu."
    def __init__(self, valeur):
        """Créé une carte de la valeur donnée"""
        self.image = cst.IMAGE[valeur]
        self.valeur = valeur

    def priority(self):
        """Renvoie le niveau de priorité de la carte.
        Si la carte n'a pas de niveau de priorité, renvoie une exception."""
        try:
            return cst.PRIORITY[self.valeur]
        except KeyError:
            raise Exception("Card '{}' as no priority".format(self.valeur))

    def is_letter(self):
        """"Indique si la carte est une lettre ou non."""
        return self.valeur in ["A", "B", "C", "D"]

    def is_operator(self):
        """Indique si la carte est un opérateur."""
        return self.valeur in ["AND", "OR", "THEN"]

    def is_open(self):
        """Indique si la carte est une parenthèse ouvrante."""
        return self.valeur == "("

    def is_close(self):
        """Indique si la carte est une parenthèse fermante."""
        return self.valeur == ")"

    def is_not(self):
        """Indique si la carte est un "NOT"."""
        return self.valeur == "NOT"

    def __repr__(self):
        return self.valeur


class CardList(list):
    """Liste de cartes."""
    def __init__(self, *args):
        """Initialisation de la liste."""
        super().__init__(*args)
        self.npi = self.to_npi()

    def append(self, card):
        super().append(card)
        self.npi = self.to_npi()

    def insert(self, index, card):
        super().insert(index, card)
        self.npi = self.to_npi()

    def pop(self, index=-1):
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
        """Prend en paramètre une liste de carte en notation infixe, et renvoie

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


class Deck(list):
    """Le paquet de cartes."""
    def __init__(self):
        """Initialise le paquet de cartes."""
        super().__init__([Card("A"), Card("B"), Card("C"), Card("D")] * 4 +
                         [Card("AND"), Card("OR"), Card("THEN")] * 4 +
                         [Card("NOT")] * 6 +
                         [Card("(")] * 8 +
                         # [Card("Fallacy"), Card("Justification")] * 3 +
                         # [Card("TabulaRasa"), Card("Revolution")] +
                         # [Card("WildVar"), Card("WildOp")] +
                         [Card("Ergo")] * 3
                        )
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
        super().append(card)

    def reset(self):
        """Réinitialise le paquet de cartes."""
        self.__init__()

    def is_finished(self):
        """Indique si la paquet est terminé."""
        return self == []


class Proof(object):
    """Classe gérant les prémices et la preuve."""
    def __init__(self):
        """Initialisation des attributs."""
        super().__init__()
        self.premises = [CardList() for _ in range(4)]
        self.correct = True
        self.currently_added = []

    def insert(self, premise, index, card):
        """Insère la carte card dans le prémice premise en position index
        et actualise currently_added."""
        self.premises[premise].insert(index, card)
        self.correct &= (self.premises[premise].npi is not None)
        if self.currently_added != []:
            (premise1, index1) = self.currently_added.pop()
            if premise1 == premise and index1 >= index:
                index1 += 1
            self.currently_added.append((premise1, index1))
        self.currently_added.append((premise, index))

    def pop(self, premise, index):
        """Enlève la carte en position index du prémice premise à condition qu'
        elle vienne d'être ajoutée. Renvoie la carte en question ou None si on
        ne peut pas l'enlever."""
        try:
            self.currently_added.remove((premise, index))
        except ValueError:
            return None
        if self.currently_added != []:
            (premise1, index1) = self.currently_added.pop()
            if premise1 == premise and index1 >= index:
                index1 -= 1
            self.currently_added.append((premise1, index1))
        return self.premises[premise].pop(index)

    def reset_added(self):
        """Remise à zéro de currently_added pour le prochain tour."""
        self.currently_added = []

    def conclusion(self):
        """TODO"""
        raise NotImplementedError


def tests():
    """Des tests..."""
    card_list = CardList([Card("NOT"), Card("NOT"), Card("("), Card("A"),
                          Card("AND"), Card("NOT"), Card("B"), Card(")"), Card("AND"),
                          Card("D")])
    print(card_list)
    print(card_list.npi)
    card_list.pop(0)
    print(card_list)
    print(card_list.npi)
    card_list.append(Card("OR"))
    card_list.append(Card("A"))
    print(card_list)
    print(card_list.npi)


if __name__ == '__main__':
    print("Bienvenue dans Ergo, le jeu où vous prouvez votre existence.")
    tests()
