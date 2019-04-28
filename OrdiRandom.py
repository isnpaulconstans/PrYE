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

        :return: Le coup joué et le liste des cartes spéciales jouées à traiter
        :rtype: (str, list)
        """
        self._coups.append(((-1,)*3, (-1,)*3))  # défausser deux cartes
        ((i_hand1, num_premise1, index_premise1),
         (i_hand2, num_premise2, index_premise2)) = choice(self._coups)
        if i_hand1 == i_hand2 == -1:
            i_hand1, i_hand2 = sample(range(len(self._hand)), 2)
        elif i_hand1 == -1 or i_hand2 == -1:
            if i_hand1 == -1:
                (i_hand1, num_premise1, index_premise1) = (i_hand2,
                                                           num_premise2,
                                                           index_premise2)
            choix = list(range(len(self._hand)))  # choix possibles de carte2
            choix.remove(i_hand1)
            i_hand2 = choice(choix)
        if i_hand1 < i_hand2:
            i_hand2 -= 1  # tirages successifs
        coup = ((i_hand1, num_premise1, index_premise1),
                (i_hand2, num_premise2, index_premise2))
        play = "Joue {} sur la ligne {} en position {}\n"
        drop = "Jette le {}\n"
        tabula = "Efface le {} de la ligne{} en position {}\n"
        msg = ""
        special_cards = []
        for (i_hand, num_premise, index_premise) in coup:
            card = self._hand.pop(i_hand)
            if card.is_ergo() and num_premise != -1:
                msg += "Joue une carte Ergo\n"
                special_cards.append("Ergo")
                break
            if index_premise == -1:
                msg += drop.format(card)
                continue
            if card.is_tabula_rasa():
                old_card = self._proof.pop(num_premise, index_premise,
                                           recent=False)
                msg += tabula.format(old_card, num_premise, index_premise)
                continue
            if card.is_wild():
                choices = ("OR", "AND", "THEN") if card.is_wildop() else "ABCD"
                card.name = choice(choices)
            self._proof.insert(num_premise, index_premise, card)
            msg += play.format(card, num_premise, index_premise)
        return msg, special_cards


if __name__ == "__main__":
    from Proof import Proof
    from Deck import Deck
    deck = Deck()
    proof = Proof()
    hand = deck.draw(7)
    ordi = Ordi(proof, hand)
