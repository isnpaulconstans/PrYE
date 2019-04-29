#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""

from Card import Card


class Ordi:
    """Classe abstraite gérant le jeu de l'odinateur"""
    def __init__(self, proof, hand, fallacy):
        """Constructeur de la classe.

        :param proof: Une preuve
        :type proof: Proof

        :param hand: La main du joueur
        :type hand: list of Cards

        :param fallacy: Indique si le joueur subit une fallacy
        :type fallacy: bool

        :return: objet Ordi
        :rtype: Ordi"""
        self._proof = proof
        self._hand = hand
        self._fallacy = fallacy
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
        """:return: une copie de la main dans laquelle chaque joker a été
        remplacé par une carte correspondant (lettre ou opérateur).

        :rtype: list"""
        new_hand = []
        for card in self._hand:
            if card.is_wild():
                card = Card("A" if card.is_wildvar() else "OR")
            new_hand.append(card)
        return new_hand

    def __revolution(self):
        """Renvoie la liste des couples de cartes échangeables dans la preuve.

        :return: lst_num_premise et lst_index : des listes de couples donnant
        des numéros de prémisse et des indices de cartes échangeables.
        Par exemple, si num_premise[0]=[np0, np1] et index[0]=[i0, i1] alors on
        peut échanger la carte d'indice i0 de la prémisse np0 avec la carte d'
        indice i1 de la prémisse np1.
        :rtype: tuple
        """
        def index_flat2premise_index(index):
            """:return: le couple (num_premise, index) correspondant à
            index_flat.
            :rtype: tuple"""
            num_premise = 0
            len_premise = len(self._proof.premises[0])
            while index >= len_premise:
                index -= len_premise
                num_premise += 1
                len_premise = len(self._proof.premises[num_premise])
            return (num_premise, index)

        proof_flat = []
        for i in range(4):
            proof_flat += self._proof.premises[i]
        len_flat = len(proof_flat)
        lst_num_premise, lst_index = [], []
        for index_flat1 in range(len_flat-1):
            np1, i1 = index_flat2premise_index(index_flat1)
            card1 = self._proof.premises[np1][i1]
            if not (card1.is_letter() or card1.is_operator()):
                continue
            for index_flat2 in range(index_flat1+1, len_flat):
                np2, i2 = index_flat2premise_index(index_flat2)
                card2 = self._proof.premises[np2][i2]
                if (card1.is_letter() and not card2.is_letter()) or\
                   (card1.is_operator() and not card2.is_operator()) or\
                   card1.name == card2.name:
                    continue
                lst_num_premise.append((np1, np2))
                lst_index.append((i1, i2))
        return lst_num_premise, lst_index

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

        Si la carte à jouer est revolution, alors num_premise et index
        deviennent des listes de couples donnant des numéros de
        prémisse et des indices de cartes échangeables.
        Par exemple, si num_premise[0]=[np0, np1] et index[0]=[i0, i1] alors on
        peut échanger la carte d'indice i0 de la prémisse np0 avec la carte d'
        indice i1 de la prémisse np1.

        i_hand = -1 signifie qu'on peut défausser une carte

        :return: une liste de couples de triplets
        :rtype: list
        """
        hand = self.__wild()
        coups = []
        for i_hand1, card1 in enumerate(hand):
            special1 = False  # indique si carte1 est jouée hors prémisses
            if card1.is_ergo():
                if self._proof.all_cards_played() and not self._fallacy:
                    coups.append(((i_hand1, 0, 0), (-1, -1, -1)))
                continue
            if card1.is_revolution():
                np1, i1 = self.__revolution()
                if np1 == []:
                    continue
                coups.append(((i_hand1, np1, i1),
                              (-1, -1, -1)))
                special1 = True
            if card1.is_fallacy():
                np1, i1 = 0, 0
                coups.append(((i_hand1, np1, i1), (-1, -1, -1)))
                special1 = True
            if card1.is_justification() and self._fallacy:
                np1, i1 = 0, 0
                coups.append(((i_hand1, np1, i1), (-1, -1, -1)))
                fallacy_cur = False
                special1 = True
            else:
                fallacy_cur = self._fallacy


#            if card1.is_fallacy() or card1.is_justification():
#                continue
            for num_premise1, premise1 in enumerate(self._proof.premises):
                index_max1 = len(premise1)+1
                if card1.is_tabula_rasa():
                    index_max1 -= 1
                elif special1:
                    index_max1 = 1
                for index1 in range(index_max1):
                    if special1:
                        num_premise1, index1 = np1, i1
                    else:
                        if card1.is_tabula_rasa():
                            old_card1 = premise1.pop(index1)
                        else:
                            premise1.insert(index1, card1)
                        if premise1.npi is not None:
                            coups.append(((i_hand1, num_premise1, index1),
                                          (-1, -1, -1)))
                    for i_hand2 in range(i_hand1+1, len(hand)):
                        card2 = hand[i_hand2]
                        if card2.is_ergo():
                            if self._proof.all_cards_played()\
                                           and premise1.npi is not None:
                                coups.append(((i_hand1, num_premise1, index1),
                                              (i_hand2, 0, 0)))
                            continue
                        if card2.is_revolution() and premise1.npi is not None:
                            lst_num_premise, lst_index = self.__revolution()
                            if lst_num_premise:
                                coups.append(((i_hand1, num_premise1, index1),
                                              (i_hand2, lst_num_premise, lst_index)))
                            continue
                        if card2.is_fallacy() or card2.is_justification()\
                                              or card2.is_revolution():
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
                                    coups.append(((i_hand1, num_premise1, index1),
                                                  (i_hand2, num_premise2, index2)))
                                if card2.is_tabula_rasa():
                                    premise2.insert(index2, old_card2)
                                else:
                                    premise2.pop(index2)
                    if card1.is_tabula_rasa():
                        premise1.insert(index1, old_card1)
                    elif not special1:
                        premise1.pop(index1)
        return coups
