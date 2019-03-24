#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des démonstrations"""

from Card import Card


class FCN:
    """Mise en Forme Conjonctive Normale."""
    def __init__(self, proof):
        """Constructeur de la classe.

        :param proof: Une preuve
        :type proof: Proof

        :return: objet FCN
        :rtype: FCN"""
        self._proof = proof
        self.__fcn_npi = []
        self.__clause_list = self.__to_clause_list()

    @property
    def clause_list(self):
        """Renvoie la preuve sous forme d'une liste de clauses.

        :return: fcn_lst
        :rtype: list
        """
        if not self._proof.modif:
            return self.__clause_list
        return self.__to_clause_list()

    def __get_proposition(self):
        """renvoie la derniere proposition de fcn en npi.

        :return: proposition
        :rtype: list
        """
        pile = []
        nb_exp = 1  # on doit dépiler une proposition
        while nb_exp != 0:
            pile.append(self.__fcn_npi.pop())
            if pile[-1].is_letter():
                nb_exp -= 1
            elif pile[-1].is_operator():
                nb_exp += 1
        pile.reverse()
        return pile

    def __insert_not(self):
        """Insère un NOT avant la dernière proposition de fcn."""
        proposition = self.__get_proposition()
        self.__fcn_npi.append(Card("NOT"))
        self.__fcn_npi.extend(proposition)

    def __elim_then(self):
        """Génère self.__fcn_npi à partir de self._proof.npi
        en ramplaçant A -> B par non A ou B
        """
        self.__fcn_npi = []
        for card in self._proof.npi:
            if card.name != "THEN":
                self.__fcn_npi.append(card)
                continue
            self.__insert_not()
            self.__fcn_npi.append(Card("OR"))

    def __morgan(self):
        """Élimine les NON ET et NON OU de fcn en utilisant les lois de Morgan.
        """
        old_fcn = self.__fcn_npi[:]
        self.__fcn_npi = []
        modif = False
        for card in old_fcn:
            if not card.is_not():
                self.__fcn_npi.append(card)
                continue
            if not self.__fcn_npi[-1].is_operator():
                self.__fcn_npi.append(card)
                continue
            modif = True  # NON ET ou NON OU
            operator = self.__fcn_npi.pop()
            operator_name = "OR" if operator.name == "AND" else "AND"
            self.__insert_not()
            self.__fcn_npi.append(Card("NOT"))
            self.__fcn_npi.append(Card(operator_name))
        if modif:
            self.__morgan()

    def __elim_not(self):
        """Élimine les doubles négations de fcn."""
        old_fcn = self.__fcn_npi[:]
        self.__fcn_npi = []
        for card in old_fcn:
            if not (card.is_not() and self.__fcn_npi[-1].is_not()):
                self.__fcn_npi.append(card)
                continue
            self.__fcn_npi.pop()

    def __develop(self):
        """Développe les expressions :

        "B C ET A OU" ou "A B C ET OU" deviennent "A B OU A C OU ET"
        """
        old_fcn = self.__fcn_npi[:]
        self.__fcn_npi = []
        modif = False
        for card in old_fcn:
            if not card.name == "OR":
                self.__fcn_npi.append(card)
                continue
            if self.__fcn_npi[-1].name != "AND":  # 1er cas
                litteralA = self.__get_proposition()
                if self.__fcn_npi[-1].name != "AND":  # pas de la bonne forme
                    self.__fcn_npi.extend(litteralA)  # on remet en place
                    self.__fcn_npi.append(card)
                    continue
                self.__fcn_npi.pop()  # AND
                litteralC = self.__get_proposition()
                litteralB = self.__get_proposition()
            else:  # 2nd cas
                self.__fcn_npi.pop()  # AND
                litteralC = self.__get_proposition()
                litteralB = self.__get_proposition()
                litteralA = self.__get_proposition()
            modif = True
            self.__fcn_npi.extend(litteralA+litteralB+[Card("OR")])
            litteralA = [Card(card.name) for card in litteralA]  # copie
            self.__fcn_npi.extend(litteralA + litteralC
                                  + [Card("OR"), Card("AND")])
        if modif:
            self.__develop()

    def __to_fcn_npi(self):
        """Calcule et renvoie la Forme Normale Conjonctive en NPI.

        :return: fcn
        :rtype: list
        """
        self.__elim_then()
        self.__morgan()
        self.__elim_not()
        self.__develop()
        return self.__fcn_npi

    @staticmethod
    def __npi_to_list(clause_npi):
        """Transforme une clause sous forme d'une liste en NPI en une clause
        sous forme d'une liste de littéraux représentés par des entiers.

        :param clause: une clause sous forme d'une liste en NPI
        :type clause: list

        :return: la clause sous forme d'une liste de littéraux, ou None si un
                 littéral et sa négation apparaissent dans la clause
        :rtype: list
        """
        clause_set = set()  # Pour éviter les doublons dans une clause
        while clause_npi:
            card = clause_npi.pop()
            if card.name == "OR":
                continue
            sign = -1 if card.is_not() else 1
            if sign == -1:
                card = clause_npi.pop()
            value = ord(card.name) - ord('A') + 1
            if -sign * value in clause_set:
                return None
            clause_set.add(sign * value)
        return list(clause_set)

    def __to_clause_list(self):
        """Calcule et renvoie la Forme Normale Conjonctive sous forme d'une
        liste de clauses, une clause étant représentée par une liste de
        littéraux. Chaque variable est représentée par un entier positif, et sa
        négation par l'entier opposé.

        Par exemple (A OU B) ET (NON B OU NON C) est représenté par
        [[1,2], [-2,-3]].

        :return: clause_list
        :rtype: list
        """
        self.__to_fcn_npi()
        self.__clause_list = []
        while self.__fcn_npi:
            if self.__fcn_npi[-1].name == "AND":
                self.__fcn_npi.pop()
                continue
            clause = self.__npi_to_list(self.__get_proposition())
            if clause is not None:
                self.__clause_list.append(clause)
        return self.__clause_list
