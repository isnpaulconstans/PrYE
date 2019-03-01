#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""

from random import choice, sample


class Ordi:
    """Classe abstraite gérant le jeu de l'odinateur"""
    def __init__(self, proof, hand):
        """Constructeur de la classe.

        :param proof: Une preuve
        :type proof: Proof

        :param hand: La main du joueur
        :type hand: list of Cards

        :return: objet Ordi
        :rtype: Ordi"""
        self._proof = proof
        self._hand = hand
        self.__parenthèses()
        self._hand = self._hand[:]
        self._coups = self.coups_possibles()

    def __parenthèses(self):
        """Modifie la main pour avoir si possible au moins une parenthèse
        ouvrante et une fermante."""
        i_parenthesis = []  # indices des parenthèses
        for i_card, card in enumerate(self._hand):
            if card.is_open() or card.is_close():
                i_parenthesis.append(i_card)
        if len(i_parenthesis) < 2:
            return
        i1, i2 = i_parenthesis[:2]
        if self._hand[i1].name == self._hand[i2].name:
            self._hand[i2].turn_parenthesis()

    def joue(self):
        """Renvoie la prochaine carte à jouer."""
        raise NotImplementedError

    def coups_possibles(self):
        """Renvoie la liste des coups possibles sous la forme d'une liste de
        sextuplets (index_hand1, num_premise1, index_premise1, index_hand2,
        num_premise2, index_premise2) où

        - index_hand est l'indice dans la main de la carte à jouer
        - num_premise est le numéro de la prémisse où jouer la carte (-1 pour
          défausser)
        - index_premise est l'indice où insérer la carte dans la prémisse

        -1 signifie qu'on peut défausser une carte

        :return: une liste de sextuplets
        :rtype: list
        """
        coups = []
        for index_hand1, card1 in enumerate(self._hand):
            if card1.is_special():
                continue
            for num_premise1, premise1 in enumerate(self._proof.premises):
                for index_premise1 in range(len(premise1)+1):
                    premise1.insert(index_premise1, card1)
                    if premise1.npi is not None:
                        coups.append((index_hand1, num_premise1, index_premise1,
                                      -1, -1, -1))
                    for index_hand2 in range(index_hand1+1, len(self._hand)):
                        card2 = self._hand[index_hand2]
                        if card2.is_special():
                            continue
                        for num_premise2, premise2 in enumerate(self._proof.premises):
                            for index_premise2 in range(len(premise2)+1):
                                premise2.insert(index_premise2, card2)
#                                print(proof.premises, end='->')
                                if premise1.npi is not None and premise2.npi is not None:
#                                    print('OK')
                                    coups.append((index_hand1, num_premise1,
                                                  index_premise1, index_hand2,
                                                  num_premise2, index_premise2))
#                                else:
#                                    print('FAUX')
                                premise2.pop(index_premise2)
                    premise1.pop(index_premise1)
        return coups


class OrdiRandom(Ordi):
    def joue(self):
        """Joue un coup au hasard parmi les coups possibles. Si aucun n'est
        possible, jette deux cartes au hasard."""
        self._coups.append((-1,)*6)  # défausser deux cartes
        (index_hand1, num_premise1,
         index_premise1, index_hand2,
         num_premise2, index_premise2) = choice(self._coups)
        if index_hand1 == -1:
            index_hand1, index_hand2 = sample(range(len(self._hand)), 2)
        elif index_hand2 == -1:
            index_hand2 = choice(range(len(self._hand)))
        return (index_hand1, num_premise1, index_premise1, index_hand2,
                num_premise2, index_premise2)


if __name__ == "__main__":
    from cards import Proof, Deck
    deck = Deck()
    proof = Proof()
    hand = deck.draw(7)
    ordi = Ordi(proof, hand)
