import tkinter as tk

class ErgoGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ergo")

if __name__ == '__main__':
    ergoGui = ErgoGui()
    ergoGui.mainloop()

