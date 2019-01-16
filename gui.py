#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
from tkinter import messagebox
from cards import Proof, Deck

CARD_HEIGHT = 70
CARD_WIDTH = 50
HEIGHT = 6 * CARD_HEIGHT + 20
WIDTH = 1000

CARPET_COLOR = "ivory"

# images cartes
IMAGE = {
    "THEN": "carteImp.gif",
    "A": "carteA.gif",
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

        self.hand = self.deck.draw(7)
        self.pile = []
        self.selected_card = None
        self.num_player = 0
        self.nb_player = 4
        self.affiche_cards(self.hand, 4)

        self.name = tk.Label(text="Ergo le jeu", font="Arial 16 italic")
        self.name.grid(row=1, column=0)
        self.slogan = tk.Label(text="Prouve que tu existes ...",
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
        """Valide un coup si possible, et passe au joueur suivant (TODO)."""
        if len(self.hand) != 5:
            messagebox.showwarning("Ergo", "Il reste plus de 5 cartes.")
            return
        if not self.proof.is_all_correct():
            messagebox.showwarning("Ergo", "Jeu invalide")
            return
        # passe au joueur suivant.
        self.hand.extend(self.deck.draw(2))
        self.affiche_cards(self.hand, 4)
        self.proof.reset_added()
        self.can.delete("pile")

    def affiche_cards(self, card_list, row):
        """affiche la liste de carte card_list à la ligne row (0 à 3 pour les
        prémisses, 4 ou 5 pour la main du joueur et à la colonne col 0 ou 1
        si c'est la main du joueur."""
        y = CARD_HEIGHT//2 + row * (CARD_HEIGHT+1) + 4 * (row == 4)
        for num in self.cards[row]:
            if "selected" in self.can.gettags(num):
                continue
            self.can.delete(num)
        self.cards[row] = []
        for index, card in enumerate(card_list):
            x = CARD_WIDTH // 2 + index * CARD_WIDTH
            if row == 4:
                x += 2 * CARD_WIDTH
            self.cards[row].append(
                self.can.create_image(x, y,
                                      image=self.photos[card.name],
                                      tag="card"
                                     )
                )

    def select(self, event):
        """Selectionne une carte, la marque comme "selected", la met en avant
        plan, et l'enlève de l'endroit où elle était (mains, prémisse ou pile).
        """
        num = self.can.find_closest(event.x, event.y)
        if "card" in self.can.gettags(num):
            self.can.addtag_withtag("selected", num)
            row = event.y//CARD_HEIGHT
            col = event.x//CARD_WIDTH - 2 * (row == 4)
            if 0 <= row < 4:  # un des premisses
                self.selected_card = self.proof.pop(row, col)
                if self.selected_card is None:  # impossible de la sélectionner
                    self.can.dtag("selected")
                    return
                self.affiche_cards(self.proof.premises[row], row)
            elif 4 <= row <= 5 and 18 <= col <= 19:  # Pile
                self.selected_card = self.pile.pop()
                self.can.dtag("selected", "pile")
            else:  # carte de la main
                self.selected_card = self.hand.pop(col)
                self.affiche_cards(self.hand, 4)
            self.can.tag_raise(num)  # pour passer en avant plan

    def move(self, event):
        """Déplace la carte marquée "selected"."""
        num = self.can.find_withtag("selected")
        self.can.coords(num, event.x, event.y)

    def drop(self, event):
        """Place la carte marquée "selected" sur la grille, et l'ajoute au bon
        endroit (prémisse, main ou pile) et enlève la marque "selected".
        Si c'est impossible, la remet à la fin de la main."""
        if self.selected_card is None:
            return
        row, col = event.y//CARD_HEIGHT, event.x//CARD_WIDTH
        if 0 <= event.x <= WIDTH and 0 <= row < 4:  # une des premisses
            if self.proof.insert(row, col, self.selected_card):
                self.can.delete("selected")
                self.affiche_cards(self.proof.premises[row], row)
                self.selected_card = None
                return
        elif 4 <= row <= 5 and 18 <= col <= 19:  # Pile
            self.can.coords("selected", WIDTH-CARD_WIDTH, HEIGHT-CARD_HEIGHT/2)
            self.pile.append(self.selected_card)
            self.can.addtag_withtag("pile", "selected")
            self.can.dtag("selected")
            self.selected_card = None
            return
        self.hand.append(self.selected_card)
        self.can.delete("selected")
        self.affiche_cards(self.hand, 4)
        self.selected_card = None

    def switch(self):
        """TODO retourne la parenthèse"""
        pass

    def version(self):
        """affiche la version du jeu"""
        messagebox.showinfo("Ergo", "Version Alpha 09/01/19")

    def rules(self):
        """Affiche les règles du jeu"""
        texte = ""
        with open("regles_ergo.txt", encoding="utf-8") as fic:
            for ligne in fic:
                texte += ligne
        messagebox.showinfo("Ergo", texte)

    def quitter(self):
        """Quitte"""
        self.quit()
        self.destroy()


if __name__ == '__main__':
    ergoGui = ErgoGui()
    ergoGui.mainloop()
