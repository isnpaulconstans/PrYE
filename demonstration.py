#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des démonstrations"""

from cards import Card, CardList


class Demonstration():
    """Classe générale pour l'évaluation d'une liste de cartes."""
    def __init__(self, premises):
        """Constructeur de la classe.

        :param premises: Une liste de 4 premisses
        :type premises: list of CardList

        :return: objet Demonstration
        :rtype: Demonstration"""
        self.premises = premises
        for premise in premises:
            assert premise.npi is not None

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
        nb_premises = 0
        self.npi = []
        for premise in premises:
            if len(premise.npi) > 0:
                nb_premises += 1
            self.npi.extend(premise.npi)
        self.npi.extend([Card("AND") for _ in range(nb_premises-1)])
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
        modif = True
        while modif:
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
                operator.name = "OR" if operator.name == "AND" else "AND"
                self.__insert_not()
                self.fcn.append(Card("NOT"))
                self.fcn.append(operator)

    def __elim_not(self):
        """Élimine les doubles négations de fcn."""
        old_fcn = self.fcn[:]
        self.fcn = []
        for card in old_fcn:
            if not (card.is_not() and self.fcn[-1].is_not()):
                self.fcn.append(card)
                continue
            self.fcn.pop()

    def __devlop(formule):
        """Développe les expressions :

        * A B C ET OU devient A B OU A C OU ET

        * A B ET C OU devient A C OU B C OU ET

        :param formule: une formule en NPI sans implication ni NON et ou
          NON OU
        :type formule: list
        :return: la formule en forme
        :rtype: list
        """
        # TODO à taper
        pass

    def to_fcn(self):
        """Forme Normale Conjonctive."""
        self.__elim_then()
        self.__morgan()
        self.__elim_not()
        self.__devlop()


class ForceBrute(Demonstration):
    """Évaluation par force brute."""
    def _to_bin(n):
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
    def conclusion(self):
        """
        :return: None si les prémisses conduisent à une contradiction,
                 ou une liste associant à chaque variable 'A', 'B', 'C' et 'D'
                 soit True si elle est prouvée, False si la négation est
                 prouvée, on None si on ne peut rien conclure.
        :rtype: list ou NoneType"""
        models = []
        for code in range(16):
            interpretation = _to_bin(code)
            for premise in self.premises:
                if not premise.evalue(interpretation):
                    break
            else:  # interpretation valable pour toutes les prémisses
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

if __name__ == "__main__":
    card_list = CardList([Card("NOT"), Card("("), Card("A"), Card("AND"),
                          Card("NOT"), Card("B"), Card(")"), Card("THEN"),
                          Card("("), Card("A"), Card("AND"), Card("("),
                          Card("B"), Card("THEN"), Card("C"), Card(")"), Card(")")])
    demo = DPLL([card_list])
