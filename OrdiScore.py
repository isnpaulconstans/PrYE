#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion du jeu de l'ordinateur.
"""

from random import random
from Ordi import Ordi
from DPLL import DPLL as Demo


class OrdiScore(Ordi):
    """Concrétisation de choix_coups avec un score pour chaque coup."""
    card_value = {"A": 1, "B": 1, "C": 1, "D": 1,
                  "AND": 1, "OR": 1, "THEN": 1,
                  "NOT": 1, "(": 2, ")": 2,
                  "Fallacy": 2, "Justification": 4,
                  "TabulaRasa": 4, "Revolution": 4,
                  "WildVar": 5, "WildOp": 5,
                  "QED": 5,
                 }
    coef_fallacy = 0.1
    coef_proof_self = 10.
    coef_proof_other = -5.
    coef_qed = 2.
    score_justification = 1.

    def sort_hand(self):
        """Tri la main par ordre décroissant de valeur. Si la main comporte
        plusieurs cartes QED, en garde une au début et déplace les autre à la
        fin (il n'y a aucun intéret à en garder plusieurs). Les cartes à jeter
        sont alors les dernières de la main.
        """
        self._hand.sort(key=lambda card: self.card_value[card.name],
                        reverse=True)
        nb_qed = self._hand.count("QED")
        for _ in range(nb_qed-1):
            i_qed = self._hand.index("QED")
            qed = self._hand.pop(i_qed)
            self._hand.append(qed)

    def choice_fallacy(self, num_other):
        """:para num_other: Le numéro du joueur sur lequel on a déjà joué une
                            carte fallacy, ou None s'il n'y en a pas
        :type num_other: int ou NoneType
        :return: le numéro du joueur sur lequel jouer fallacy et le score
                 correspondant.
        :rtype: tuple
        """
        others = list(range(4))
        others.remove(self._num_player)
        if num_other is not None:
            others.remove(num_other)
        point_max = -float('inf')
        for i_other in others:
            if self._fallacys[i_other] == 3:
                point = 0
            else:
                point = ((10+self._scores[i_other]) * (3-self._fallacys[i_other])
                         * self.coef_fallacy)
            if point > point_max or (point == point_max and random() > 0.5):
                point_max = point
                i_other_max = i_other
        return i_other_max, point_max

    def extend_coups(self, lst_coups):
        """Ajoute tous les choix possibles des cartes Revolution et Wild à la
        liste des coups.

        Pour les cartes Wild, index est transformé en un couple (index, name)
        où name est le nom à affecter à la wild card.

        :param lst_coups: la liste de coups initiale au format créé par
                          coups_possibles
        :type lst_coups: list

        :return: La liste de coups mise à jour
        :rtype: list
        """
        def is_to_extend(i_hand):
            """:return: True si la carte d'indice i_hand de la main nécessite
            une extension.
            :rtype: bool

            :param i_hand: l'indice de la carte dans la main, ou -1 si c'est
                           une carte à jeter
            :type i_hand: int
            """

            if i_hand == -1:
                return False
            card = self._hand[i_hand]
            return card.is_revolution() or card.is_wild()

        # tri des coups à étendre ou pas
        new_lst_coups = []
        to_extend_lst = []
        for coup in lst_coups:
            to_extend = False
            for i_coup in range(2):
                (i_hand, num_premise, index_premise) = coup[i_coup]
                if is_to_extend(i_hand):
                    to_extend = True
            if to_extend:
                to_extend_lst.append(coup[:])
            else:
                new_lst_coups.append(coup[:])
        # extension des coups le nécessitant
        for i_coup in range(2):
            lst_coups = to_extend_lst
            to_extend_lst = []
            for coup in lst_coups:
                (i_hand, num_premise, index_premise) = coup[i_coup]
                if not is_to_extend(i_hand):
                    to_extend_lst.append(coup[:])
                    continue
                card = self._hand[i_hand]
                if card.is_revolution():
                    for num, index in zip(num_premise, index_premise):
                        new_coup = coup[:]
                        new_coup[i_coup] = (i_hand, num, index)
                        to_extend_lst.append(new_coup)
                elif card.is_wild():
                    name_lst = ("OR", "AND", "THEN") if card.is_wildop()\
                                                     else "ABCD"
                    for name in name_lst:
                        new_coup = coup[:]
                        new_coup[i_coup] = (i_hand, num_premise,
                                            (index_premise, name))
                        to_extend_lst.append(new_coup)
        new_lst_coups.extend(to_extend_lst)
        return new_lst_coups

    def calc_score(self):
        """:return: le score obtenu avec le coup actuellement joué
        :rtype: int
        """
        demo = Demo(self._proof)
        provens = demo.conclusion()
        if provens is None:
            return 0.
        score_proof = self._proof.score()
        score = 0.
        for index, proven in enumerate(provens):
            coef = self.coef_proof_self if index == self._num_player\
                                        else self.coef_proof_other
            if not proven:
                coef = - coef
            score += coef * score_proof
        return score

    def choix_coups(self):
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
        self.sort_hand()
        lst_coups = self.coups_possibles()
        lst_coups = self.extend_coups(lst_coups)
        score_max = -float('inf')
        for coup in lst_coups:
            score = 0.
            poped_cards = []  # cartes effacées avec tabula_rasa
            qed = False  # indique si QED a été joué
            for i_coup, (i_hand, num_premise, index_premise) in enumerate(coup):
                # cartes hors prémisses
                if i_hand == -1:
                    i_drop = len(self._hand)-1  # prochaine carte à jeter
                    if coup[1-i_coup][0] == i_drop:  # si la carte à jeter est
                        i_drop -= 1                   # l'autre carte jouée
                    coup[i_coup] = (i_drop, num_premise, index_premise)
                    card = self._hand[i_drop]
                    score -= self.card_value[card]
                    continue
                card = self._hand[i_hand]
                if card.is_justification():
                    score += self.score_justification
                    continue
                score -= self.card_value[card]
                if card.is_fallacy():
                    other_card = self._hand[coup[1-i_coup][0]]
                    num_other = coup[1-i_coup][1] if other_card.is_fallacy()\
                                                  else None
                    num_premise, point = self.choice_fallacy(num_other)
                    coup[i_coup] = (i_hand, num_premise, index_premise)
                    score += point
                    continue
                if card.is_qed():
                    qed = True
                    break
                # modification de _proof
                if card.is_tabula_rasa():
                    poped_cards.append(self._proof.pop(num_premise,
                                                       index_premise,
                                                       recent=False))
                    continue
                if card.is_revolution():
                    row1, row2 = num_premise
                    col1, col2 = index_premise
                    card1 = self._proof.premises[row1][col1]
                    card2 = self._proof.premises[row2][col2]
                    self._proof.change(row1, col1, card2)
                    self._proof.change(row2, col2, card1)
                    continue
                if card.is_wild():
                    index_premise, name = index_premise
                    card.name = name
                self._proof.insert(num_premise, index_premise, card)
            # calcul du score obtenu
            coef = self.coef_qed if qed else 1
            score += coef * self.calc_score()
            if score > score_max or (score == score_max and random() > 0.5):
                # XXX testes du score
#                [(i_hand1, num_premise1, index_premise1),
#                 (i_hand2, num_premise2, index_premise2)] = coup
#                card1 = self._hand[i_hand1]
#                card2 = self._hand[i_hand2]
#                print("Score : {}".format(score), end=' : ')
#                print("{} ligne {} col {}".format(card1,
#                                                  num_premise1,
#                                                  index_premise1), end=' ')
#                print("{} ligne {} col {}".format(card2,
#                                                  num_premise2,
#                                                  index_premise2))
                score_max = score
                coup_max = coup
            #restauration de self._proof
            coup = reversed(coup)
            for i_coup, (i_hand, num_premise, index_premise) in enumerate(coup):
                if num_premise == -1:
                    continue
                card = self._hand[i_hand]
                if card.is_justification() or card.is_fallacy() or card.is_qed():
                    continue
                if card.is_tabula_rasa():
                    card = poped_cards.pop()
                    self._proof.insert(None, None, card, new=False)
                    continue
                if card.is_revolution():
                    row1, row2 = num_premise
                    col1, col2 = index_premise
                    card1 = self._proof.premises[row1][col1]
                    card2 = self._proof.premises[row2][col2]
                    self._proof.change(row1, col1, card2)
                    self._proof.change(row2, col2, card1)
                    continue
                if card.wild:
                    card.name = "WildVar" if card.is_letter() else "WildOp"
                    index_premise = index_premise[0]
                self._proof.pop(num_premise, index_premise)
        coup = coup_max
        # gestion des wild cards
        for i_coup, (i_hand, num_premise, index_premise) in enumerate(coup):
            card = self._hand[i_hand]
            if not card.is_wild():
                continue
            index_premise, name = index_premise
            card.name = name
            coup[i_coup] = (i_hand, num_premise, index_premise)
        [(i_hand1, num_premise1, index_premise1),
         (i_hand2, num_premise2, index_premise2)] = coup
        if i_hand1 < i_hand2:
            i_hand2 -= 1  # i_hand2 -= 1 en cas de tirages successifs
        return ((i_hand1, num_premise1, index_premise1),
                (i_hand2, num_premise2, index_premise2))
