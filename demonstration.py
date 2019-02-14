#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des démonstrations"""

from cards import Card, CardList, Proof


class Demonstration():
    """Classe abstraite pour l'évaluation d'une liste de CardList."""
    def __init__(self, premises):
        """Constructeur de la classe.

        :param premises: Une liste de premisses
        :type premises: list of CardList

        :return: objet Demonstration
        :rtype: Demonstration"""
        self.premises = premises
        nb_premises = 0
        self.npi = []
        for premise in premises:
            assert premise.npi is not None
            if premise.npi != []:
                nb_premises += 1
            self.npi.extend(premise.npi)
        self.npi.extend([Card("AND") for _ in range(nb_premises-1)])

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
    def __init__(self, premises):
        super().__init__(premises)
        self.fcn = []

    def __insert_not(self):
        """Insère un NOT avant la dernière proposition de fcn."""
        pile = []
        nb_exp = 1  # on doit dépiler une proposition
        while nb_exp != 0:
            pile.append(self.fcn.pop())
            if pile[-1].is_letter():
                nb_exp -= 1
            elif pile[-1].is_operator():
                nb_exp += 1
        self.fcn.append(Card("NOT"))
        while pile:
            self.fcn.append(pile.pop())

    def __elim_then(self):
        """Génère self.fcn à partir de self.npi
        en ramplaçant A -> B par non A ou B
        """
        self.fcn = []
        for card in self.npi:
            if card.name != "THEN":
                self.fcn.append(card)
                continue
            self.__insert_not()
            self.fcn.append(Card("OR"))

    def __morgan(self):
        """Élimine les NON ET et NON OU de fcn en utilisant les lois de Morgan.
        """
        old_fcn = self.fcn[:]
        self.fcn = []
        modif = False
        for card in old_fcn:
            if not card.is_not():
                self.fcn.append(card)
                continue
            if not self.fcn[-1].is_operator():
                self.fcn.append(card)
                continue
            modif = True  # NON ET ou NON OU
            operator = self.fcn.pop()
            operator_name = "OR" if operator.name == "AND" else "AND"
            self.__insert_not()
            self.fcn.append(Card("NOT"))
            self.fcn.append(Card(operator_name))
        if modif:
            self.__morgan()

    def __elim_not(self):
        """Élimine les doubles négations de fcn."""
        old_fcn = self.fcn[:]
        self.fcn = []
        for card in old_fcn:
            if not (card.is_not() and self.fcn[-1].is_not()):
                self.fcn.append(card)
                continue
            self.fcn.pop()

    def __devlop(self):
        """Développe les expressions :

        "A B C ET OU" ou "B C ET A OU" deviennent "A B OU A C OU ET"
        """
        def get_litteral():
            if self.fcn[-1].is_not():
                neg = self.fcn.pop()
                return [self.fcn.pop(), neg]
            return [self.fcn.pop()]

        old_fcn = self.fcn[:]
        self.fcn = []
        modif = False
        for card in old_fcn:
            if not card.name == "OR":
                self.fcn.append(card)
                continue
            if self.fcn[-1].name == "AND":
                self.fcn.pop()
                litteralC = get_litteral()
                litteralB = get_litteral()
                litteralA = get_litteral()
            elif self.fcn[-2].name == "AND" or (self.fcn[-2].is_not() and
                                                self.fcn[-3].name == "AND"):
                litteralA = get_litteral()
                self.fcn.pop()  # AND
                litteralC = get_litteral()
                litteralB = get_litteral()
            else:
                self.fcn.append(card)
                continue
            modif = True
            self.fcn.extend(litteralA+litteralB+[Card("OR")])
            litteralA = [Card(card.name) for card in litteralA]  # copie
            self.fcn.extend(litteralA+litteralC+[Card("OR"), Card("AND")])
        if modif:
            self.__devlop()

    def to_fcn(self):
        """Forme Normale Conjonctive."""
        self.__elim_then()
        self.__morgan()
        self.__elim_not()
        self.__devlop()
        return self.fcn


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
        assert self.npi is not None
        if self.npi == []:
            return True
        pile = []
        for card in self.npi:
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
    demo = ForceBrute(p.premises)
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
    demo = DPLL([CardList([Card("NOT"), Card("("),
                           Card("C"), Card("OR"), Card("D"),
                           Card(")"), Card("OR"), Card("A")]),
                 CardList([ Card("NOT"), Card("B"), Card("THEN"),  Card("NOT"),
                           Card("A")])
                 ])
