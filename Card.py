#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les cartes du jeu."""

from Constantes import Constantes as Cst


class Card():
    """Les cartes du jeu."""
    # Le niveau de priorité de chaque carte
    __PRIORITY = {
        "THEN": 1,
        "OR": 2,
        "AND": 3,
        "NOT": 4,
        "(": 0,
        ")": 0,
        }

    def __init__(self, name):
        """Constructeur de la classe

        :param name: nom de la carte (ET, OU, AND, NOT, ...)
        :type name: string

        :return: Objet Card
        :rtype: Card
        """
        assert name in Cst.card_names()
        self.__name = name

    @property
    def name(self):
        """getter

        :return: nom de la carte
        :rtype: str
        """
        return self.__name

    @name.setter
    def name(self, name):
        """setter"""
        assert name in Cst.card_names()
        self.__name = name

    def priority(self):
        """
        :return: le niveau de priorité de la carte. Si la carte n'a pas de
                 niveau de priorité, lève une exception.
        :rtype: int
        """
        try:
            return Card.__PRIORITY[self.__name]
        except KeyError:
            raise Exception("Card '{}' as no priority".format(self.__name))

    def is_letter(self):
        """Indique si la carte est une lettre ou non.

         :rtype: boolean
        """
        return self.__name in ["A", "B", "C", "D"]

    def is_operator(self):
        """Indique si la carte est un opérateur.

         :rtype: boolean
        """
        return self.__name in ["AND", "OR", "THEN"]

    def is_open(self):
        """Indique si la carte est une parenthèse ouvrante.

         :rtype: boolean
        """
        return self.__name == "("

    def is_close(self):
        """Indique si la carte est une parenthèse fermante.

         :rtype: boolean
        """
        return self.__name == ")"

    def is_not(self):
        """Indique si la carte est un "NOT".

         :rtype: boolean
        """
        return self.__name == "NOT"

    def is_ergo(self):
        """Indique si la carte est "Ergo".

         :rtype: boolean
        """
        return self.__name == "Ergo"

    def is_fallacy(self):
        """Indique si la carte est "Fallacy".

         :rtype: boolean
        """
        return self.__name == "Fallacy"

    def is_justification(self):
        """Indique si la carte est "Justification".

         :rtype: boolean
        """
        return self.__name == "Justification"

    def is_tabula_rasa(self):
        """Indique si la carte est "Justification".

         :rtype: boolean
        """
        return self.__name == "TabulaRasa"

    def is_revolution(self):
        """Indique si la carte est "Revolution".

         :rtype: boolean
        """
        return self.__name == "Revolution"

    def is_wild(self):
        """Indique si la carte est un joker (WildVar, WildOp).

        :rtype: boolean
        """
        return self.name in ["WildVar", "WildOp"]

    def is_wildvar(self):
        """Indique si la carte est "WildVar".

        :rtype: boolean
        """
        return self.name == "WildVar"

    def is_wildop(self):
        """Indique si la carte est WildOp.

        :rtype: boolean
        """
        return self.name == "WildOp"

    def is_special(self):
        """Indique si la carte est spéciale (Ergo, Fallacy, Justification,
        TabulaRasa, Revolution, WildVar, WildOp).

        :rtype: boolean
        """
        return self.name in ["Ergo", "Fallacy", "Justification", "TabulaRasa",
                             "Revolution", "WildVar", "WildOp"]

    def turn_parenthesis(self):
        """Retourne la parenthèse, si c'en est une, ne fait rien sinon."""
        if self.__name == ")":
            self.__name = "("
        elif self.__name == "(":
            self.__name = ")"

    def __repr__(self):
        """:return: le nom de la carte.
        :rtype: string
        """
        return self.__name
