#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""


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

    def joue(self):
        """Renvoie la prochaine carte à jouer."""
        raise NotImplementedError

    def coups_possibles(self):
        """Renvoie la liste des coups possibles sous la forme d'une liste de
        sextuplets (index_hand1, num_premise1, index_premise1, index_hand2,
        num_premise2, index_premise2) où

        - index_hand est l'indice dans la main de la carte à jouer
        - num_premise est le numéro de la prémisse où jouer la carte
        - index_premise est l'indice où insérer la carte dans la prémisse

        :return: une liste de sextuplets
        :rtype: list
        """
        coups = []
        for index_hand1, card1 in enumerate(self._hand):
            for index_hand2 in range(index_hand1+1, len(self._hand)):
                card2 = self._hand[index_hand2]
                for num_premise1, premise1 in enumerate(self._proof.premises):
                    for num_premise2, premise2 in enumerate(self._proof.premises):
                        for index_premise1 in range(len(premise1)):
                            premise1.insert(index_premise1, card1)
                            for index_premise2 in range(len(premise2)):
                                premise2.insert(index_premise2, card2)
                                if premise1.npi is not None and premise2.npi is not None:
                                    coups.append((index_hand1, num_premise1,
                                                  index_premise1, index_hand2,
                                                  num_premise2, index_premise2))
                                premise2.pop(index_premise2)
                            premise1.pop(index_premise2)
        return coups

