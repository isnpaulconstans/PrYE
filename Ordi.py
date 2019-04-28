#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""

from Card import Card


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
        self.__parenthèses()  # modifie hand

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

    def __wild(self):
        """Renvoie une copie de la main dans laquelle chaque joker a été
        remplacé par une carte correspondant (lettre ou opérateur)."""
        new_hand = []
        for card in self._hand:
            if card.is_wild():
                card = Card("A" if card.is_wildvar() else "OR")
            new_hand.append(card)
        return new_hand

    def joue(self):
        """Renvoie les prochaines cartes à jouer."""
        raise NotImplementedError

    def coups_possibles(self):
        """Renvoie la liste des coups possibles sous la forme d'une liste de
        couples de triplets ((i_hand1, num_premise1, index1),
        (i_hand2, num_premise2, index2)) où

        - i_hand est l'indice dans la main de la carte à jouer
        - num_premise est le numéro de la prémisse où jouer la carte (-1 pour
          défausser)
        - index_premise est l'indice où insérer la carte dans la prémisse

        -1 signifie qu'on peut défausser une carte

        :return: une liste de couples de triplets
        :rtype: list
        """
        hand = self.__wild()
        coups = []
        for i_hand1, card1 in enumerate(hand):
            if card1.is_special() and not card1.is_tabula_rasa():
                continue
            for num_premise1, premise1 in enumerate(self._proof.premises):
                index_max1 = len(premise1)+1
                if card1.is_tabula_rasa():
                    index_max1 -= 1
                for index1 in range(index_max1):
                    if card1.is_tabula_rasa():
                        old_card1 = premise1.pop(index1)
                    else:
                        premise1.insert(index1, card1)
                    if premise1.npi is not None:
                        coups.append(((i_hand1, num_premise1, index1),
                                      (-1, -1, -1)))
                    for i_hand2 in range(i_hand1+1, len(hand)):
                        card2 = hand[i_hand2]
                        if card2.is_special() and not card2.is_tabula_rasa():
                            continue
                        for num_premise2, premise2 in enumerate(self._proof.premises):
                            index_max2 = len(premise2)+1
                            if card2.is_tabula_rasa():
                                index_max2 -= 1
                            for index2 in range(index_max2):
                                if card2.is_tabula_rasa():
                                    if index1 == index2:
                                        continue
                                    old_card2 = premise2.pop(index2)
                                else:
                                    premise2.insert(index2, card2)
                                if premise1.npi is not None \
                                   and premise2.npi is not None:
                                    coups.append(((i_hand1, num_premise1,
                                                  index1),
                                                  (i_hand2, num_premise2,
                                                  index2))
                                                 )
                                if card2.is_tabula_rasa():
                                    premise2.insert(index2, old_card2)
                                else:
                                    premise2.pop(index2)
                    if card1.is_tabula_rasa():
                        premise1.insert(index1, old_card1)
                    else:
                        premise1.pop(index1)
        return coups
