#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des prémisses et la preuve."""

from Card import Card
from CardList import CardList


class Proof():
    """Classe gérant les prémisses et la preuve."""
    def __init__(self):
        """Initialisation des attributs :

        * premises : liste de 4 CardList correspondant aux 4 lignes de
          prémisses;

        * currently_added : liste de cartes venant d'être ajoutées aux
          prémisses, et pas encore validées.

        :return: un objet Proof
        :rtype: Proof
        """
        self.premises = [CardList() for _ in range(4)]
        self.currently_added = []
        self.__modif = True  # modification depuis le dernier appel à npi
        self.__npi = []

    @property
    def modif(self):
        """Indique s'il y a eu une modification depuis le dernier appel à npi.

        :return: True s'il y a une une modification, False sinon.
        :rtype: bool
        """
        return self.__modif

    @property
    def npi(self):
        """Renvoie la preuve complète en notation polonaise inversée

        :return: npi
        :rtype: list
        """
        if not self.modif:
            return self.__npi
        self.__modif = False
        nb_premises = 0
        self.__npi = []
        for premise in self.premises:
            assert premise.npi is not None
            if premise.npi != []:
                nb_premises += 1
            self.__npi.extend(premise.npi)
        self.__npi.extend([Card("AND") for _ in range(nb_premises-1)])
        return self.__npi

    def insert(self, premise, index, card):
        """Insère la carte card dans la prémisse premise en position index
        et actualise currently_added.

        :param premise: le numéro de la prémisse
        :type premise: int
        :param index: la position à laquelle insérer la carte dans la prémisse
        :type index: int
        :param card: la carte à insérer
        :type card: Card
        :return: True si l'insertion est possible, False sinon.
        :rtype: boolean
        """
        if len(self.currently_added) >= 2:
            return False
        self.__modif = True
        self.premises[premise].insert(index, card)
        if index >= len(self.premises[premise]):
            index = len(self.premises[premise])-1
        if self.currently_added != []:
            (premise1, index1) = self.currently_added.pop()
            if premise1 == premise and index1 >= index:
                index1 += 1
            self.currently_added.append((premise1, index1))
        self.currently_added.append((premise, index))
        return True

    def pop(self, premise, index, recent=True):
        """Enlève la carte en position index de la prémisse premise.
        Si recent=True, ne renvoie la carte que si elle vienne d'être ajoutée.

        :param premise: le numéro de la prémisse
        :type premise: int
        :param index: la position dans la prémisse de la carte à supprimer
        :type index: int
        :param recent: indique si on ne doit renvoyer que les cartes qui
                       viennent d'être jouées
        :type recent: bool
        :return: la carte en question ou None si on ne peut pas l'enlever.
        :rtype: Card ou NoneType"""
        try:
            self.currently_added.remove((premise, index))
        except ValueError:
            if recent or index >= len(self.premises[premise]):
                return None
        self.__modif = True
        if self.currently_added != []:
            (premise1, index1) = self.currently_added.pop()
            if premise1 == premise and index1 >= index:
                index1 -= 1
            self.currently_added.append((premise1, index1))
        return self.premises[premise].pop(index)

    def reset_added(self):
        """Remise à zéro de currently_added pour le prochain tour."""
        self.currently_added = []

    def is_all_correct(self):
        """Indique si toutes les prémisses sont correctes ou pas.

        :rtype: boolean"""
        for premise in self.premises:
            if premise.npi is None:
                return False
        return True

    def all_cards_played(self):
        """Indique si chacune des 4 cartes A, B, C et D a été jouée, et donc
        s'il est possible de jouer la carte Ergo.

        :rtype: boolean
        """
        played = [False]*4
        for premise in self.premises:
            for card in premise:
                if card.is_letter():
                    played[ord(card.name)-ord('A')] = True
        return played == [True] * 4

    def score(self):
        """Renvvoie le score associé à la preuve.

        :return: Le score correspondant à la preuve, c'est à dire le nombre de
                 cartes qui la compose.
        :rtype: int
        """
        return sum([len(premise) for premise in self.premises])
