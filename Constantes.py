#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""constantes."""


class Constantes():
    """Différentes constantes concernant le jeu"""
    # cartes
    CARD_HEIGHT = 70 + 1
    CARD_WIDTH = 50 + 1
    # Le nombre de cartes de chaque type
    NUMBER = {"A": 4, "B": 4, "C": 4, "D": 4,
              "AND": 4, "OR": 4, "THEN": 4,
              "NOT": 6, "(": 4, ")": 4,
              "Liar": 3, "Truth": 3,
              "Blank": 1, "Exchange": 1,
              "JokerVar": 1,  "JokerOp": 1,
              "QED": 3,
             }
    # fond
    LINE_WIDTH = 5
    CARPET_COLOR = "ivory"

    @classmethod
    def card_names(cls):
        """:return: Le nom des cartes du paquet
        :rtype: list
        """
        return list(cls.NUMBER.keys())
