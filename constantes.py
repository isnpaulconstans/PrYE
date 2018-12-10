#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Créé par Nicolas, le 24/11/2018 en Python 3.2

constantes du jeu."""

CARD_HEIGHT = 140
CARD_WIDTH = 100
HEIGHT = 5 * CARD_HEIGHT + 10
WIDTH = 1000

CARPET_COLOR = "ivory"

# images cartes
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
    "CQFD" : "carteCQFD.gif"
    }

PRIORITY = {
    "AND": 1,
    "OR": 2,
    "THEN": 3,
    "NOT": 4,
    "(": 0,  # PARENTHESE
    ")": 0,  # PARENTHESE
    }
