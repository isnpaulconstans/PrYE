#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
import random as rd
import constantes as cst
from cards import Card, CardList



class ErgoGui(tk.Tk):
    """Interface graphique.
    TODO
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ergo")
        self.geometry("1200x800") #dimension fenetre jeu
        self.grillePremice = [[-1]*7 for _ in range(4)] #grille pour chaque ligne
        self.grilleHand = [-1 for _ in range(5)] #cartes du joueur
        self.listCard = ["A","A","A","A","B","B","B","B","C","C","C","C","D",
                        "D","D","D","AND","AND","AND","AND","OR","OR","OR",
                        "OR","THEN","THEN","THEN","THEN","NOT","NOT","NOT",
                        "NOT","NOT","NOT","(","(","(","(","(","(","(","(",
                        "CQFD","CQFD","CQFD"]
        self.can = tk.Canvas(self, height=cst.HEIGHT, width=cst.WIDTH,
                             bg=cst.CARPET_COLOR)
        for i in range(4):
            self.can.create_line(0, i*cst.CARD_HEIGHT, cst.WIDTH,
                                 i*cst.CARD_HEIGHT, fill="black")
        for i in range(10):
            self.can.create_line(i*cst.CARD_WIDTH,0,i*cst.CARD_WIDTH,
                                4*cst.CARD_HEIGHT, fill="red",dash=(4,4))
        self.can.create_rectangle(0, cst.HEIGHT-cst.CARD_HEIGHT-5,
                                  cst.WIDTH, cst.HEIGHT,
                                  width=5, outline="red")
        self.can.create_line(cst.WIDTH-100,cst.HEIGHT-cst.CARD_HEIGHT-5,
                            cst.WIDTH-100,cst.HEIGHT, width=5, fill="red")
        self.can.create_text(50,4*CARD_HEIGHT +50 , text="Joueur",
                            font="Arial 16 italic", fill="blue")
        self.can.create_text(9*CARD_WIDTH+50,4*CARD_HEIGHT +50 , text="Pile",
                            font="Arial 16 italic", fill="blue")
        for i in range(4):
            tk.Label(text="Premice"+str(i+1)).grid(row=i+1,column=2)
        self.can.grid(row=1,column=1,rowspan=5)
        self.name = tk.Label(text="Ergo le jeu",
                            font="Arial 16 italic")
        self.name.grid(row=1,column=0)
        self.ButPlay = tk.Button(text="play",command=self.play)
        self.ButPlay.grid(row=5,column=0)
        # TEST
        self.can.bind('<Button1-Motion>', func=self.move)
        # Creation de toutes les images de cartes
##        card_then = Card("THEN")
##        self.im = tk.PhotoImage(file=card_then.image)
##        self.card = self.can.create_image(cst.CARD_WIDTH//2, cst.CARD_HEIGHT//2,
##                                          image=self.im)

##    def afficheCard(self, ref):
##            """affiche dans le canvas en bas la main du joueur"""
##            card1 = Card(ref)
##            self.im1 = tk.PhotoImage(file=card1.image)
##            self.cardP1 = self.can.create_image(cst.CARD_WIDTH+cst.CARD_WIDTH//2,
##                                        cst.CARD_HEIGHT//2+570, image=self.im1)
##
##
##
    def play(self):
        """lance le jeu en melangeant le jeu de carte et en distribuant
        5 cartes au joueur """
        rd.shuffle(self.listCard)
        if self.listCard != []:
            for i in range(5):
                self.grilleHand[i]=self.listCard[0]
                self.listCard.pop(0)
        self.afficheCard()

    def afficheCard(self):
        """affiche dans le canvas en bas la main du joueur"""
        card1 = Card(self.grilleHand[0])
        self.im1 = tk.PhotoImage(file=card1.image)
        self.cardP1 = self.can.create_image(cst.CARD_WIDTH+cst.CARD_WIDTH//2,
                                    cst.CARD_HEIGHT//2+570, image=card1.image)
        card2 = Card(self.grilleHand[1])
        self.im2 = tk.PhotoImage(file=card2.image)
        self.cardP2 = self.can.create_image(2*cst.CARD_WIDTH+cst.CARD_WIDTH//2,
                                    cst.CARD_HEIGHT//2+570, image=self.im2)


    def place(self, event):
        """TEST place la carte sur un premice si possible
        Renvoie True si ok, False sinon."""
        pass

    def switch(self):
        """TEST retourne la parenthèse"""
        pass


    def move(self, event):
        """TEST : déplace la carte."""
        self.can.coords(self.cardP1, event.x, event.y)


if __name__ == '__main__':
    ergoGui = ErgoGui()
    ergoGui.mainloop()
