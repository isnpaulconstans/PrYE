#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
import constantes as cst
from cards import Card, CardList


class ErgoGui(tk.Tk):
    """Interface graphique.
    TODO
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ergo")
        self.can = tk.Canvas(self, height=cst.HEIGHT, width=cst.WIDTH,
                             bg=cst.CARPET_COLOR)
        for i in range(4):
            self.can.create_line(0, i*cst.CARD_HEIGHT, cst.WIDTH,
                                 i*cst.CARD_HEIGHT, fill="black")
        self.can.create_rectangle(0, cst.HEIGHT-cst.CARD_HEIGHT-5,
                                  cst.WIDTH, cst.HEIGHT,
                                  width=5, outline="red")
        self.can.pack()
        # TEST
        self.can.bind('<Button1-Motion>', func=self.move)
        card_then = Card("THEN")
        self.im = tk.PhotoImage(file=card_then.image)
        self.card = self.can.create_image(cst.CARD_WIDTH//2, cst.CARD_HEIGHT//2,
                                          image=self.im)

    def move(self, event):
        """TEST : déplace la carte."""
        self.can.coords(self.card, event.x, event.y)


if __name__ == '__main__':
    ergoGui = ErgoGui()
    ergoGui.mainloop()
