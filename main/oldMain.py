from tkinter.messagebox import showinfo

import serial  # Importation de la bibliothèque « pySerial »
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
        # self.resizable(width=False, height=False)
        self.iconbitmap('../img/logo.ico')

        self.canvas = Canvas(self, width=1000, height=500, background='ivory')
        self.barreParametre = Frame(height=720, width=200, bg='grey', )
        self.barreControle = Frame(height=220, width=1000, background='grey')

        self.menuBar = Menu(self)

        self.initialisationMenu()
        self.initialisationDesWidgets()

    def initialisationDesWidgets(self):
        self.barreParametre.grid(row=0, column=1, sticky='e', rowspan=2)
        self.canvas.grid(row=0, column=0, sticky='n')
        self.barreControle.grid(row=1, column=0, sticky='n')

        """ 
        -----  POUR PLUS TARD (Redimensionnement dynamique) ----- 

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        """

    def initialisationMenu(self):
        menuFile = Menu(self.menuBar, tearoff=0)
        menuFile.add_command(label="New", command=self.alert)
        menuFile.add_command(label="Open", command=self.alert)
        menuFile.add_command(label="Save Config", command=self.alert)
        menuFile.add_separator()
        menuFile.add_command(label="Quitter", command=self.quit)

        menuEdit = Menu(self.menuBar, tearoff=0)
        menuEdit.add_command(label="Mode Automatique", command=self.alert)
        menuEdit.add_command(label="Mode Manuel", command=self.alert)

        menuScan = Menu(self.menuBar, tearoff=0)
        menuScan.add_command(label="Run", command=self.alert)
        menuScan.add_command(label="Stop", command=self.alert)
        menuScan.add_command(label="Export Room", command=self.alert)

        self.menuBar.add_cascade(label="Fichier", menu=menuFile)
        self.menuBar.add_cascade(label="Edit", menu=menuEdit)
        self.menuBar.add_cascade(label="Scan", menu=menuScan)

        self.config(menu=self.menuBar, bg='black')

    def ouvrirParam(self):
        self.canvas["width"] = 200

    def alert(self):
        showinfo("alerte", "Bravo!")

    def initalisationBarreControle(self):
        Button(self.barreControle, text=" Start Scanning", command=self.alert, image=imgStart, compound=LEFT).grid(
            row=0, column=0)
        Button(self.barreControle, text=" Pause Scanning", command=self.alert, image=imgPause, compound=LEFT).grid(
            row=0, column=1)
        Button(self.barreControle, text=" Stop Scanning", command=self.alert, image=imgStop, compound=LEFT).grid(row=0,
                                                                                                                 column=2)
        ConteneurInfos = Frame(self.barreControle, background="Black", height=180, width=1000)
        ConteneurInfos.grid(row=1, column=0, columnspan=3)

        Button(ConteneurInfos, text="ask for manual control", command=self.alert).grid(row=0, column=0)


if __name__ == "__main__":
    app = Application()
    app.title("Rammus Scanning")
    imgStart = PhotoImage(file="../img/appContent/start.png").subsample(20, 20)
    imgStop = PhotoImage(file="../img/appContent/stop.png").subsample(8, 8)
    imgPause = PhotoImage(file="../img/appContent/pause.png").subsample(38, 38)
    app.initalisationBarreControle()
    app.mainloop()
