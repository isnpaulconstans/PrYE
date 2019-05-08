#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""

from Ordi import Ordi


class OrdiRandom(Ordi):
    """Concrétisation de choix_coups avec un score pour chaque coup."""
    card_value = {"A": 1, "B": 1, "C": 1, "D": 1,
                       "AND": 1, "OR": 1, "THEN": 1,
                       "NOT": 1, "(": 1, ")": 1,
                       "Fallacy": 2, "Justification": 4,
                       "TabulaRasa": 4, "Revolution": 4,
                       "WildVar": 5,  "WildOp": 5,
                       "Ergo": 5,
                      }

    def drop_choice(self, other):
        """Renvoie la carte de la main de score mini"""
        #  TODO à écrire !
        pass

    def choix_coups(self, num_player):
        """Choisi un coup parmi l'ensemble des coups possibles.

        * Si la carte à jouer est Fallacy, num_premise indique le numéro
          du joueur sur lequelle elle doit être jouée.

        * Si la carte est Révolution, num_premise et index sont les
          couples de numéros de prémisses et d'indice des cartes à
          échanger.

        * Dans le cas d'une carte Wild, self._hand est modifié.

        :return: Un couple de triplets ((i_hand1, num_premise1, index1),
                 (i_hand2, num_premise2, index2))

        :rtype: tuple
        """
        score_max = -float('inf')
        for ((i_hand1, num_premise1, index_premise1),
             (i_hand2, num_premise2, index_premise2)) in self._coups:
            if i_hand1 == i_hand2 == -1:
                for i1, card1 in enumerate(self._hand):
                    value1 = self.card_value[card1.name]
                    for i2 in range(i1+1, len(self._hand)):
                        card2 = self._hand[i2]
                        value2 = self.card_value[card2.name]
                        score = value1 + value2
                        if card1.is_ergo() and card2.is_ergo():
                            # TODO inutile de garder plusieurs ergo
                            pass
                        if score <= score_max:
                            continue
                        score_max = score
                        i_hand1, i_hand2 = i1, i2
            elif i_hand1 == -1 or i_hand2 == -1:
                if i_hand1 == -1:
                    (i_hand1, num_premise1, index_premise1) = (i_hand2,
                                                               num_premise2,
                                                               index_premise2)
                choix = list(range(len(self._hand)))  # choix possibles de carte2
                choix.remove(i_hand1)
                i_hand2 = choice(choix)
            coup = ([i_hand1, num_premise1, index_premise1],
                    [i_hand2, num_premise2, index_premise2])
            for i_coup, (i_hand, num_premise, index_premise) in enumerate(coup):
                card = self._hand[i_hand]
                if card.is_fallacy():
                    others = list(range(4))
                    others.remove(num_player)
                    coup[i_coup][1] = choice(others)
                if card.is_revolution():
                    i = randrange(len(num_premise))
                    coup[i_coup][1] = num_premise[i]
                    coup[i_coup][1] = index_premise[i]
                if card.is_wild() and num_premise != -1:
                    choices = ("OR", "AND", "THEN") if card.is_wildop() else "ABCD"
                    card.name = choice(choices)
        if i_hand1 < i_hand2:
            coup[1][0] -= 1  # i_hand2 -= 1 en cas de tirages successifs
        return coup


if __name__ == "__main__":
    from Proof import Proof
    from Deck import Deck
    deck = Deck()
    proof = Proof()
    hand = deck.draw(7)
    ordi = Ordi(proof, hand)
