#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des démonstrations"""

from copy import deepcopy
from Demonstration import Demonstration
from FCN import FCN


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
        """getter pour clause_list."""
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
        :type clause_list: list
        :param model: un modèle partiel composé de 0 (non testé), None
                      (indéfini), True ou False
        :type model: list
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
        # S'il n'y a plus de clause, on a trouvé un modèle
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
        # toutes les variables ont été testées
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
