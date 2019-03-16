#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
from tkinter import messagebox
from cards import Proof, Deck
from demonstration import ForceBrute, DPLL
from ordi import OrdiRandom

# Constantes
CARD_HEIGHT = 70 + 1
CARD_WIDTH = 50 + 1
LINE_WIDTH = 5

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

# definition du chemin des lettres de l'animation
LETWAY = [(1, 15), (1, 14), (1, 13), (2, 13), (3, 13), (4, 13), (5, 13),
          (5, 14), (5, 15), (4, 15), (3, 15), (2, 15),  # E
          (1, 11), (1, 10), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (5, 10),
          (5, 11), (4, 11), (3, 11),  # R
          (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (1, 6), (1, 7), (2, 7),
          (3, 7), (4, 6), (5, 7),  # G
          (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (3, 2), (4, 1), (5, 1),
          (5, 2), (5, 3)  # O
          ]


class ErgoGuiIntro(tk.Toplevel):
    """Interface graphique fenetre acceuil avec animation
    et choix du mode de jeu"""
    def __init__(self):
        """Constructeur de la classe

        :return: Objet ErgoGuiIntro
        :rtype: ErgoGuiIntro
        """
        super().__init__()
        self.title("Ergo acceuil")
        self.geometry("850x600")
        self.grab_set()
        self.transient(self.master)
        self.resizable(width=False, height=False)
        self.__init_intro__()
        self.button_choice()
        self.flag = 1
        self.pause = 150
        self.animate_letter(len(LETWAY), LETWAY)

    def __init_intro__(self):
        """ Creation de la fenetre d'animation """
        self.can = tk.Canvas(self, height=500, width=850,
                             bg="skyblue")
        self.can.grid()
        self.img = tk.PhotoImage(file="images/carteDos.gif")
        self.id_img = self.can.create_image(425, 465, image=self.img)

    def rectangle(self, x, y):
        """ création d'un rectangle trace du passage de la carte """
        self.can.create_rectangle(x, y, x+CARD_WIDTH, y+CARD_HEIGHT,
                                  fill="ivory")

    def animate_letter(self, nb_cards, l_way):
        """ deplace la carte sur le canvas en suivant un chemin defini ,
        de façon récursive et laisse la trace du parcours

        :param nb_cards: nombre de cartes à afficher
        :type nb_cards: int

        :param l_way: le chemin à suivre par la carte Ergo
        :type l_way: list
        """
        if self.flag != 1:
            return
        if nb_cards == 0:
            self.flag = 0
            return
        self.can.coords(self.id_img,
                        CARD_WIDTH*(l_way[nb_cards-1][1]+1)-CARD_WIDTH/2,
                        CARD_HEIGHT*l_way[nb_cards-1][0]+CARD_HEIGHT/2)
        self.rectangle(CARD_WIDTH*l_way[nb_cards-1][1],
                       CARD_HEIGHT*l_way[nb_cards-1][0])
        self.can.tag_raise(self.id_img)
        self.after(self.pause, lambda: self.animate_letter(nb_cards-1, l_way))

    def button_choice(self):
        """ Creation des boutons de choix du mode de jeu """
        tk.Button(self, text="Mode seul", bd=7, font="Arial 16",
                  command=lambda: self.choice(1)
                  ).grid()
        tk.Button(self, text="Mode multijoueurs", bd=7, font="Arial 16",
                  command=lambda: self.choice(4)
                  ).grid()

    def choice(self, nb_player):
        """Lance la fenetre de jeu """
        self.master.nb_player = nb_player
        self.master.init_round()
        self.destroy()


class ErgoCanvas(tk.Canvas):
    """Création du canvas de jeu avec les lignes des prémisses, les mains
    et noms des joueurs et la pile"""
    def __init__(self, *args, **kwargs):
        self.height = 6 * CARD_HEIGHT + 3 * LINE_WIDTH
        self.width = 23 * CARD_WIDTH
        super().__init__(*args, **kwargs,
                         height=self.height, width=self.width,
                         bg=CARPET_COLOR)
        self.photos = {name: tk.PhotoImage(file='images/'+IMAGE[name])
                       for name in IMAGE}
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
            self.create_line(0, i*CARD_HEIGHT, self.width, i*CARD_HEIGHT,
                             fill="black")
        for i in range(23):
            self.create_line(i*CARD_WIDTH, 0, i*CARD_WIDTH, 4*CARD_HEIGHT,
                             fill="red", dash=(4, 4))
        # mains
        self.create_rectangle(LINE_WIDTH//2,
                              4*CARD_HEIGHT+LINE_WIDTH//2+1,
                              self.width-3*CARD_WIDTH-LINE_WIDTH//2,
                              self.height-(CARD_HEIGHT-1)-1.5*LINE_WIDTH,
                              width=LINE_WIDTH, outline="red")
        self.create_rectangle(LINE_WIDTH//2,
                              self.height-(CARD_HEIGHT-1)-1.5*LINE_WIDTH,
                              self.width-3*CARD_WIDTH-LINE_WIDTH//2,
                              self.height-LINE_WIDTH//2,
                              width=LINE_WIDTH, outline="red")
        self.create_rectangle(self.width-3*CARD_WIDTH+LINE_WIDTH//2+1,
                              4*CARD_HEIGHT+LINE_WIDTH//2+1,
                              self.width-LINE_WIDTH//2,
                              self.height-LINE_WIDTH//2,
                              width=LINE_WIDTH, outline="pink")
        self.create_text(21.5*CARD_WIDTH, 4.5*CARD_HEIGHT,
                         text="Pile", font="Arial 16 italic", fill="blue")
        # le dos de cartes
        for (row, col) in [(0, 12), (1, 2), (1, 12)]:
            xdeb = col * CARD_WIDTH + CARD_WIDTH // 2
            y = 4.5*CARD_HEIGHT + (CARD_HEIGHT + LINE_WIDTH)*row + LINE_WIDTH+1
            for index in range(5):
                x = xdeb + index * CARD_WIDTH
                self.create_image(x, y, image=self.photos["Back"])
        # les noms des joueurs
        self.names = [self.create_text(CARD_WIDTH*(1 + 10 * (i % 2)),
                                       4.5 * CARD_HEIGHT
                                       + (i // 2) * (CARD_HEIGHT+10),
                                       text=self.master.player_names[i],
                                       font="Arial 16 italic",
                                       fill="blue")
                      for i in range(4)]
        self.scores = [self.create_text(CARD_WIDTH*(1 + 10 * (i % 2)),
                                        4.85 * CARD_HEIGHT
                                        + (i // 2) * (CARD_HEIGHT+10),
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
#        y = CARD_HEIGHT//2 + row * (CARD_HEIGHT+1) + 4 * (row == 4)
        for num in self.cards[row]:
            if "selected" in self.gettags(num):
                continue
            self.delete(num)
        self.cards[row] = []
        for col, card in enumerate(card_list):
            x, y = self.row_col2x_y(loc, row, col)
#            x = CARD_WIDTH // 2 + index * CARD_WIDTH
#            if row == 4:
#                x += 2 * CARD_WIDTH
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
            return (self.width - 1.5*CARD_WIDTH,
                    self.height - CARD_HEIGHT)
        y = CARD_HEIGHT//2 + row * (CARD_HEIGHT)+1
        x = CARD_WIDTH // 2 + col * CARD_WIDTH
        if loc == "hand":
            y += LINE_WIDTH+1
            x += 2 * CARD_WIDTH
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
                 * row est le numéro de la prémisse
                 * col est la position dans la prémisse
        """
        row = y//CARD_HEIGHT
        col = x//CARD_WIDTH
        if 0 <= row < 4:
            loc = "premise"
        elif 4 <= row <= 5 and 20 <= col <= 22:
            loc = "pile"
        else:
            loc = "hand"
            col -= 2
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
        def restore():
            """remet la carte dans la main du joueur."""
            hand = self.master.hands[self.master.num_player]
            hand.append(self.selected_card)
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
        if loc != "premise":
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
        if "card" in self.gettags(num):
            loc, row, col = self.x_y2row_col(event.x, event.y)
#            row = event.y//CARD_HEIGHT
#            col = event.x//CARD_WIDTH - 2
            hand = self.master.hands[self.master.num_player]
            if loc != "hand" or not (0 <= col < len(hand)):
                return
            card = hand[col]
            card.turn_parenthesis()
            self.affiche_cards("hand", hand)


class ErgoGui(tk.Tk):
    """Interface graphique."""
    def __init__(self):
        """Constructeur de la classe

        :return: Objet ErgoGui
        :rtype: ErgoGui
        """
        tk.Tk.__init__(self)
        ErgoGuiIntro()
        self.title("Ergo")
#        self.geometry("1500x500")  # dimension fenetre jeu
        self.resizable(width=False, height=False)
        # initialisation du menu et canvas
        self.__init_menu__()
        self.scores = [0]*4
        self.player_names = ["Joueur "+chr(ord('A')+i) for i in range(4)]
        self.can = ErgoCanvas(self)
        self.can.grid(row=0, column=1, rowspan=7)
        for i in range(4):
            tk.Label(text="Prémisse "+str(i+1)).grid(row=i, column=2)
        tk.Label(text="Ergo le jeu", font="Arial 16 italic").grid(row=0,
                                                                  column=0)
        tk.Label(text="Prouve que tu existes ...",
                 font="Arial 28 italic").grid(row=7, column=1)
        tk.Button(text="jouer", command=self.play).grid(row=5, column=0)

    def init_round(self):
        """Inialise un début de tour."""
        self.deck = Deck()
        self.can.reset()
        self.proof = Proof()
        self.demoDPLL = DPLL(self.proof)
        self.demoFB = ForceBrute(self.proof)
        self.num_player = 0
        self.can.display_current_player(self.num_player)
        self.ordi_player = [False]*self.nb_player + [True]*(4-self.nb_player)
        self.hands = [self.deck.draw(5) for _ in range(4)]
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.cards_played = 0
        self.can.affiche_cards("hand", self.hands[self.num_player])

    def __init_menu__(self):
        """creation de la barre de menu qui permet d'afficher l'aide,
        les règles, la version et de pouvoir quitter le jeu."""
        self.barre_menu = tk.Menu(self)
        # creation du menu "Aide"
        self.aide = tk.Menu(self.barre_menu, tearoff=0)
        self.barre_menu.add_cascade(label="Aide", underline=0, menu=self.aide)
        self.aide.add_command(label="Règles", underline=0, command=self.rules)
        self.aide.add_command(label="A propos", underline=0,
                              command=self.version)
        self.aide.add_command(label="Quitter", underline=0,
                              command=self.quitter)
        # afficher le menu
        self.config(menu=self.barre_menu)

    def play(self):
        """Valide un coup si possible, et passe au joueur suivant."""
        if len(self.hands[self.num_player]) != 5:
            messagebox.showwarning("Ergo",
                                   "Il faut garder 5 cartes pour valider.")
            return
        if not self.proof.is_all_correct():
            messagebox.showwarning("Ergo", "Jeu invalide")
            return
        # passe au joueur suivant.
        if self.deck.is_finished():
            self.fin_manche()
        self.proof.reset_added()
        self.cards_played = 0
        self.can.delete("pile")
        self.num_player = (self.num_player + 1) % 4
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.can.affiche_cards("hand", self.hands[self.num_player])
        self.can.display_current_player(self.num_player)
        if self.ordi_player[self.num_player]:
            self.ordi_plays()

    def ordi_plays(self):
        """Fait jouer l'ordinateur."""
        hand = self.hands[self.num_player]
        name = "Joueur " + chr(ord('A') + self.num_player)
        play = "Joue {} sur la ligne {} en position {}"
        drop = "Jette le {}"
        ordi = OrdiRandom(self.proof, hand)
        coup = ordi.joue()
        for (i_hand, num_premise, index_premise) in coup:
            card = hand.pop(i_hand)
            if index_premise == -1:
                messagebox.showinfo(name, drop.format(card))
            else:
                self.proof.insert(num_premise, index_premise, card)
                self.can.affiche_cards("premise",
                                       self.proof.premises[num_premise],
                                       num_premise)
                messagebox.showinfo(name,
                                    play.format(card,
                                                num_premise,
                                                index_premise))
        self.can.affiche_cards("hand", self.hands[self.num_player])
        self.play()

    def fin_manche(self):
        """Fin de la manche, affichage des gagnants et du score."""
        # TODO faire plus propre
        prouve = self.demoFB.conclusion()
        if prouve is None:
            msg = "La preuve contient une contradiction,\
                    personne ne marque de point"
        else:
            score = self.proof.score()
            msg = "Le(s) gagnant(s) est(sont) : "
            for index, val in enumerate(prouve):
                if val:
                    msg += chr(ord('A')+index) + " "
                    self.scores[index] += score
                msg += "\n"
            msg += "\nChacun marque {} points".format(score)
        messagebox.showinfo("Fin de la manche", msg)
        self.init_round()

    def version(self):
        """Affiche la version du jeu"""
        messagebox.showinfo("Ergo", "Version Beta 17/03/19")

    def rules(self):
        """Affiche les règles du jeu à partir du fichier regles_ergo.txt"""
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
