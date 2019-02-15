#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des démonstrations"""

from cards import Card, CardList, Proof


class Demonstration():
    """Classe abstraite pour l'évaluation d'une liste de CardList."""
    def __init__(self, proof):
        """Constructeur de la classe.

        :param proof: Une preuve
        :type proof: Proof

        :return: objet Demonstration
        :rtype: Demonstration"""
        self._proof = proof

    def conclusion(self):
        """
        :return: None si les prémisses conduisent à une contradiction,
                 ou une liste associant à chaque variable 'A', 'B', 'C' et 'D'
                 soit True si elle est prouvée, False si la négation est
                 prouvée, on None si on ne peut rien conclure.
        :rtype: list ou NoneType"""
        raise NotImplementedError


class DPLL(Demonstration):
    """Évaluation par l'algorithme de Davis-Putnam-Logemann-Loveland."""
    def __init__(self, proof):
        """Constructeur de la classe.

        :param proof: Une preuve
        :type proof: Proof

        :return: objet Demonstration
        :rtype: Demonstration"""
        super().__init__(proof)
        self.__fcn = self.__to_fcn()

    @property
    def fcn(self):
        """Renvoie la preuve sous forme conjonctive normale.

        :return: fcn
        :rtype: list
        """
        if not self._proof.modif:
            return self.__fcn
        return self.__to_fcn()

    def __get_proposition(self):
        """renvoie la derniere proposition de fcn en npi.

        :return: proposition
        :rtype: list
        """
        pile = []
        nb_exp = 1  # on doit dépiler une proposition
        while nb_exp != 0:
            pile.append(self.__fcn.pop())
            if pile[-1].is_letter():
                nb_exp -= 1
            elif pile[-1].is_operator():
                nb_exp += 1
        pile.reverse()
        return pile

    def __insert_not(self):
        """Insère un NOT avant la dernière proposition de fcn."""
        proposition = self.__get_proposition()
        self.__fcn.append(Card("NOT"))
        self.__fcn.extend(proposition)

    def __elim_then(self):
        """Génère self.__fcn à partir de self.npi
        en ramplaçant A -> B par non A ou B
        """
        self.__fcn = []
        for card in self._proof.npi:
            if card.name != "THEN":
                self.__fcn.append(card)
                continue
            self.__insert_not()
            self.__fcn.append(Card("OR"))

    def __morgan(self):
        """Élimine les NON ET et NON OU de fcn en utilisant les lois de Morgan.
        """
        old_fcn = self.__fcn[:]
        self.__fcn = []
        modif = False
        for card in old_fcn:
            if not card.is_not():
                self.__fcn.append(card)
                continue
            if not self.__fcn[-1].is_operator():
                self.__fcn.append(card)
                continue
            modif = True  # NON ET ou NON OU
            operator = self.__fcn.pop()
            operator_name = "OR" if operator.name == "AND" else "AND"
            self.__insert_not()
            self.__fcn.append(Card("NOT"))
            self.__fcn.append(Card(operator_name))
        if modif:
            self.__morgan()

    def __elim_not(self):
        """Élimine les doubles négations de fcn."""
        old_fcn = self.__fcn[:]
        self.__fcn = []
        for card in old_fcn:
            if not (card.is_not() and self.__fcn[-1].is_not()):
                self.__fcn.append(card)
                continue
            self.__fcn.pop()

    def __develop(self):
        """Développe les expressions :

        "A B C ET OU" ou "B C ET A OU" deviennent "A B OU A C OU ET"
        """
        old_fcn = self.__fcn[:]
        self.__fcn = []
        modif = False
        for card in old_fcn:
            if not card.name == "OR":
                self.__fcn.append(card)
                continue
            if self.__fcn[-1].name != "AND":
                litteralA = self.__get_proposition()
                if self.__fcn[-1].name != "AND":
                    self.__fcn.extend(litteralA)
                    self.__fcn.append(card)
                    continue
                self.__fcn.pop()  # AND
                litteralC = self.__get_proposition()
                litteralB = self.__get_proposition()
            else:
                self.__fcn.pop()  # AND
                litteralC = self.__get_proposition()
                litteralB = self.__get_proposition()
                litteralA = self.__get_proposition()
#            if self.__fcn[-1].name == "AND":
#                self.__fcn.pop()
#                litteralC = self.__get_proposition()
#                litteralB = self.__get_proposition()
#                litteralA = self.__get_proposition()
#            elif self.__fcn[-2].name == "AND" or (
#                    self.__fcn[-2].is_not() and self.__fcn[-3].name == "AND"):
#                litteralA = self.__get_proposition()
#                self.__fcn.pop()  # AND
#                litteralC = self.__get_proposition()
#                litteralB = self.__get_proposition()
#            else:
#                self.__fcn.append(card)
#                continue
            modif = True
            self.__fcn.extend(litteralA+litteralB+[Card("OR")])
            litteralA = [Card(card.name) for card in litteralA]  # copie
            self.__fcn.extend(litteralA+litteralC+[Card("OR"), Card("AND")])
        if modif:
            self.__develop()

    def __to_fcn(self):
        """Calcule et renvoie la Forme Normale Conjonctive.

        :return: fcn
        :rtype: list
        """
        self.__elim_then()
        self.__morgan()
        self.__elim_not()
        self.__develop()
        return self.__fcn


class ForceBrute(Demonstration):
    """Évaluation par force brute."""
    @staticmethod
    def __to_bin(n):
        """Renvoie une liste de booléens correspondant à l'écriture en binaire
        sur 4 bits de l'entier n.

        :param n: Un entier entre 0 et 15
        :type n: int
        :return: l'écriture booléenne en binaire sur 4 bits de n.
        :rtype: list
        """
        res = [False]*4
        i = 3
        while n > 0:
            res[i] = (n % 2 == 1)
            n //= 2
            i -= 1
        return res

    def evalue(self, interpretation):
        """Évalue la liste en fonction du modèle. npi doit être calculé.
        :param interpretation: liste de 4 booléens correspondant aux valeurs de
        A, B, C et D

        :type interpretation: list
        :return: Valeur de la liste de carte en fonction du modèle.
        :rtype: boolean
        """
        assert self._proof.npi is not None
        if self._proof.npi == []:
            return True
        pile = []
        for card in self._proof.npi:
            if card.is_letter():
                val = interpretation[ord(card.name)-ord('A')]
            elif card.is_operator():
                val2 = pile.pop()
                val1 = pile.pop()
                if card.name == "AND":
                    val = val1 and val2
                elif card.name == "OR":
                    val = val1 or val2
                else:  # "THEN"
                    val = (not val1) or val2
            else:  # "NOT"
                val = not pile.pop()
            pile.append(val)
        val = pile.pop()
        assert pile == []  # sinon il y a eu un problème quelque part
        return val

    def conclusion(self):
        """
        :return: None si les prémisses conduisent à une contradiction,
                 ou une liste associant à chaque variable 'A', 'B', 'C' et 'D'
                 soit True si elle est prouvée, False si la négation est
                 prouvée, on None si on ne peut rien conclure.
        :rtype: list ou NoneType"""
        models = []
        for code in range(16):
            interpretation = self.__to_bin(code)
            if self.evalue(interpretation):
                models.append(interpretation)
        if models == []:
            return None
        result = models[0]
        # il faut déterminer pour chaque lettre si toutes les valeurs possibles
        # sont les mêmes
        for interpretation in models:
            for i_lettre in range(4):
                if result[i_lettre] != interpretation[i_lettre]:
                    result[i_lettre] = None
        return result


def _tests():
    """Des tests..."""
    card_list = CardList([Card("NOT"), Card("("), Card("A"), Card("AND"),
                          Card("NOT"), Card("B"), Card(")"), Card("AND"),
                          Card("D")])
    p = Proof()
    p.premises[0] = card_list
    p.premises[1] = CardList([Card("NOT"), Card("B")])
    p.premises[2] = CardList([Card("D"), Card("THEN"), Card("C")])
    demo = ForceBrute(p)
    print(demo.conclusion())
    print(p.score())



if __name__ == "__main__":
#    card_list = CardList([Card("NOT"), Card("("), Card("A"), Card("AND"),
#                          Card("NOT"), Card("B"), Card(")"), Card("THEN"),
#                          Card("("), Card("A"), Card("AND"), Card("("),
#                          Card("B"), Card("THEN"), Card("C"), Card(")"), Card(")")])
#    demo = DPLL([card_list])
#    fb = ForceBrute([card_list])
#    card_list.to_fcn()
#    print(card_list.fcn)
#    _tests()
    p = Proof()
    p.premises[0] = CardList([Card("NOT"), Card("("),
                              Card("B"), Card("THEN"), Card("A"), Card(")"),
                              Card("AND"), Card("C"), Card("OR"), Card("D"),
                              Card("AND"), Card("B")])
    demo = DPLL(p)
