#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Programme principal."""

import tkinter as tk
from tkinter import messagebox
import webbrowser
from sys import platform
from ErgoIntro import ErgoIntro
from Card import Card
from Deck import Deck
from ErgoCanvas import ErgoCanvas
from Proof import Proof
from DPLL import DPLL as Demo
#from OrdiRandom import OrdiRandom as Ordi
from OrdiScore import OrdiScore as Ordi


class Main(tk.Tk):
    """Programme principal."""
    def __init__(self):
        """Constructeur de la classe

        :return: Objet Main
        :rtype: Main
        """
        tk.Tk.__init__(self)
        self.title("Ergo")
        self.resizable(width=False, height=False)
        if platform == "linux":
            self.iconbitmap("@images/carteBack.icon")
        else:
            self.iconbitmap(default="images/carteBack.ico")
        self.__init_menu__()
        self.nb_player = 4
        self.scores = [0] * 4
        self.player_names = ["Joueur "+chr(ord('A')+i) for i in range(4)]
        self.num_player = 3  # sera incrémenté de 1 par init_round
        self.can = ErgoCanvas(self)
        self.can.grid(row=0, column=1, rowspan=7)
        for i in range(4):
            tk.Label(text="Prémisse "+str(i+1)).grid(row=i, column=2)
        tk.Label(text="Ergo le jeu", font="Arial 16 italic").grid(row=0,
                                                                  column=0)
        tk.Label(text="Prouve que tu existes ...",
                 font="Arial 28 italic").grid(row=7, column=1)
        tk.Button(text="jouer", command=self.play).grid(row=5, column=0)
        ErgoIntro()

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

    def start(self, nb_player, cheat):
        """Lance une partie

        :param nbplayer: le nombre de joueurs humains
        :type nbplayer: int
        :param cheat: indique si le cheatmode (affichage des varibale prouvées)
                      est activé
        :type cheat: bool
        """
        self.nb_player = nb_player
        for num_player in range(nb_player, 4):
            self.player_names[num_player] = "Ordi "+chr(ord('A')+num_player)
        if cheat:
            tk.Button(text="cheat", command=self.cheat).grid(row=6, column=0)
        self.init_round()

    def init_round(self):
        """Inialise un début de tour."""
        self.deck = Deck()
        self.can.reset()
        self.proof = Proof()
        self.demo = Demo(self.proof)
        self.num_player = (self.num_player + 1) % 4
        self.fallacy = [0] * 4
        self.can.display_current_player(self.num_player)
        self.ordi_player = [False]*self.nb_player + [True]*(4-self.nb_player)
        self.hands = [self.deck.draw(5) for _ in range(4)]
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.cards_played = 0
        self.can.display_cards("hand", self.hands[self.num_player])
        if self.ordi_player[self.num_player]:
            self.can.reset_bind()
            self.ordi_plays()
        else:
            self.can.init_bind()

    def play(self):
        """Valide un coup si possible."""
        if self.cards_played != 2:
            messagebox.showwarning("Ergo",
                                   "Il faut jouer 2 cartes pour valider.")
            return
        if not self.proof.is_all_correct():
            messagebox.showwarning("Ergo", "Jeu invalide")
            return
        self.next_player()

    def cheat(self):
        """Affiche les noms des joueurs prouvés."""
        prouve = self.demo.conclusion()
        if prouve is None:
            msg = "La preuve contient une contradiction"
        else:
            msg = ""
            for index, val in enumerate(prouve):
                if val:
                    msg += self.player_names[index] + " "
        tk.messagebox.showinfo("cheat", msg)

    def next_player(self):
        """Passe au joueur suivant."""
        if self.deck.is_finished():
            self.fin_manche()
            return
        self.proof.reset_added()
        self.cards_played = 0
        self.unbind("<Escape>")
        self.can.delete("pile")
        if self.fallacy[self.num_player] > 0:
            self.fallacy[self.num_player] -= 1
        self.num_player = (self.num_player + 1) % 4
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.can.display_cards("hand", self.hands[self.num_player])
        self.can.display_current_player(self.num_player)
        if self.ordi_player[self.num_player]:
            self.can.reset_bind()
            self.ordi_plays()
        else:
            self.can.init_bind()

    def ordi_plays(self):
        """Fait jouer l'ordinateur."""
        ordi = Ordi(self.proof, self.hands[self.num_player],
                    self.num_player, self.scores, self.fallacy)
        msg, special_cards = ordi.joue(self.player_names)
        ergo_played = False
        for special in special_cards:
            if special == "Ergo":
                ergo_played = True
            elif special == "Justification":
                self.fallacy[self.num_player] = 0
            else:  # special == ("Fallacy", num_player)
                num_other = special[1]
                self.fallacy[num_other] = 3
        for num_premise in range(4):
            cards = self.proof.premises[num_premise]
            if ergo_played and num_premise == 3:
                cards = cards + [Card("Ergo")]
            self.can.display_cards("premise", cards, num_premise)
        self.can.display_current_player(self.num_player)
        self.can.display_cards("hand", self.hands[self.num_player])
        messagebox.showinfo(self.player_names[self.num_player], msg)
        if ergo_played:
            self.fin_manche()
        else:
            self.next_player()

    def fin_manche(self):
        """Fin de la manche, affichage des gagnants et du score."""
        provens = self.demo.conclusion()
        if provens is None:
            msg = "La preuve contient une contradiction,\
                    personne ne marque de point"
        else:
            score = self.proof.score()
            winers = ""
            for index, proven in enumerate(provens):
                if proven:
                    winers += self.player_names[index] + " "
                    self.scores[index] += score
            if winers:
                msg = winers + "\nBravo, vous marquez {} points".format(score)
            else:
                msg = "Personne n'est prouvé, personne ne marque de point"
        self.can.display_current_player(self.num_player)
        messagebox.showinfo("Fin de la manche", msg)
        score_max = max(self.scores)
        if score_max >= 50:
            self.fin_partie(score_max)
        else:
            self.init_round()

    def fin_partie(self, score_max):
        """Affiche le nom des gagnants et ferme la fenêtre.

        :param score_max: le score du ou des gagnant(s)
        :type score_max: int
        """
        winers = ""
        for index, score in enumerate(self.scores):
            if score == score_max:
                winers += self.player_names[index] + " "
        msg = winers + "\nBravo, vous avez gagné !"
        messagebox.showinfo("Fin de la partie", msg)
        self.quitter()

    def version(self):
        """Affiche la version du jeu"""
        messagebox.showinfo("Ergo", "Version finale 31/05/19")

    def rules(self):
        """Affiche les règles du jeu dans le navigateur wenb par défaut."""
        webbrowser.open("regles_ergo.html")

    def quitter(self):
        """Quitte"""
        self.quit()
        self.destroy()


if __name__ == '__main__':
    Main().mainloop()
