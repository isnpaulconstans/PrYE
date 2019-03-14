#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
from tkinter import messagebox
from cards import Proof, Deck
from demonstration import ForceBrute, DPLL, FCN
from ordi import OrdiRandom

#ess
# Constantes
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

# definition du chemin des lettres de l'animation
letWay = [(1,15),(1,14),(1,13),(2,13),(3,13),(4,13),(5,13),(5,14),(5,15),
          (4,15),(3,15),(2,15),
        (1,11),(1,10),(1,9),(2,9),(3,9),(4,9),(5,9),(5,10),(5,11),(4,11),
        (3,11),
        (5,5),(4,5),(3,5),(2,5),(1,5),(1,6),(1,7),(2,7),(3,7),(4,6),(5,7),
        (1,3),(1,2),(1,1),(2,1),(3,1),(3,2),(4,1),(5,1),(5,2),(5,3)]

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
        self.animate_letter(len(letWay),  letWay)

    def __init_intro__(self):
        """ Creation de la fenetre d'animation """
        self.canIntro = tk.Canvas(self, height=500, width=850,
                                  bg="skyblue")
        self.canIntro.grid()
        self.img = tk.PhotoImage(file="images/carteDos.gif")
        self.idImg = self.canIntro.create_image(425,465,image=self.img)

    def rectangle(self,x,y):
        """ création d'un rectangle trace du passage de la carte """
        self.canIntro.create_rectangle(x,y,x+50,y+70, fill="ivory")

    def animate_letter(self, nbCarte, lWay):
        """ deplace la carte sur le canvas en suivant un chemin defini ,
        de façon récursive et laisse la trace du parcours

        :param nbCarte: nombre de cartes à afficher
        :type nbCarte: int

        :param lWay: le chemin à suivre par la carte Ergo
        :type lWay: list
        """
        if self.flag != 1:
            return
        if nbCarte == 0:
            self.flag = 0
            return
        self.canIntro.coords(self.idImg,CARD_WIDTH*(lWay[nbCarte-1][1]+1)
                -CARD_WIDTH/2,CARD_HEIGHT*lWay[nbCarte-1][0]+CARD_HEIGHT/2)
        self.rectangle(50*lWay[nbCarte-1][1],70*lWay[nbCarte-1][0])
        self.canIntro.tag_raise(self.idImg)
        self.after(self.pause,lambda :self.animate_letter(nbCarte-1,lWay))

    def button_choice(self):
        """ Creation des boutons de choix du mode de jeu """
        self.but_play_against_pc = tk.Button(self,text="Mode seul", bd=7,
                                             font="Arial 16",
                    command = lambda : self.animate_letter(len(letWay),letWay))
        self.but_play_against_pc.grid()
        self.but_play_multiplayers = tk.Button(self,text="Mode multijoueurs",
                                               bd=7, font="Arial 16",
                                               command=self.choice)
        self.but_play_multiplayers.grid()

    def choice(self):
        """ Ouverture de la fenetre de jeu """
        self.master.deb_partie(4)
        self.destroy()
#        global ergoGui
#        ergoGui = ErgoGui()
#        ergoGui.mainloop()



class ErgoGui(tk.Tk):
    """Interface graphique."""
    def __init__(self):
        """Constructeur de la classe

        :return: Objet ErgoGui
        :rtype: ErgoGui
        """
        tk.Tk.__init__(self)
        ess = ErgoGuiIntro()
        self.title("Ergo")
        self.geometry("1200x500")  # dimension fenetre jeu
        self.resizable(width=False, height=False)

        self.proof = Proof()
        self.deck = Deck()
        self.demoDPLL = DPLL(self.proof)
        self.demoFB = ForceBrute(self.proof)
        self.photos = {name: tk.PhotoImage(file='images/'+IMAGE[name])
                       for name in IMAGE}
        self.cards = [[] for _ in range(5)]  # les 5 lignes de cartes
        # initialisation du menu et canvas
        self.__init_menu__()
        self.__init_canvas__()

    def deb_partie(self, nb_player):

        self.num_player = 0
        self.nb_player = 4
        self.hands = [self.deck.draw(5) for _ in range(4)]
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.pile = []
        self.selected_card = None
        self.cards_played = 0
        self.affiche_cards(self.hands[self.num_player], 4)

        self.name = tk.Label(text="Ergo le jeu", font="Arial 16 italic")
        self.name.grid(row=1, column=0)
        self.slogan = tk.Label(text="Prouve que tu existes ...",
                               font="Arial 28 italic")
        self.slogan.grid(row=6, column=1)
        self.but_play = tk.Button(text="jouer", command=self.play)
        self.but_play.grid(row=5, column=0)
        # liens bouttons souris
        self.can.bind('<Button-1>', func=self.select)
        self.can.bind('<Button1-Motion>', func=self.move)
        self.can.bind("<ButtonRelease-1>", func=self.drop)
        self.can.bind("<Button-3>", func=self.switch)
        # TODO creer une méthode init_round
        # TODO gérer les scores
        # TODO créer une classe ErgoCanvas et y mettre tous le canvas

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

    def __init_canvas__(self):
        """Création du canvas de jeu avec les lignes des prémisses, les mains
        et noms des joueurs et la pile"""
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
        self.can.create_rectangle(WIDTH-2*CARD_WIDTH+5,
                                  HEIGHT-2*CARD_HEIGHT-15,
                                  WIDTH, HEIGHT,
                                  width=5, outline="pink")
        self.can.create_text(18*CARD_WIDTH+50, 4*CARD_HEIGHT+50,
                             text="Pile", font="Arial 16 italic", fill="blue")
        # les lignes des prémisses
        for i in range(4):
            tk.Label(text="Prémisse "+str(i+1)).grid(row=i+1, column=2)
        self.can.grid(row=1, column=1, rowspan=5)
        # le dos de cartes
        for (row, col) in [(0, 11), (1, 2), (1, 11)]:
            xdeb = col * CARD_WIDTH + CARD_WIDTH // 2
            y = 4 * (CARD_HEIGHT+2) + (CARD_HEIGHT + 10) * row + CARD_HEIGHT//2
            for index in range(5):
                x = xdeb + index * CARD_WIDTH
                self.can.create_image(x, y, image=self.photos["Back"])
        # les noms des joueurs
        self.names = [self.can.create_text(CARD_WIDTH*(1 + 9 * (i % 2)),
                                           (4 + i // 2) * CARD_HEIGHT + 50,
                                           text="Joueur " + "ABCD"[i],
                                           font="Arial 16 italic",
                                           fill="blue")
                      for i in range(4)]

    def display_current_player(self):
        """ Affiche les numéros de joueurs en faisant tourner, le joueur
        courant est toujours en haut à gauche. """
        for i, player in enumerate(self.names):
            self.can.itemconfig(player, text="Joueur " +
                                "ABCD"[(self.num_player+i) % (self.nb_player)])

    def play(self):
        """Valide un coup si possible, et passe au joueur suivant"""
        if len(self.hands[self.num_player]) != 5:
            messagebox.showwarning("Ergo",
                                   "Il faut garder 5 cartes pour valider.")
            return
        if not self.proof.is_all_correct():
            messagebox.showwarning("Ergo", "Jeu invalide")
            return
        # TEST
#        print(self.demo._proof.premises, self.demo._proof.npi, self.demo._proof.modif)
        print(self.demoDPLL.conclusion(), "|=", self.demoFB.conclusion())
#        print(self.demoDPLL._DPLL__clause_list, "|=", self.demoFB.conclusion())
        # passe au joueur suivant.
        if self.deck.is_finished():
            self.fin_manche()
        self.proof.reset_added()
        self.cards_played = 0
        self.can.delete("pile")
        self.num_player = (self.num_player + 1) % self.nb_player
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.affiche_cards(self.hands[self.num_player], 4)
        self.display_current_player()
        if self.num_player != 0:
            self.ordi_plays()

    def ordi_plays(self):
        hand = self.hands[self.num_player]
        ordi = OrdiRandom(self.proof, hand)
        coup = ordi.joue()
        (index_hand1, num_premise1, index_premise1,
         index_hand2, num_premise2, index_premise2) = coup
        messagebox.showinfo("Joueur "+chr(ord('A')+self.num_player),
                            "{} sur {} en position {}".format(hand[index_hand1],
                                                              num_premise1,
                                                              index_premise1))
        messagebox.showinfo("Joueur "+chr(ord('A')+self.num_player),
                            "{} sur {} en position {}".format(hand[index_hand2],
                                                              num_premise2,
                                                              index_premise2))
        card1 = hand.pop(index_hand1)
        if index_hand1<index_hand2:
            index_hand2 -= 1
        card2 = hand.pop(index_hand2)
        if index_premise1 >= 0:
            self.proof.insert(num_premise1, index_premise1, card1)
            self.affiche_cards(self.proof.premises[num_premise1], num_premise1)
        if index_premise2 >= 0:
            self.proof.insert(num_premise2, index_premise2, card2)
            self.affiche_cards(self.proof.premises[num_premise2], num_premise2)
        self.affiche_cards(self.hands[self.num_player], 4)
        messagebox.askyesno("ca marche ?")
        self.play()

    def affiche_cards(self, card_list, row):
        """affiche la liste de carte card_list à la ligne row (0 à 3 pour les
        prémisses, 4 pour la main du joueur

        :param card_list: la liste de cartes à afficher
        :type card_list: list

        :param row: le numéro de la ligne
        :type row: int
        """
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

        :param event: événement
        :type event: tkinter.Event
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
                if self.cards_played == 2:
                    messagebox.showwarning("2 cartes", "On ne peut pas jouer "
                                           + "plus de deux cartes")
                    self.can.dtag("selected")
                    return
                self.selected_card = self.hands[self.num_player].pop(col)
                self.affiche_cards(self.hands[self.num_player], 4)
                self.cards_played += 1
            self.can.tag_raise(num)  # pour passer en avant plan

    def move(self, event):
        """Déplace la carte marquée "selected".

        :param event: événement
        :type event: tkinter.Event
        """
        num = self.can.find_withtag("selected")
        self.can.coords(num, event.x, event.y)

    def drop(self, event):
        """Place la carte marquée "selected" sur la grille, et l'ajoute au bon
        endroit (prémisse, main ou pile) et enlève la marque "selected".
        Si c'est impossible, la remet à la fin de la main.

        :param event: événement
        :type event: tkinter.Event
        """
        def restore():
            """remet la carte dans la main du joueur."""
            self.hands[self.num_player].append(self.selected_card)
            self.can.delete("selected")
            self.affiche_cards(self.hands[self.num_player], 4)
            self.selected_card = None
            self.cards_played -= 1

        if self.selected_card is None:
            return
        row, col = event.y//CARD_HEIGHT, event.x//CARD_WIDTH
        if 4 <= row <= 5 and 18 <= col <= 19:  # Pile
            self.can.coords("selected", WIDTH-CARD_WIDTH, HEIGHT-CARD_HEIGHT/2)
            self.pile.append(self.selected_card)
            self.can.addtag_withtag("pile", "selected")
            self.can.dtag("selected")
            self.selected_card = None
            return
        if not (0 <= event.x <= WIDTH and 0 <= row < 4):  # une des premisses
            restore()
            return
        if self.selected_card.is_ergo():
            if not self.proof.is_all_correct():
                messagebox.showwarning("Ergo", "Jeu invalide")
                restore()
                return
            if not self.proof.all_cards_played():
                messagebox.showwarning("Fin de manche", "Toutes les lettres " +
                                       "doivent apparaître pour pouvoir " +
                                       "mettre fin à la manche")
                restore()
                return
            self.affiche_cards(self.proof.premises[-1]+[self.selected_card], 3)
            self.can.delete("selected")
            self.selected_card = None
            self.fin_manche()
            return
        if self.proof.insert(row, col, self.selected_card):
            self.can.delete("selected")
            self.affiche_cards(self.proof.premises[row], row)
            self.selected_card = None
            return

    def switch(self, event):
        """Retourne la parenthèse si c'en est une, dans la main du joueur
        courant.

        :param event: événement
        :type event: tkinter.Event
        """
        num = self.can.find_closest(event.x, event.y)
        if "card" in self.can.gettags(num):
            row = event.y//CARD_HEIGHT
            col = event.x//CARD_WIDTH - 2
            if row == 4 and 0 <= col < len(self.hands[self.num_player]):
                card = self.hands[self.num_player][col]
                card.turn_parenthesis()
                self.affiche_cards(self.hands[self.num_player], 4)

    def fin_manche(self):
        """Fin de la manche, affichage des gagnants et du score."""
        # TODO faire plus propre
        msg = ""
        prouve = self.demoFB.conclusion()
        if prouve is None:
            msg += "La preuve contient une contradiction,\
                    personne ne marque de point"
        else:
            msg += "Le(s) gagnant(s) est(sont) : "
            for index, val in enumerate(prouve):
                if val:
                    msg += chr(ord('A')+index) + " "
                msg += "\n"
            msg += "\nChacun marque {} points".format(self.proof.score())
        messagebox.showinfo("Fin de la manche", msg)

    def version(self):
        """Affiche la version du jeu"""
        messagebox.showinfo("Ergo", "Version Alpha 21/01/19")

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
#    test = ErgoGuiIntro()
#    test.mainloop()
    ergoGui = ErgoGui()
    ergoGui.mainloop()
