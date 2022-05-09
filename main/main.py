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
        self.iconbitmap('../img/logo.ico')
        self.grid()

        '''     CREATION DES 2 BLOCS PRINCIPAUX    '''

        self.canvas = Canvas(self, background='ivory')
        self.barreControle = Frame(self, background='grey')

        '''     INITIALISATION DE LA CASE ETAT DE LA BARRE DE CONTROLE      '''
        self.caseEtat = Frame(self.barreControle, background="cyan")

        '''     INITIALISATION DES BOUTONS DE LA BARRE DE CONTROLE     '''
        self.boutonStart = Button(self.barreControle, text="Start Scanning", fg="green", command=self.alert)
        self.boutonPause = Button(self.barreControle, text="Pause Scanning", fg="orange", command=self.alert)
        self.boutonStop = Button(self.barreControle, text="Stop Scanning", fg="red", command=self.alert)
        self.boutonManuel = Button(self.barreControle, text="Mode Manuel", command=self.alert, state=DISABLED)
        self.boutonAvancer = Button(self.barreControle, text="Avancer", command=self.alert, state=DISABLED)
        self.boutonDroite = Button(self.barreControle, text="Tourner à droite", command=self.alert, state=DISABLED)
        self.boutonGauche = Button(self.barreControle, text="Tourner à gauche", command=self.alert, state=DISABLED)

        '''     INITIALISATION DES ZONES DE TEXTES DE LA BARRE DE CONTROLE    '''
        self.labelTempsRun = Label(self.barreControle, text="Time : 00.00.00")
        self.labelCommandeAutomatique = Label(self.barreControle, text="Commande Automatique", fg="black", bg="gray")
        self.labelCommandeManuelle = Label(self.barreControle, text="Commande Manuelle", fg="black", bg="gray")

        '''     PLACEMENT DES ELEMENTS SUR LA FENETRE    '''
        self.boutonStart.grid(row=1, column=0,padx=20,pady=5,sticky='N')
        self.boutonPause.grid(row=1, column=1,padx=20,pady=5,sticky='N')
        self.boutonStop.grid(row=1, column=2,padx=20,pady=5,sticky='N')
        self.boutonManuel.grid(row=3,column=0, pady=5,sticky='N')
        self.boutonAvancer.grid(row=3, column=1, pady=5, sticky='N')
        self.boutonGauche.grid(row=3, column=2, pady=5, sticky='N')
        self.boutonDroite.grid(row=3, column=3, pady=5, sticky='N')

        self.labelTempsRun.grid(row=1, column=3, padx=20, pady=5, sticky='N')
        self.caseEtat.grid(row=0, column=4, rowspan=4, padx=20, pady=5, sticky='NEWS')
        self.labelCommandeAutomatique.grid(row=0, column=0, columnspan=4, sticky='S')
        self.labelCommandeManuelle.grid(row=2, column=0, columnspan=4, sticky='S')

        self.canvas.grid(row=0, sticky='NEWS')
        self.barreControle.grid(row=1, sticky='NEWS')

        '''      CONFIGURATION DES LIGNES & COLONES DE LA FENETRE DE BASE      '''
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        '''      CONFIGURATION DES LIGNES & COLONES DE LA BARRE DE CONTROLE      '''
        self.barreControle.grid_columnconfigure(4, weight=4)
        self.barreControle.grid_columnconfigure(3, weight=1)
        self.barreControle.grid_columnconfigure(2, weight=1)
        self.barreControle.grid_columnconfigure(1, weight=1)
        self.barreControle.grid_columnconfigure(0, weight=1)
        self.barreControle.grid_rowconfigure(0, weight=1)
        self.barreControle.grid_rowconfigure(1, weight=1)
        self.barreControle.grid_rowconfigure(2, weight=1)
        self.barreControle.grid_rowconfigure(3, weight=1)

        '''      CREATION & INITIALISATION DU MENU     '''
        self.menuBar = Menu(self)
        self.initialisationMenu()

    def alert(self):
        showinfo("alerte", "Bravo!")

    def initialisationMenu(self):
        menuFile = Menu(self.menuBar, tearoff=0)
        menuFile.add_command(label="New", command=self.alert)
        menuFile.add_command(label="Open", command=self.alert)
        menuFile.add_command(label="Change Config", command=self.alert)
        menuFile.add_separator()
        menuFile.add_command(label="Quitter", command=self.quit)

        menuEdit = Menu(self.menuBar, tearoff=0)
        menuEdit.add_command(label="Mode Automatique", command=self.alert)
        menuEdit.add_command(label="Mode Manuel", command=self.alert)
        menuEdit.add_separator()
        menuEdit.add_command(label="Paramètres Robot", command=self.alert)

        menuScan = Menu(self.menuBar, tearoff=0)
        menuScan.add_command(label="Run", command=self.alert)
        menuScan.add_command(label="Stop", command=self.alert)
        menuScan.add_command(label="Pause", command=self.alert)
        menuScan.add_separator()
        menuScan.add_command(label="Export Room", command=self.alert)

        self.menuBar.add_cascade(label="  Window  ", menu=menuFile)
        self.menuBar.add_cascade(label="  Edit  ", menu=menuEdit)
        self.menuBar.add_cascade(label="  Scan  ", menu=menuScan)

        self.config(menu=self.menuBar, bg='black')


if __name__ == "__main__":
    app = Application()
    app.title("Rammus Scanning")
    imgStart = PhotoImage(file="../img/appContent/start.png").subsample(20, 20)
    imgStop = PhotoImage(file="../img/appContent/stop.png").subsample(8, 8)
    imgPause = PhotoImage(file="../img/appContent/pause.png").subsample(38, 38)
    app.mainloop()
