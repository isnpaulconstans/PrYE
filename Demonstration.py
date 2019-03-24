#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des démonstrations"""


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
