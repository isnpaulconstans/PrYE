#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""

from Ordi import Ordi


class OrdiScore(Ordi):
    """Concrétisation de choix_coups avec un score pour chaque coup."""
    card_value = {"A": 1, "B": 1, "C": 1, "D": 1,
                  "AND": 1, "OR": 1, "THEN": 1,
                  "NOT": 1, "(": 1, ")": 1,
                  "Fallacy": 2, "Justification": 4,
                  "TabulaRasa": 4, "Revolution": 4,
                  "WildVar": 5, "WildOp": 5,
                  "Ergo": 5,
                 }

    def sort_hand(self):
        """Tri la main par ordre décroissant de valeur. Si la main comporte
        plusieurs cartes Ergo, en garde une au début et déplace les autre à la
        fin (il n'y a aucun intéret à en garder plusieurs). Les cartes à jeter
        sont alors les dernières de la main.
        """
        self._hand.sort(key=lambda card: self.card_value[card.name],
                        reverse=True)
        nb_ergo = self._hand.count("Ergo")
        for _ in range(nb_ergo-1):
            i_ergo = self._hand.index("Ergo")
            ergo = self._hand.pop(i_ergo)
            self._hand.append(ergo)

    def choice_fallacy(self, num_player, scores, fallacy):
        """
        :return : le joueur sur lequel joueur la carte fallacy
        :rtype : int

        :param num_player: Le numéro du joueur
        :type num_player: int

        :param scores: Les scores des joueurs
        :type scores: list

        :param fallacy: Les nombres de tours de "fallacy" pour chaque joueur
        :type fallacy: list
        """
        others = list(range(4))
        others.remove(num_player)

    def choix_coups(self, num_player, scores, fallacy):
        """Choisi un coup parmi l'ensemble des coups possibles.

        * Si la carte à jouer est Fallacy, num_premise indique le numéro
          du joueur sur lequelle elle doit être jouée.

        * Si la carte est Révolution, num_premise et index sont les
          couples de numéros de prémisses et d'indice des cartes à
          échanger.

        * Dans le cas d'une carte Wild, self._hand est modifié.

        :param num_player: Le numéro du joueur
        :type num_player: int

        :param scores: Les scores des joueurs
        :type scores: list

        :param fallacy: Les nombres de tours de "fallacy" pour chaque joueur
        :type fallacy: list

        :return: Un couple de triplets ((i_hand1, num_premise1, index1),
                 (i_hand2, num_premise2, index2))
        :rtype: tuple
        """
        self.sort_hand()
        score_max = -float('inf')
        for coup in self._coups:
            score = 0
            i_drop = -1  # indice de la prochaine carte à jeter
            for i_coup, (i_hand, num_premise, index_premise) in enumerate(coup):
                if i_hand == -1:
                    card = self._hand[i_drop]
                    i_drop -= 1
                    score -= self.card_value[card]
                    continue
                card = self._hand[i_hand]
                if card.is_fallacy():
                    coup[i_coup][1] = self.choice_fallacy(num_player, scores,
                                                          fallacy)
                if card.is_revolution():
                    i = randrange(len(num_premise))
                    coup[i_coup][1] = num_premise[i]
                    coup[i_coup][1] = index_premise[i]
                if card.is_wild() and num_premise != -1:
                    choices = ("OR", "AND", "THEN") if card.is_wildop() else "ABCD"
                    card.name = choice(choices)
                # Ajouter la carte à self._proof
            # calculer le score obtenu
            if score > score_max:
                score_max = score
                coup_max = coup
        coup = coup_max
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
