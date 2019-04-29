#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liste de cartes"""


class CardList(list):
    """Liste de cartes, avec la Notation Polonaise Inversée associée.
    Si la liste ne correspond pas à une preuve syntaxiquement correcte,
    NPI vaut None."""
    def __init__(self, *args):
        """Constructeur de la classe.

        :param args: des arguments pour construire la liste

        :return: objet CardList initalisé avec les éléments passés par args
        :rtype: CardList"""
        super().__init__(*args)
        self.__modif = True  # modification depuis le dernier appel à npi
        self.__npi = None

    @property
    def modif(self):
        """Indique s'il y a eu une modification depuis le dernier appel à npi.

        :return: True s'il y a une une modification, False sinon.
        :rtype: bool
        """
        return self.__modif

    def change(self, index, card):
        """Change la carte en position index pour mettre card à la place.

        :param index: la position de la carte à changer dans la prémisse
        :type index: int
        :param card: la carte à mettre
        :type card: Card
        :return: la carte qu'il y avait avant modification.
        :rtype: Card
        """
        self.__modif = True
        old_card = self[index]
        self[index] = card
        return old_card

    def append(self, card):
        """Ajoute la carte card à la  fin de la liste.

         :param card: la carte à ajouter
         :type card: Card
        """
        super().append(card)
        self.__modif = True

    def insert(self, index, card):
        """Insère card à la position index.

         :param card: la carte à insérer
         :type card: Card
         :param index: la position à laquelle insérer la carte
         :type index: int
        """
        super().insert(index, card)
        self.__modif = True

    def pop(self, index=-1):
        """Supprime la carte en position index (par défaut la dernière)
        et la renvoie.

        :param index: la position de la carte à renvoyer
        :type index: int
        :return: la carte supprimée
        :rtype: Card
        """
        card = super().pop(index)
        self.__modif = True
        return card

    def is_syntactically_correct(self):
        """Indique si la liste de cartes est syntaxiquement correcte,
        sans s'occuper de la correspondance des parenthèses.

        :return: True si la liste est syntaxiquement correcte, False sinon
        :rtype: bool
        """
        if self == []:
            return True
        if len(self) == 1:
            return self[0].is_letter()
        if not (self[0].is_open() or self[0].is_letter() or self[0].is_not()):
            return False
        if self[-1].is_not() or self[-1].is_operator():
            return False
        for i_card in range(len(self)-1):
            card1, card2 = self[i_card], self[i_card+1]
            if (card1.is_letter() or card1.is_close()) and \
               (card2.is_letter() or card2.is_not() or card2.is_open()):
                return False
            if card1.is_operator() and \
               (card2.is_operator() or card2.is_close()):
                return False
            if card1.is_not() and \
               (card2.is_operator() or card2.is_close() or card2.is_not()):
                return False
            if card1.is_open() and (card2.is_operator() or card2.is_close()):
                return False
        return not card2.is_operator()

    @property
    def npi(self):
        """Met à jour self.npi en :

         * None si la syntaxe de la liste n'est pas correcte

         * une liste de carte correspondant à la notation polonaise inversée de
           la liste de départ sinon.
        """
        if not self.__modif:
            return self.__npi
        self.__modif = False
        if not self.is_syntactically_correct():
            self.__npi = None
            return self.__npi
        self.__npi = []
        stack = []
        for card in self:
            if card.is_letter():
                self.__npi.append(card)
                continue
            if card.is_open():
                stack.append(card)
                continue
            if card.is_close():
                while stack != [] and not stack[-1].is_open():
                    self.__npi.append(stack.pop())
                if stack == []:  # Pas de parenthèse ouvrante correspondante
                    self.__npi = None
                    return self.__npi
                else:  # On enlève la parenthèse ouvrante correspondante
                    stack.pop()
                continue
            while stack != [] and stack[-1].priority() >= card.priority():
                self.__npi.append(stack.pop())
            stack.append(card)
        while stack != []:
            card = stack.pop()
            if card.is_open():  # pas de parenthèse fermante correspondante
                self.__npi = None
                return self.__npi
            self.__npi.append(card)
        return self.__npi
