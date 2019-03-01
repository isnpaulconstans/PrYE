#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des démonstrations"""

from cards import Card, CardList, Proof
from copy import deepcopy


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
        """Calcule et renvoie la Forme Normale Conjonctive sous forme d'un
        ensemble de clause, une clause étant représentée par un ensemble de
        littéraux. Chaque variable est représentée par un entier positif, et sa
        négation par l'entier opposé.

        Par exemple (A OU B) ET (NON B OU NON C) est représenté par
        {{1,2}, {-2,-3}}.

        :return: fcn_set
        :rtype: set
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
        """Détermine les variables "démontrées"

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
        self.__fcn = FCN(proof)
        self.__clause_list = self.__fcn.clause_list

    @property
    def clause_list(self):
        if self._proof.modif:
            self.__clause_list = self.__fcn.clause_list
        return self.__clause_list

    @staticmethod
    def __propagation(clause_list, lit):
        """
        supprime toutes les clauses où lit apparaît, et enlève non lit de
        toutes les clauses où il apparait.

        :param clause_list: Une liste de clauses
        :type clause_list: list
        :param lit: un littéral
        :type lit: int
        """
        for clause in clause_list[:]:
            if lit in clause:
                clause_list.remove(clause)
            if -lit in clause:
                clause.remove(-lit)

    def dpll(self, clause_list, model):
        """Détermine un modèle pour la liste de clauses en partant d'un modèle
        partiel.

        :return: True si un modèle de permet de satisfaire la liste de clauses,
                 et False sinon.
                 Modifie la liste de clauses et le modèle partiel.

        :param clause_list: une liste de clauses
        :param model: un modèle partiel
        """
        # recherche de clauses unitaires
        unit_clause = True
        while unit_clause:
            unit_clause = False
            for clause in clause_list:
                if len(clause) != 1:
                    continue
                unit_clause = True
                lit = clause[0]
                model[abs(lit)-1] = (lit > 0)
                self.__propagation(clause_list, lit)
                break
        # S'il n'y a plus de cluase, on a trouvé un modèle
        if clause_list == []:
            return True
        # S'il y a une clause vide, la liste de clauses n'est pas satisfiable
        for clause in clause_list:
            if clause == []:
                return False
        # On cherche une variable non encore déterminée et on cherche à la
        # déterminer par le principe du tiers exclu.
        for ivar, var in enumerate(model):
            if var is not 0:
                continue
            print(ivar, var)
            for valeur in (False, True):
                model_tmp = model[:]
                model_tmp[ivar] = valeur
                clause_list_tmp = deepcopy(clause_list)
                lit = ivar + 1 if valeur else -ivar-1
                self.__propagation(clause_list_tmp, lit)
                # si lit n'est pas satisfiable, non lit est démontré
                if not self.dpll(clause_list_tmp, model_tmp):
                    model[ivar] = not valeur
                    self.__propagation(clause_list, -lit)
                    return self.dpll(clause_list, model)
            # rien de donne de contradiction : on ne peut rien conclure sur
            # cette variable
            model[ivar] = None
        # on ne peut rien conclure de plus, mais le modèle est satisfiable
        return True

    def conclusion(self):
        """Détermine les variables "démontrées"

        :return: None si les prémisses conduisent à une contradiction,
                 ou une liste associant à chaque variable 'A', 'B', 'C' et 'D'
                 soit True si elle est prouvée, False si la négation est
                 prouvée, on None si on ne peut rien conclure.
        :rtype: list ou NoneType"""
        clause_list = deepcopy(self.__fcn.clause_list)
        model = [0] * 4  # 0 signifie non encore testé
        if not self.dpll(clause_list, model):
            return None
        return model


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
        """Détermine les variables "démontrées"

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
#    p.premises[0] = CardList([Card("NOT"), Card("("),
#                              Card("B"), Card("THEN"), Card("A"), Card(")"),
#                              Card("AND"), Card("C"), Card("OR"), Card("D"),
#                              Card("AND"), Card("B")])
    p.premises[0] = CardList([Card("A"), Card("THEN"), Card("B")])
    p.premises[1] = CardList([Card("A"), Card("OR"), Card("NOT"), Card("B")])
    demo = DPLL(p)
