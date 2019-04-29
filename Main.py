#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
from tkinter import messagebox
from ErgoIntro import ErgoIntro
from Deck import Deck
from ErgoCanvas import ErgoCanvas
from Proof import Proof
from ForceBrute import ForceBrute
from DPLL import DPLL
from OrdiRandom import OrdiRandom


class Main(tk.Tk):
    """Interface graphique."""
    def __init__(self):
        """Constructeur de la classe

        :return: Objet Main
        :rtype: Main
        """
        tk.Tk.__init__(self)
        self.title("Ergo")
        self.resizable(width=False, height=False)
        self.nb_player = 1
        self.__init_menu__()
        self.scores = [0] * 4
        self.player_names = ["Joueur "+chr(ord('A')+i) for i in range(4)]
        self.num_player = 3
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

    def init_round(self):
        """Inialise un début de tour."""
        self.deck = Deck()
        self.can.reset()
        self.proof = Proof()
        self.demoDPLL = DPLL(self.proof)
        # XXX comparaison de DPLL et FB
        self.demoFB = ForceBrute(self.proof)
        self.num_player = (self.num_player + 1) % 4
        self.fallacy = [0] * 4
        self.can.display_current_player(self.num_player)
        self.ordi_player = [False]*self.nb_player + [True]*(4-self.nb_player)
        self.hands = [self.deck.draw(5) for _ in range(4)]
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.cards_played = 0
        self.can.display_cards("hand", self.hands[self.num_player])
        if self.ordi_player[self.num_player]:
            self.ordi_plays()

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
        """Valide un coup si possible."""
        if self.cards_played != 2:
            messagebox.showwarning("Ergo",
                                   "Il faut jouer 2 cartes pour valider.")
            return
#        if len(self.hands[self.num_player]) != 5:
#            messagebox.showwarning("Ergo",
#                                   "Il faut garder 5 cartes pour valider.")
#            return
        if not self.proof.is_all_correct():
            messagebox.showwarning("Ergo", "Jeu invalide")
            return
        self.next_player()

    def next_player(self):
        """Passe au joueur suivant."""
        if self.deck.is_finished():
            self.fin_manche()
            return
        # XXX comparaison FB DPLL
        print(self.demoDPLL.conclusion(), self.demoFB.conclusion())
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
            self.ordi_plays()

    def ordi_plays(self):
        """Fait jouer l'ordinateur."""
        ordi = OrdiRandom(self.proof, self.hands[self.num_player],
                          self.fallacy[self.num_player] > 0)
        msg, special_cards = ordi.joue(self.num_player, self.player_names)
        messagebox.showinfo(self.player_names[self.num_player], msg)
        for num_premise in range(4):
            self.can.display_cards("premise",
                                   self.proof.premises[num_premise],
                                   num_premise)
#        self.can.display_current_player(self.num_player)
        for special in special_cards:
            if special == "Ergo":
                self.fin_manche()
                return
            if special == "Justification":
                self.fallacy[self.num_player] = 0
            else:  # special == ("Fallacy", num_player)
                num_other = special[1]
                self.fallacy[num_other] = 3
        self.next_player()

    def fin_manche(self):
        """Fin de la manche, affichage des gagnants et du score."""
        prouve = self.demoDPLL.conclusion()
        if prouve is None:
            msg = "La preuve contient une contradiction,\
                    personne ne marque de point"
        else:
            score = self.proof.score()
            winers = ""
            for index, val in enumerate(prouve):
                if val:
                    winers += self.player_names[index] + " "
                    self.scores[index] += score
            msg = winers + f"\nBravo, vous marquez {score} points"
        self.can.display_current_player(self.num_player)
        messagebox.showinfo("Fin de la manche", msg)
        score_max = max(self.scores)
        if score_max >= 50:
            self.fin_partie(score_max)
        else:
            self.init_round()

    def fin_partie(self, score_max):
        """Fin de la partie, affichage des gagnants."""
        winers = ""
        for index, score in enumerate(self.scores):
            if score == score_max:
                winers += self.player_names[index] + " "
        msg = winers + "\nBravo, vous avez gagné !"
        messagebox.showinfo("Fin de la partie", msg)
        self.quit()
        self.destroy()

    def version(self):
        """Affiche la version du jeu"""
        messagebox.showinfo("Ergo", "Version PreProd 30/04/19")

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
    Main().mainloop()
