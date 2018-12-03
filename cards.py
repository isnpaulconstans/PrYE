#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Différentes classes et algo."""

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
        return self.valeur in ["AND", "OR", "THEN", "NOT"]

    def is_open(self):
        """Indique si la carte est une parenthèse ouvrante."""
        return self.valeur == "("

    def is_close(self):
        """Indique si la carte est une parenthèse fermante."""
        return self.valeur == ")"

    def __repr__(self):
        return self.valeur


def to_npi(input_card_lst):
    """Prend en paramètre une liste de carte en notation d'infixe, et renvoie

     * None si le parenthésage de la liste n'est pas correct

     * une liste de carte correspondant à la notation polonaise inversée de
       la liste de départ sinon."""
    npi_card_lst = []
    stack = []
    for card in input_card_lst:
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
            while stack != [] and stack[-1].is_operator()\
                              and stack[-1].priority() >= card.priority():
                npi_card_lst.append(stack.pop())
            stack.append(card)
    while stack != []:
        card = stack.pop()
        if not card.is_operator():
            return None
        npi_card_lst.append(card)
    return npi_card_lst


if __name__ == '__main__':
    print("Bienvenue dans Ergo, le jeu où vous prouvez votre existence.")
    cardLst = [Card("("), Card("A"), Card("AND"), Card(")"), Card("B"), Card("OR"), Card("C")]
    print(to_npi(cardLst))
