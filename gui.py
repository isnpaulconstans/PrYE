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
    "Ergo": "carteCQFD.gif",
    "Back": "carteDos.gif"
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

        self.proof = Proof()
        self.deck = Deck()
        self.photos = {name: tk.PhotoImage(file=IMAGE[name])
                       for name in IMAGE}
        self.cards = [[] for _ in range(5)]  # les 5 lignes de cartes

        self.__init_menu__()
        self.__init_canvas__()

        self.num_player = 0
        self.nb_player = 4
        self.hands = [self.deck.draw(5) for _ in range(4)]
        self.hands[self.num_player].extend(self.deck.draw(2)) #on ajoute 2 cartes
        self.pile = []
        self.selected_card = None
        self.affiche_cards(self.hands[self.num_player], 4)

        self.name = tk.Label(text="Ergo le jeu", font="Arial 16 italic")
        self.name.grid(row=1, column=0)
        self.slogan = tk.Label(text="Prouve que tu existes ...",
                               font="Arial 28 italic")
        self.slogan.grid(row=6, column=1)
        self.but_play = tk.Button(text="play", command=self.play)
        self.but_play.grid(row=5, column=0)
        # liens bouttons souris
        self.can.bind('<Button-1>', func=self.select)
        self.can.bind('<Button1-Motion>', func=self.move)
        self.can.bind("<ButtonRelease-1>", func=self.drop)
        self.can.bind("<Button-3>", func=self.switch)


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
        # TODO faire méthode affichage numéro joueur et changement joueur
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
        # le dos de cartes
        for (row, col) in [(0,11),(1,2),(1,11)]:
            xdeb = col * CARD_WIDTH + CARD_WIDTH // 2
            y = 4 * (CARD_HEIGHT+2) + (CARD_HEIGHT + 10) * row + CARD_HEIGHT//2
            for index in range(5):
                x = xdeb +  index * CARD_WIDTH
                self.can.create_image(x, y, image=self.photos["Back"])


    def display_current_player(self, num_player):

        self.can.create_text(CARD_WIDTH, 4*CARD_HEIGHT+50, text=P1,
                             font="Arial 16 italic", fill="blue")
        self.can.create_text(CARD_WIDTH, 5*CARD_HEIGHT+50, text=P2,
                             font="Arial 16 italic", fill="blue")
        self.can.create_text(10*CARD_WIDTH, 4*CARD_HEIGHT+50, text=P3,
                             font="Arial 16 italic", fill="blue")
        self.can.create_text(10*CARD_WIDTH, 5*CARD_HEIGHT+50, text=P4,
                             font="Arial 16 italic", fill="blue")


    def play(self):
        """Valide un coup si possible, et passe au joueur suivant (TODO)."""
        if len(self.hands[self.num_player]) != 5:
            messagebox.showwarning("Ergo", "Il faut garder 5 cartes pour valider.")
            return
        if not self.proof.is_all_correct():
            messagebox.showwarning("Ergo", "Jeu invalide")
            return
        # TODO carte ergo et gagnant
        # passe au joueur suivant.
        self.num_player = (self.num_player + 1) % self.nb_player
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.affiche_cards(self.hands[self.num_player], 4)
        self.proof.reset_added()
        self.can.delete("pile")

    def affiche_cards(self, card_list, row):
        """affiche la liste de carte card_list à la ligne row (0 à 3 pour les
        prémisses, 4 pour la main du joueur"""
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
    # TODO creer methode passage coord en col et row
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
                self.selected_card = self.hands[self.num_player].pop(col)
                self.affiche_cards(self.hands[self.num_player], 4)
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
        self.hands[self.num_player].append(self.selected_card)
        self.can.delete("selected")
        self.affiche_cards(self.hands[self.num_player], 4)
        self.selected_card = None

    def switch(self, event):
        """TODO retourne la parenthèse"""
        # creer retourner faisant appel passage + .turn_parenthesis
        num = self.can.find_closest(event.x, event.y)
        if "card" in self.can.gettags(num):
            row = event.y//CARD_HEIGHT
            col = event.x//CARD_WIDTH
            if row == 4 and 2 <= col < 9:
                card = self.hands[self.num_player][col-2]
                card.turn_parenthesis()
                self.affiche_cards(self.hands[self.num_player], 4)



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
