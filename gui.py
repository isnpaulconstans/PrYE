import tkinter as tk
from constantes import *

class Card(object):
    def __init__(self, image):
        self.image=tk.PhotoImage(file=image)


class ErgoGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ergo")
        self.can = tk.Canvas(self, height=HEIGHT, width=WIDTH, bg=CARPET_COLOR)
        self.cardThen = Card(CARD_A)
        self.card = self.can.create_image(CARD_WIDTH//2, CARD_HEIGHT//2,
                                          image=self.cardThen.image)
        for i in range(4):
            self.can.create_line(0, i*CARD_HEIGHT, WIDTH, i*CARD_HEIGHT,
                                 fill="black")
        self.can.create_rectangle(0, HEIGHT-CARD_HEIGHT-5, WIDTH, HEIGHT,
                                  width=5, outline="red")
        self.can.pack()
        self.can.bind('<Button1-Motion>', func=self.move)

    def move(self, event):
        self.can.coords(self.card, event.x, event.y)

if __name__ == '__main__':
    ergoGui = ErgoGui()
    ergoGui.mainloop()


