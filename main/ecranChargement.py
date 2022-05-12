import tkinter as tk
from tkinter import *
from threading import Thread


class EcranChargement(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        window_h = 200
        window_w = 500

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x_coord = int((screen_w // 2) - (window_w // 2))
        y_coord = int((screen_h // 2) - (window_h // 2))

        self.geometry("{}x{}+{}+{}".format(window_w, window_h, x_coord, y_coord))

        self.resizable(width=False,height=False)

        self.tk.call('tk::PlaceWindow',self)

        self.title("Connexion en cours...")

        self.canva = Canvas(self, width=500, height=200, bg="ivory")
        self.canva.pack()
        self.fin = False


    def start(self):
        while not self.fin:
            print("oui")


    def finChargement(self):
        self.fin = True