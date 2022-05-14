import tkinter as tk
from tkinter import *
from threading import Thread
import time


class EcranChargement(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.posx = 0
        self.posy = 0

        self.resizable(width=False,height=False)
        self.title("Connexion en cours...")
        self.canva = Canvas(self, width=500, height=200, bg="ivory")
        self.canva.configure()

        self.canva.grid()
        self.fin = False

    def start(self,photo):
        print("zizi")
        while not self.fin:
            for i in range(5):
                print(i)
                time.sleep(1)
                self.posx = self.posx+1
            self.fin=True


    def finChargement(self):
        self.fin = True

def start(photo):
    ecranChargement = EcranChargement()
    ecranChargement.canva.create_image(ecranChargement.posx, ecranChargement.posy, image=photo)
    print("oui")
    ecranChargement.start(photo)