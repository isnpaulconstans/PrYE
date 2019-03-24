#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""constantes."""


class Constantes():
    """Différentes constantes concernant le jeu"""
    # cartes
    CARD_HEIGHT = 70 + 1
    CARD_WIDTH = 50 + 1
    IMAGE = {
        "THEN": "carteImp.gif",
        "A": "carteA.gif",
        "B": "carteB.gif",
        "C": "carteC.gif",
        "D": "carteD.gif",
        "AND": "carteEt.gif",
        "OR": "carteOu.gif",
        "NOT": "carteNeg.gif",
        "(": "carteOpenParenthesis.gif",
        ")": "carteCloseParenthesis.gif",
        "Ergo": "carteCQFD.gif",
        "Back": "carteDos.gif"
        }
    # Le nombre de cartes de chaque type
    NUMBER = {"A": 4, "B": 4, "C": 4, "D": 4,
              "AND": 4, "OR": 4, "THEN": 4,
              "NOT": 6, "(": 4, ")": 4,
              # "Fallacy": 3, "Justification": 3,
              # "TabulaRasa": 1, "Revolution": 1,
              # "WildVar": 1, "WildOp": 1,
              "Ergo": 3,
             }
    # fond
    LINE_WIDTH = 5
    CARPET_COLOR = "ivory"

    @classmethod
    def card_names(cls):
        """Renvoie les noms des cartes du paquet.

        :return: Le nom des cartes du paquet
        :rtype: dict_keys
        """
        return cls.NUMBER.keys()
