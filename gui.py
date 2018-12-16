#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
import random as rd
from tkinter import messagebox
# import constantes as cst
from cards import Proof, Deck

CARD_HEIGHT = 70
CARD_WIDTH = 50
HEIGHT = 6 * CARD_HEIGHT + 20
WIDTH = 1000

CARPET_COLOR = "ivory"

# images cartes
IMAGE = {
    "THEN": "carteImp.gif",
    "A": "carteAb.gif",
    "B": "carteB.gif",
    "C": "carteC.gif",
    "D": "carteD.gif",
    "AND": "carteEt.gif",
    "OR": "carteOu.gif",
    "NOT": "carteNeg.gif",
    "(": "carteOpenParenthesis.gif",
    ")": "carteCloseParenthesis.gif",
    "Ergo": "carteCQFD.gif"
    }


class ErgoGui(tk.Tk):
    """Interface graphique.
    TODO
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ergo")
        self.geometry("1200x500")  # dimension fenetre jeu
        self.resizable(width=False, height=False)
        self.__init_menu__()
        self.__init_canvas__()

        self.proof = Proof()
        self.deck = Deck()
        self.photos = {name: tk.PhotoImage(file=IMAGE[name])
                       for name in IMAGE}
        self.cards = [[] for _ in range(5)]  # les 5 lignes de cartes

        self.hand = self.deck.draw(5)
        self.affiche_cards(self.hand, 4)

        self.name = tk.Label(text="Ergo le jeu", font="Arial 16 italic")
        self.name.grid(row=1, column=0)
        self.slogan = tk.Label(text="Prouve que tu existe ...",
                               font="Arial 28 italic")
        self.slogan.grid(row=6, column=1)
        self.but_play = tk.Button(text="play", command=self.play)
        self.but_play.grid(row=5, column=0)
        # TEST
        self.can.bind('<Button-1>', func=self.select)
        self.can.bind('<Button1-Motion>', func=self.move)
        self.can.bind("<ButtonRelease-1>", func=self.drop)


    def __init_menu__(self):
        """creation de la barre de menu."""
        self.barre_menu = tk.Menu(self)
        # creation du menu "Aide"
        self.aide = tk.Menu(self.barre_menu, tearoff=0)
        self.barre_menu.add_cascade(label="Aide", underline=0, menu=self.aide)
        self.aide.add_command(label="Règles", underline=0, command=self.rules)
        self.aide.add_command(label="A propos", underline=0, command=self.version)
        self.aide.add_command(label="Quitter", underline=0, command=self.quitter)
        # afficher le menu
        self.config(menu=self.barre_menu)

    def __init_canvas__(self):
        """Création du canvas de jeu."""
        self.can = tk.Canvas(self, height=HEIGHT, width=WIDTH,
                             bg=CARPET_COLOR)
        for i in range(4):
            self.can.create_line(0, i*CARD_HEIGHT, WIDTH,
                                 i*CARD_HEIGHT, fill="black")
        for i in range(20):
            self.can.create_line(i*CARD_WIDTH, 0, i*CARD_WIDTH,
                                 4*CARD_HEIGHT, fill="red", dash=(4, 4))
        self.can.create_rectangle(0, HEIGHT-CARD_HEIGHT-5,
                                  WIDTH-2*CARD_WIDTH, HEIGHT,
                                  width=5, outline="red")
        self.can.create_rectangle(0, HEIGHT-2*CARD_HEIGHT-15,
                                  WIDTH-2*CARD_WIDTH, HEIGHT-CARD_HEIGHT-10,
                                  width=5, outline="red")
        self.can.create_rectangle(WIDTH-2*CARD_WIDTH+5, HEIGHT-2*CARD_HEIGHT-15,
                                  WIDTH, HEIGHT,
                                  width=5, outline="pink")
        self.can.create_text(CARD_WIDTH, 4*CARD_HEIGHT+50, text="Joueur 1",
                             font="Arial 16 italic", fill="blue")
        self.can.create_text(CARD_WIDTH, 5*CARD_HEIGHT+50, text="Joueur 2",
                             font="Arial 16 italic", fill="blue")
        self.can.create_text(10*CARD_WIDTH, 4*CARD_HEIGHT+50, text="Joueur 3",
                             font="Arial 16 italic", fill="blue")
        self.can.create_text(10*CARD_WIDTH, 5*CARD_HEIGHT+50, text="Joueur 4",
                             font="Arial 16 italic", fill="blue")
        self.can.create_text(18*CARD_WIDTH+50, 4*CARD_HEIGHT+50,
                             text="Pile", font="Arial 16 italic", fill="blue")
        for i in range(4):
            tk.Label(text="Prémisse "+str(i+1)).grid(row=i+1, column=2)
        self.can.grid(row=1, column=1, rowspan=5)

    def play(self):
        """lance le jeu en melangeant le jeu de carte et en distribuant
        5 cartes au joueur """
        self.hand = self.deck.draw(5)
        self.affiche_cards(self.hand, 2)

    def affiche_cards(self, card_list, row):
        """affiche dans le canvas en bas la main du joueur"""
        for index, card in enumerate(card_list):
            self.cards[row] = self.can.create_image(2*CARD_WIDTH+
                CARD_WIDTH // 2 + index * CARD_WIDTH,
                CARD_HEIGHT//2 + row * (CARD_HEIGHT+1) + 4 * (row == 4),
                image=self.photos[card.valeur],
                tag="card"
                )

    def place(self, event):
        """TEST place la carte sur un premice si possible
        Renvoie True si ok, False sinon."""
        pass

    def switch(self):
        """TEST retourne la parenthèse"""
        pass

    def select(self, event):
        """TEST : selectionne une carte"""
        num = self.can.find_closest(event.x, event.y)
        if "card" in self.can.gettags(num):
            self.can.addtag_withtag("selected", num)
            self.can.tag_raise(num)  # pour passer en avant plan

    def move(self, event):
        """TEST : déplace la carte."""
        num = self.can.find_withtag("selected")
        self.can.coords(num, event.x, event.y)

    def drop(self, event):
        """TEST : place la carte sur la grille, si en dehors place sur pile"""
        lig, col = event.y//70, event.x//50
        if 0 <= event.x <= WIDTH and 0 <= event.y <= HEIGHT:
            self.can.coords("selected", CARD_WIDTH*(col+0.5),
                            CARD_HEIGHT*(lig+0.5))
        else:
            self.can.coords("selected", WIDTH-CARD_WIDTH, HEIGHT-CARD_HEIGHT/2)
        self.can.dtag("selected", "selected")

    def version(self):
        """version du jeux"""
        messagebox.showinfo("Ergo", "Version Alpha 16/12/18")

    def rules(self):
        """Affiche les règles du jeu"""
        texte =""
        with open("regles_ergo.txt") as fic:
            for ligne in fic:
                texte += ligne
        messagebox.showinfo("Ergo", texte)

    def quitter(self):
        """Quitte"""
        self.destroy()


if __name__ == '__main__':
    ergoGui = ErgoGui()
    ergoGui.mainloop()
