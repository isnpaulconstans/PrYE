#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
from tkinter import messagebox
from Constantes import Constantes as Cst


class ErgoCanvas(tk.Canvas):
    """Création du canvas de jeu avec les lignes des prémisses, les mains
    et noms des joueurs et la pile"""
    def __init__(self, *args, **kwargs):
        self.height = 6 * Cst.CARD_HEIGHT + 3 * Cst.LINE_WIDTH
        self.width = 23 * Cst.CARD_WIDTH
        super().__init__(*args, **kwargs,
                         height=self.height, width=self.width,
                         bg=Cst.CARPET_COLOR)
        self.photos = {name: tk.PhotoImage(file='images/'+Cst.IMAGE[name])
                       for name in Cst.IMAGE}
        self.cards = [[] for _ in range(5)]  # les 5 lignes de cartes
        self.selected_card = None
        self.pile = []
        # liens bouttons souris
        self.bind('<Button-1>', func=self.select)
        self.bind('<Button1-Motion>', func=self.move)
        self.bind("<ButtonRelease-1>", func=self.drop)
        self.bind("<Button-3>", func=self.switch)
        # prémisses
        for i in range(5):
            self.create_line(0, i*Cst.CARD_HEIGHT,
                             self.width, i*Cst.CARD_HEIGHT,
                             fill="black")
        for i in range(23):
            self.create_line(i*Cst.CARD_WIDTH, 0,
                             i*Cst.CARD_WIDTH, 4*Cst.CARD_HEIGHT,
                             fill="red", dash=(4, 4))
        # mains
        self.create_rectangle(Cst.LINE_WIDTH//2,
                              4*Cst.CARD_HEIGHT+Cst.LINE_WIDTH//2+1,
                              self.width-3*Cst.CARD_WIDTH-Cst.LINE_WIDTH//2,
                              self.height-(Cst.CARD_HEIGHT-1)-1.5*Cst.LINE_WIDTH,
                              width=Cst.LINE_WIDTH, outline="red")
        self.create_rectangle(Cst.LINE_WIDTH//2,
                              self.height-(Cst.CARD_HEIGHT-1)-1.5*Cst.LINE_WIDTH,
                              self.width-3*Cst.CARD_WIDTH-Cst.LINE_WIDTH//2,
                              self.height-Cst.LINE_WIDTH//2,
                              width=Cst.LINE_WIDTH, outline="red")
        self.create_rectangle(self.width-3*Cst.CARD_WIDTH+Cst.LINE_WIDTH//2+1,
                              4*Cst.CARD_HEIGHT+Cst.LINE_WIDTH//2+1,
                              self.width-Cst.LINE_WIDTH//2,
                              self.height-Cst.LINE_WIDTH//2,
                              width=Cst.LINE_WIDTH, outline="pink")
        self.create_text(21.5*Cst.CARD_WIDTH, 4.5*Cst.CARD_HEIGHT,
                         text="Pile", font="Arial 16 italic", fill="blue")
        # le dos de cartes
        for (row, col) in [(0, 12), (1, 2), (1, 12)]:
            xdeb = col * Cst.CARD_WIDTH + Cst.CARD_WIDTH // 2
            y = 4.5*Cst.CARD_HEIGHT + (Cst.CARD_HEIGHT
                                       + Cst.LINE_WIDTH)*row + Cst.LINE_WIDTH+1
            for index in range(5):
                x = xdeb + index * Cst.CARD_WIDTH
                self.create_image(x, y, image=self.photos["Back"])
        # les noms des joueurs
        self.names = [self.create_text(Cst.CARD_WIDTH*(1 + 10 * (i % 2)),
                                       4.25 * Cst.CARD_HEIGHT
                                       + (i // 2) * (Cst.CARD_HEIGHT +
                                                     Cst.LINE_WIDTH),
                                       text=self.master.player_names[i],
                                       font="Arial 16 italic",
                                       fill="blue")
                      for i in range(4)]
        self.scores = [self.create_text(Cst.CARD_WIDTH*(1 + 10 * (i % 2)),
                                        4.6 * Cst.CARD_HEIGHT
                                        + (i // 2) * (Cst.CARD_HEIGHT +
                                                      Cst.LINE_WIDTH),
                                        text=self.master.scores[i],
                                        font="Arial 16 italic",
                                        fill="blue")
                       for i in range(4)]

    def display_current_player(self, num_player):
        """ Affiche les numéros de joueurs en faisant tourner, le joueur
        courant est toujours en haut à gauche.

        :param num_player: le numéro du joueur courant
        :type num_player: int
        """
        for i, player in enumerate(self.names):
            self.itemconfig(player,
                            text=self.master.player_names[(num_player+i) % 4])
        for i, score in enumerate(self.scores):
            self.itemconfig(score,
                            text=self.master.scores[(num_player+i) % 4])
        for i in range(4):
            fallacy = self.master.fallacy[(num_player+i) % 4]
            tag = "fallacy" + str(i)
            self.delete(tag)
            if fallacy == 0:
                continue
            text = str(fallacy) + " tour" + ("s" if fallacy > 1 else "")
            x1 = Cst.CARD_WIDTH*(.25 + 10 * (i % 2))
            y1 = 4.75 * Cst.CARD_HEIGHT + (i // 2) * (Cst.CARD_HEIGHT +
                                                      Cst.LINE_WIDTH)
            self.create_oval(x1, y1, x1+20, y1+20,
                             outline='red', width=4, tag=tag)
            self.create_line(x1, y1+20, x1+20, y1, fill='red',
                             width=4, tag=tag)
            self.create_text(x1+55, y1+10,
                             text=text, font="Arial 14 italic", fill="red",
                             tag=tag)

    def affiche_cards(self, loc, card_list, row=4):
        """affiche la liste de carte card_list dans la prémisse row ou dans le
        main du joueur

        :param loc: la localisation ("premise" ou "hand")
        :type loc: str
        :param card_list: la liste de cartes à afficher
        :type card_list: list
        :param row: le numéro de la ligne
        :type row: int
        """
        for num in self.cards[row]:
            if "selected" in self.gettags(num):
                continue
            self.delete(num)
        self.cards[row] = []
        for col, card in enumerate(card_list):
            x, y = self.row_col2x_y(loc, row, col)
            card_image = self.create_image(x, y,
                                           image=self.photos[card.name],
                                           tag="card")
            self.cards[row].append(card_image)

    def reset(self):
        """remise à zéro de l'affichage."""
        for row in self.cards:
            while row:
                self.delete(row.pop())

    def row_col2x_y(self, loc, row=4, col=0):
        """Renvoie les coordonnées du centre d'une cartes située à la colonne
        col de la prémisse row, ou de la main, ou sur la pile.

        :param loc: "premise", "hand" ou "pile"
        :type loc: str
        :param row: numéro de la prémisse
        :type row: int
        :param col: position dans la prémisse
        :type row: int

        :return: les coordonnées (x, y) dans le canvas
        :rtype: tuple
        """
        if loc == "pile":
            return (self.width - 1.5*Cst.CARD_WIDTH,
                    self.height - Cst.CARD_HEIGHT)
        y = Cst.CARD_HEIGHT//2 + row * (Cst.CARD_HEIGHT)+1
        x = Cst.CARD_WIDTH // 2 + col * Cst.CARD_WIDTH
        if loc == "hand":
            y += Cst.LINE_WIDTH+1
            x += 2 * Cst.CARD_WIDTH
        return (x, y)

    def x_y2row_col(self, x, y):
        """Transforme les coordonnées dans le canvas en numéro de ligne et de
        colonne.

        :param x: abscisse
        :type x: int
        :param y: ordonnée
        :type x: int

        :return: loc, row, col où

                 * loc est "premise", "hand" ou "pile"
                 * row est le numéro de la prémisse ou de la main
                 * col est la position dans la prémisse ou la main
        """
        row = y//Cst.CARD_HEIGHT
        col = x//Cst.CARD_WIDTH
        if 0 <= row < 4:
            loc = "premise"
        elif 4 <= row <= 5 and 20 <= col <= 22:
            loc = "pile"
        else:
            loc = "hand"
            row = (row - 4) * 2 + col // 10
            col = col % 10 - 2
        return loc, row, col

    def select(self, event):
        """Selectionne une carte, la marque comme "selected", la met en avant
        plan, et l'enlève de l'endroit où elle était (mains, prémisse ou pile).

        :param event: événement
        :type event: tkinter.Event
        """
        num = self.find_closest(event.x, event.y)
        if "card" in self.gettags(num):
            self.addtag_withtag("selected", num)
            loc, row, col = self.x_y2row_col(event.x, event.y)
            if loc == "premise":
                self.selected_card = self.master.proof.pop(row, col)
                if self.selected_card is None:  # impossible de la sélectionner
                    self.dtag("selected")
                    return
                self.affiche_cards(loc, self.master.proof.premises[row], row)
            elif loc == "pile":
                self.selected_card = self.pile.pop()
                self.dtag("selected", "pile")
            else:  # carte de la main
                if self.master.cards_played == 2:
                    messagebox.showwarning("2 cartes", "On ne peut pas jouer "
                                           + "plus de deux cartes")
                    self.dtag("selected")
                    return
                hand = self.master.hands[self.master.num_player]
                self.selected_card = hand.pop(col)
                self.affiche_cards("hand", hand)
                self.master.cards_played += 1
            self.tag_raise(num)  # pour passer en avant plan

    def move(self, event):
        """Déplace la carte marquée "selected".

        :param event: événement
        :type event: tkinter.Event
        """
        num = self.find_withtag("selected")
        self.coords(num, event.x, event.y)

    def drop(self, event):
        """Place la carte marquée "selected" sur la grille, et l'ajoute au bon
        endroit (prémisse, main ou pile) et enlève la marque "selected".
        Si c'est impossible, la remet à la fin de la main.

        :param event: événement
        :type event: tkinter.Event
        """
        def restore(index=7):
            """remet la carte dans la main du joueur."""
            hand = self.master.hands[self.master.num_player]
            hand.insert(index, self.selected_card)
            self.delete("selected")
            self.affiche_cards("hand", hand)
            self.selected_card = None
            self.master.cards_played -= 1

        if self.selected_card is None:
            return
        loc, row, col = self.x_y2row_col(event.x, event.y)
        if loc == "pile":
            x, y = self.row_col2x_y("pile")
            self.coords("selected", x, y)
            self.pile.append(self.selected_card)
            self.addtag_withtag("pile", "selected")
            self.dtag("selected")
            self.selected_card = None
            return
        if loc == "hand":
            restore(col if row == 0 else 7)
            return
        if self.master.fallacy[self.master.num_player] > 0:
            messagebox.showwarning("Fallacy", "Impossible d'ajouter une carte"
                                   + "à la preuve")
            restore()
            return
        if self.selected_card.is_ergo():
            if not self.master.proof.is_all_correct():
                messagebox.showwarning("Ergo", "Jeu invalide")
                restore()
                return
            if not self.master.proof.all_cards_played():
                messagebox.showwarning("Fin de manche", "Toutes les lettres " +
                                       "doivent apparaître pour pouvoir " +
                                       "mettre fin à la manche")
                restore()
                return
            cards = self.master.proof.premises[-1]+[self.selected_card]
            self.affiche_cards(loc, cards, 3)
            self.delete("selected")
            self.selected_card = None
            self.master.fin_manche()
            return
        if self.master.proof.insert(row, col, self.selected_card):
            self.delete("selected")
            self.affiche_cards(loc, self.master.proof.premises[row], row)
            self.selected_card = None
            return

    def switch(self, event):
        """Retourne la parenthèse si c'en est une, dans la main du joueur
        courant.

        :param event: événement
        :type event: tkinter.Event
        """
        num = self.find_closest(event.x, event.y)
        if "card" not in self.gettags(num):
            return
        loc, row, col = self.x_y2row_col(event.x, event.y)
        hand = self.master.hands[self.master.num_player]
        if loc != "hand" or not (0 <= col < len(hand)):
            return
        card = hand[col]
        card.turn_parenthesis()
        self.affiche_cards("hand", hand)
