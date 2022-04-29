import serial #Importation de la bibliothèque « pySerial »
import serial.tools.list_ports
import tkinter as tk
from tkinter import *


"""

def ouvrir_liaisonArduino(com_arduino):
    print("Recherche d'un port serie...")
    com_arduino = serial.Serial(Choix du port, Choix du debit, timeout=1)


def recpetionArduino(com_arduino, line):
    print("Lecture sur la liaison serie...")
    x = com_arduino.read()  # copie d’un caractere lu dans la variable « x »
    s = com_arduino.read(10)  # copie de 10 caracteres lu dans la variable « s »
    line = com_arduino.readline()  # copie d’une ligne entiere jusqu’a \n dans « line »


def emissionArduino(com_arduino, message):
    print("Ecriture sur la liaison serie...")
    com_arduino.write(message)


def fermer_liaisonArduino(com_arduino):
    print("Fermeture de la liaison serie...")
    com_arduino.close()  # Cloture du port pour le cas ou il serait déjà ouvert ailleurs

"""


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
