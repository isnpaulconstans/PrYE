#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""

from random import choice, sample
from Ordi import Ordi


class OrdiRandom(Ordi):
    """Implémentation de Ordi."""
    def joue(self):
        """Joue un coup au hasard parmi les coups possibles. Si aucun n'est
        possible, jette deux cartes au hasard.
        """
        self._coups.append(((-1,)*3, (-1,)*3))  # défausser deux cartes
        ((i_hand1, num_premise1, index_premise1),
         (i_hand2, num_premise2, index_premise2)) = choice(self._coups)
        if i_hand1 == -1:  # deux cartes à défausser
            i_hand1, i_hand2 = sample(range(len(self._hand)), 2)
        elif i_hand2 == -1:  # une seule carte à défausser
            choix = list(range(len(self._hand)))  # choix possibles de carte2
            choix.remove(i_hand1)
            i_hand2 = choice(choix)
        if i_hand1 < i_hand2:
            i_hand2 -= 1  # tirages successifs
        return ((i_hand1, num_premise1, index_premise1),
                (i_hand2, num_premise2, index_premise2))


if __name__ == "__main__":
    from cards import Proof, Deck
    deck = Deck()
    proof = Proof()
    hand = deck.draw(7)
    ordi = Ordi(proof, hand)
