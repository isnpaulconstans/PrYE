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

    def change(self, premise, index, card):
        """Change la carte dans la prémisse premise en position index pour
        mettre card à la place.

        :param premise: le numéro de la prémisse
        :type premise: int
        :param index: la position de la carte à changer dans la prémisse
        :type index: int
        :param card: la carte à mettre
        :type card: Card
        :return: la carte qu'il y avait avant modification.
        :rtype: card
        """
        self.__modif = True
        return self.premises[premise].change(index, card)

    def insert(self, premise, index, card, new=True):
        """Insère la carte card dans la prémisse premise en position index
        et actualise currently_added si recent=True.

        :param premise: le numéro de la prémisse
        :type premise: int
        :param index: la position à laquelle insérer la carte dans la prémisse
        :type index: int
        :param card: la carte à insérer
        :type card: Card
        :param recent: indique s'il s'agit de l'ajout d'une nouvelle carte ou
                       de l'annulation d'un Tabula Rasa
        :type recent: bool
        :return: si new : True si l'insertion est possible, False sinon.
                 si not new : le numéro de la prémisse modifiée.
        :rtype: boolean
        """
        if new and len(self.currently_added) >= 2:
            return False
        self.__modif = True
        if not new:
            for (premise1, index1, mod) in reversed(self.currently_added):
                if not mod:
                    premise, index = premise1, index1
                    self.currently_added.remove((premise, index, False))
                    break
            else:
                return False
        self.premises[premise].insert(index, card)
        if index >= len(self.premises[premise]):
            index = len(self.premises[premise])-1
        for i, (premise1, index1, mod) in enumerate(self.currently_added):
            if premise1 == premise and index1 >= index:
                index1 += 1
                self.currently_added[i] = (premise1, index1, mod)
        if not new:
            return premise
        self.currently_added.append((premise, index, True))
        return True

    def pop(self, premise, index, recent=True):
        """Enlève la carte en position index de la prémisse premise.
        Si recent=True, ne renvoie la carte que si elle vienne d'être ajoutée.

        :param premise: le numéro de la prémisse
        :type premise: int
        :param index: la position dans la prémisse de la carte à supprimer
        :type index: int
        :param recent: indique si on ne doit renvoyer que les cartes qui
                       viennent d'être jouées ou s'il s'agit d'un Tabula Rasa
        :type recent: bool
        :return: la carte en question ou None si on ne peut pas l'enlever.
        :rtype: Card ou NoneType"""
        present = (premise, index, True) in self.currently_added
        if (present and not recent) or (not present and recent) \
                                    or index >= len(self.premises[premise]):
            return None
        if recent:
            self.currently_added.remove((premise, index, True))
#        try:
#            self.currently_added.remove((premise, index, recent))
#        except ValueError:
#            if recent or index >= len(self.premises[premise]):
#                return None
        self.__modif = True
        for i, (premise1, index1, mod) in enumerate(self.currently_added):
            if premise1 == premise and index1 > index:
                index1 -= 1
                self.currently_added[i] = (premise1, index1, mod)
        if not recent:
            self.currently_added.append((premise, index, False))
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
