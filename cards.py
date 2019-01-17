#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestion des cartes et des preuves."""

from random import shuffle


class Card(object):
    """Les cartes du jeu."""
    # Le niveau de priorité de chaque carte
    PRIORITY = {
        "AND": 1,
        "OR": 2,
        "THEN": 3,
        "NOT": 4,
        "(": 0,
        ")": 0,
        }
    # Le nombre de cartes de chaque type
    NUMBER = {"A": 4, "B": 4, "C": 4, "D": 4,
              "AND": 4, "OR": 4, "THEN": 4,
              "NOT": 6, "(": 4, ")": 4,
#              "Fallacy": 3, "Justification": 3,
#              "TabulaRasa": 1, "Revolution": 1,
#              "WildVar": 1, "WildOp": 1,
#              "Ergo": 3,
             }

    def __init__(self, name):
        """Constructeur de la classe

        :param name: nom de la carte (ET, OU, AND, NOT, ...)
        :type name: string

        :return: Objet Card
        :rtype: Card
        """
        assert name in Card.NUMBER
        self.name = name

    def priority(self):
        """
        :return: le niveau de priorité de la carte. Si la carte n'a pas de
                 niveau de priorité, lève une exception.
        :rtype: int
        """
        try:
            return Card.PRIORITY[self.name]
        except KeyError:
            raise Exception("Card '{}' as no priority".format(self.name))

    def is_letter(self):
        """Indique si la carte est une lettre ou non.

         :rtype: boolean
        """
        return self.name in ["A", "B", "C", "D"]

    def is_operator(self):
        """Indique si la carte est un opérateur.

         :rtype: boolean
        """
        return self.name in ["AND", "OR", "THEN"]

    def is_open(self):
        """Indique si la carte est une parenthèse ouvrante.

         :rtype: boolean
        """
        return self.name == "("

    def is_close(self):
        """Indique si la carte est une parenthèse fermante.

         :rtype: boolean
        """
        return self.name == ")"

    def is_not(self):
        """Indique si la carte est un "NOT".

         :rtype: boolean
        """
        return self.name == "NOT"

    def turn_parenthesis(self):
        """Retourne la parenthèse, si c'en est une, ne fait rien sinon."""
        if self.name == ")":
            self.name = "("
        elif self.name == "(":
            self.name = ")"

    def __repr__(self):
        """:return: le nom de la carte.
        :rtype: string
        """
        return self.name


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
        self.to_npi()

    def append(self, card):
        """Ajoute la carte card à la  fin de la liste.

         :param card: la carte à ajouter
         :type card: Card
        """
        super().append(card)
        self.to_npi()

    def insert(self, index, card):
        """Insère card à la position index.

         :param card: la carte à insérer
         :type card: Card
         :param index: la position à laquelle insérer la carte
         :type index: int
        """
        super().insert(index, card)
        self.to_npi()

    def pop(self, index=-1):
        """Supprime la carte en position index (par défaut la dernière)
        et la renvoie.

        :param index: la position de la carte à renvoyer
        :type index: int
        :return: la carte supprimée
        :rtype: Card
        """
        card = super().pop(index)
        self.to_npi()
        return card

    def is_syntactically_correct(self):
        """Indique si la liste de cartes est syntaxiquement correcte,
        sans s'occuper de la correspondance des parenthèses.

        :return: True si la liste est syntaxiquement correcte, False sinon
        :rtype: boolean
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
            if card1.is_letter() or card1.is_close():
                if card2.is_letter() or card2.is_not():
                    return False
            if card1.is_operator():
                if card2.is_operator() or card2.is_close():
                    return False
            if card1.is_not():
                if card2.is_operator() or card2.is_close() or card2.is_not():
                    return False
            if card1.is_open():
                if card2.is_operator():
                    return False
        return not card2.is_operator()

    def to_npi(self):
        """Met à jour self.npi en :

         * None si la syntaxe de la liste n'est pas correcte

         * une liste de carte correspondant à la notation polonaise inversée de
           la liste de départ sinon."""
        if not self.is_syntactically_correct():
            self.npi = None
            return
        self.npi = []
        stack = []
        for card in self:
            if card.is_letter():
                self.npi.append(card)
            elif card.is_open():
                stack.append(card)
            elif card.is_close():
                while stack != [] and not stack[-1].is_open():
                    self.npi.append(stack.pop())
                if stack == []:  # Pas de parenthèse ouvrante correspondante
                    self.npi = None
                    return
                else:  # On enlève la parenthèse ouvrante correspondante
                    stack.pop()
            else:
                while stack != [] and stack[-1].priority() >= card.priority():
                    self.npi.append(stack.pop())
                stack.append(card)
        while stack != []:
            card = stack.pop()
            if card.is_open():  # pas de parenthèse fermante correspondante
                self.npi = None
                return
            self.npi.append(card)

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


class Deck(list):
    """Le paquet de cartes."""
    def __init__(self):
        """Constructeur de la classe

        :return: un paquet de cartes mélangées
        :rtype: Deck
        """
        super().__init__()
        for carte, number in Card.NUMBER.items():
            self.extend([Card(carte) for _ in range(number)])
        shuffle(self)

    def draw(self, number):
        """
        :return: number cartes du paquet s'il en reste assez, la fin du
                 paquet ou une liste vide sinon.
        :rtype: list
        """
        res = []
        while len(res) < number and self != []:
            res.append(self.pop())
        return res

    def append(self, card):
        """Ajoute une carte (possible avec Tabula Rasa).

        :param card: la carte à ajouter
        :type card: Card"""
        self.append(card)

    def reset(self):
        """Réinitialise le paquet de cartes."""
        self.__init__()

    def is_finished(self):
        """Indique si la paquet est terminé.

        :return: True si la paquet est terminé, False sinon
        :rtype: boolean"""
        return self == []


class Proof(object):
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
        super().__init__()
        self.premises = [CardList() for _ in range(4)]
        self.currently_added = []

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

    def pop(self, premise, index):
        """Enlève la carte en position index de la prémisse premise à
        condition qu'elle vienne d'être ajoutée.

        :param premise: le numéro de la prémisse
        :type premise: int
        :param index: la position dans la prémisse de la carte à supprimer
        :type index: int
        :return: la carte en question ou None si on ne peut pas l'enlever.
        :rtype: Card ou NoneType"""
        try:
            self.currently_added.remove((premise, index))
        except ValueError:
            return None
        if self.currently_added != []:
            (premise1, index1) = self.currently_added.pop()
            if premise1 == premise and index1 >= index:
                index1 -= 1
            self.currently_added.append((premise1, index1))
        card = self.premises[premise].pop(index)
        return card

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

    def score(self):
        """
        :return: Le score correspondant à la preuve, c'est à dire le nombre de
                 cartes qui la compose.
        :rtype: int
        """
        return sum([len(premise) for premise in self.premises])


def _to_bin(n):
    """Renvoie une liste de booléens correspondant à l'écriture en binaire sur
    4 bits de l'entier n.

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


def _tests():
    """Des tests..."""
    card_list = CardList([Card("NOT"), Card("("), Card("A"), Card("AND"),
                          Card("NOT"), Card("B"), Card(")"), Card("AND"),
                          Card("D")])
    p = Proof()
    p.premises[0] = card_list
    p.premises[1] = CardList([Card("NOT"), Card("B")])
    p.premises[2] = CardList([Card("D"), Card("THEN"), Card("C")])
    print(p.conclusion())
    print(p.score())


if __name__ == '__main__':
    print("Bienvenue dans Ergo, le jeu où vous prouvez votre existence.")
    _tests()
