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
        :type name: str

        :return: Objet Card
        :rtype: Card
        """
        assert name in Cst.card_names()
        self.__name = name
        self.__joker = self.is_joker()

    def __repr__(self):
        """:return: le nom de la carte.
        :rtype: string
        """
        return self.__name

    def __eq__(self, other):
        """
        * Si other est une chaîne de caractères, indique si le nom de la carte
          est other.

        * Si other est une carte, indique si elle a le même nom que la carte.

        :param other: l'objet auquel comparer
        :type other: str ou Card

        :return : True si les noms sont égaux, False sinon
        :rtype : bool
        """
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, Card):
            return self.name == other.name
        raise TypeError("'=' not supported between instances of 'Card' "
                        "and '{}'".format(type(other)))

    def __hash__(self):
        """:return : hash(self)
        :rtype : int
        """
        return self.name.__hash__()

    @property
    def joker(self):
        """getter

        :return: indique si la carte est ou a été un joker (JokerVar, JokerOp).
        :rtype: bool
        """
        return self.__joker

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

         :rtype: bool
        """
        return self.__name in ["A", "B", "C", "D"]

    def is_operator(self):
        """Indique si la carte est un opérateur.

         :rtype: bool
        """
        return self.__name in ["AND", "OR", "THEN"]

    def is_open(self):
        """Indique si la carte est une parenthèse ouvrante.

         :rtype: bool
        """
        return self.__name == "("

    def is_close(self):
        """Indique si la carte est une parenthèse fermante.

         :rtype: bool
        """
        return self.__name == ")"

    def is_not(self):
        """Indique si la carte est un "NOT".

         :rtype: bool
        """
        return self.__name == "NOT"

    def is_qed(self):
        """Indique si la carte est "QED".

         :rtype: bool
        """
        return self.__name == "QED"

    def is_liar(self):
        """Indique si la carte est "Liar".

         :rtype: bool
        """
        return self.__name == "Liar"

    def is_truth(self):
        """Indique si la carte est "Truth".

         :rtype: bool
        """
        return self.__name == "Truth"

    def is_blank(self):
        """Indique si la carte est "Blank".

         :rtype: bool
        """
        return self.__name == "Blank"

    def is_exchange(self):
        """Indique si la carte est "Exchange".

         :rtype: bool
        """
        return self.__name == "Exchange"

    def is_joker(self):
        """Indique si la carte est un joker (JokerVar, JokerOp).

        :rtype: bool
        """
        return self.name in ["JokerVar", "JokerOp"]

    def is_jokervar(self):
        """Indique si la carte est "JokerVar".

        :rtype: bool
        """
        return self.name == "JokerVar"

    def is_jokerop(self):
        """Indique si la carte est JokerOp.

        :rtype: bool
        """
        return self.name == "JokerOp"

    def is_special(self):
        """Indique si la carte est spéciale (QED, Liar, Truth,
        Blank, Exchange, JokerVar, JokerOp).

        :rtype: bool
        """
        return self.name in ["QED", "Liar", "Truth", "Blank",
                             "Exchange", "JokerVar", "JokerOp"]

    def turn_parenthesis(self):
        """Retourne la parenthèse, si c'en est une, ne fait rien sinon."""
        if self.__name == ")":
            self.__name = "("
        elif self.__name == "(":
            self.__name = ")"
