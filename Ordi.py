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
        self.__parenthèses()  # modifie hand
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
        """Renvoie les prochaines cartes à jouer."""
        raise NotImplementedError

    def coups_possibles(self):
        """Renvoie la liste des coups possibles sous la forme d'une liste de
        couples de triplets ((i_hand1, num_premise1, index_premise1),
        (i_hand2, num_premise2, index_premise2)) où

        - i_hand est l'indice dans la main de la carte à jouer
        - num_premise est le numéro de la prémisse où jouer la carte (-1 pour
          défausser)
        - index_premise est l'indice où insérer la carte dans la prémisse

        -1 signifie qu'on peut défausser une carte

        :return: une liste de couples de triplets
        :rtype: list
        """
        coups = []
        for i_hand1, card1 in enumerate(self._hand):
            if card1.is_special():
                continue
            for num_premise1, premise1 in enumerate(self._proof.premises):
                for index_premise1 in range(len(premise1)+1):
                    premise1.insert(index_premise1, card1)
                    if premise1.npi is not None:
                        coups.append(((i_hand1, num_premise1, index_premise1),
                                      (-1, -1, -1)))
                    for i_hand2 in range(i_hand1+1, len(self._hand)):
                        card2 = self._hand[i_hand2]
                        if card2.is_special():
                            continue
                        for num_premise2, premise2 in enumerate(self._proof.premises):
                            for index_premise2 in range(len(premise2)+1):
                                premise2.insert(index_premise2, card2)
                                if premise1.npi is not None \
                                   and premise2.npi is not None:
                                    coups.append(((i_hand1, num_premise1,
                                                  index_premise1),
                                                  (i_hand2, num_premise2,
                                                  index_premise2))
                                                 )
                                premise2.pop(index_premise2)
                    premise1.pop(index_premise1)
        return coups
