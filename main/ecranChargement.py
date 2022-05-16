import tkinter as tk
from tkinter import *
from threading import Thread
import time

CONTINUE = True

class EcranChargement(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.posx = -80
        self.posy = 100

        self.grab_set()

        self.resizable(width=False,height=False)
        self.title("Connexion en cours...")
        self.canva = Canvas(self, width=500, height=200, bg="ivory")
        self.canva.configure()

        self.canva.grid()

    def start(self,photo):
        while CONTINUE:
            self.posx = self.posx+2
            time.sleep(0.001)
            self.canva.create_image(self.posx, self.posy, image=photo)
            if self.posx == 600:
                self.posx=0
        self.destroy()


    def finChargement(self):
        self.fin = True

def start(photo):
    ecranChargement = EcranChargement()
    ecranChargement.canva.create_image(ecranChargement.posx, ecranChargement.posy, image=photo)
    ecranChargement.start(photo)

