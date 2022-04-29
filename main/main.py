import tkinter as tk
from tkinter import *


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1200x720")
        self.creer_widgets()

    def creer_widgets(self):
        self.titleToScreen = tk.Label(self, text="RAMMUS", justify=CENTER, pady=100, font=("Helvetica", 50))
        self.bouton = tk.Button(self, text="Quitter", command=self.quit)
        self.titleToScreen.pack()
        self.bouton.pack()


if __name__ == "__main__":
    app = Application()
    app.title("Rammus Scanning")
    app.mainloop()
