import time
from tkinter.messagebox import showinfo

import sys
import serial  # Importation de la bibliothèque « pySerial »
import serial.tools.list_ports
import tkinter as tk
from tkinter import *
from threading import Thread

import ecranChargement

SERIALPORT = 'COM4'
BAUDRATE = 9600
photo = None


def ouvrir_liaisonArduino(ser):
    print("Recherche d'un port serie au ", ser)
    com_arduino = serial.Serial(port=ser, baudrate=BAUDRATE, timeout=1)
    return com_arduino


def recpetionArduino(com_arduino):
    line = com_arduino.readline()  # copie d’une ligne entiere jusqu’a \n dans « line »
    return line


def emissionArduino(com_arduino, message):
    print("Env : ", message)
    com_arduino.write(str.encode(message))


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1200x720")
        self.iconbitmap('../img/logo.ico')
        self.grid()

        self.com, self.recept, self.thread, self.touche = None, None, None, '-1'
        self.affichageVertical = False
        self.modeAutomatique = True
        self.stop = True
        self.nouvelleTouche = True
        self.serialPortString = SERIALPORT
        self.coord_precedente_x = 0
        self.coord_precedente_y = 0
        self.coord_suivante_x = 0
        self.coord_suivante_y = 0

        '''     CREATION DES 2 BLOCS PRINCIPAUX    '''
        self.canvas = Canvas(self, background='ivory', borderwidth=0, highlightthickness=0)
        self.barreControle = Frame(self, background='grey')
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.clavier)
        self.canvas.bind("<KeyRelease>", self.resetTouche)

        '''     INITIALISATION DE LA CASE ETAT DE LA BARRE DE CONTROLE      '''
        self.caseEtat = Frame(self.barreControle, background="white")
        self.telecomande = Frame(self.barreControle, background="grey")

        '''     INITIALISATION DES BOUTONS DE LA TELECOMANDE     '''
        self.boutonStart = Button(self.telecomande, text="Démarrer", fg="green", command=self.startModeAutomatique)
        self.boutonPause = Button(self.telecomande, text="Mettre en Pause", fg="orange",
                                  command=self.pauseModeAutomatique, state=DISABLED)
        self.boutonStop = Button(self.telecomande, text="Stopper", fg="red", command=self.stopModeAutomatique,
                                 state=DISABLED)

        '''     INITIALISATION DES ZONES DE TEXTES DE LA BARRE DE CONTROLE    '''
        self.labelTempsRun = Label(self.telecomande, text="Temps : 00.00.00", background="gray")
        self.labelCommande = Label(self.telecomande, text="Commande Automatique", fg="black", bg="gray")
        self.labelManuel = Label(self.telecomande, text="Utilisez les flèches directionnelles pour contrôler le robot",
                                 fg="black", bg="gray")

        '''     INITIALISATION DES ZONES DE TEXTES DE LA CASE D'ETAT    '''
        self.labelEtatConnexion = Label(self.caseEtat, text="Etat de la connexion : déconnecté", bg="white")
        self.labelEtatScan = Label(self.caseEtat, text="Etat du scan : en attente", bg="white")
        self.labelPort = Label(self.caseEtat, text="Port Actuel : COM4", bg="white")
        self.labelFreqDenvoie = Label(self.caseEtat, text="Fréquence d'émission : 9600", bg="white")

        '''     PLACEMENT DES ELEMENTS SUR LA FENETRE    '''
        self.passageModeAuto()
        self.canvas.grid(row=0, column=0, sticky='NEWS')

        '''      CONFIGURATION DES LIGNES & COLONES DE LA BARRE DE CONTROLE      '''
        self.passageConfigHorizontale()

        '''      CREATION & INITIALISATION DU MENU     '''
        self.menuBar = Menu(self)
        self.initialisationMenu()

    def alert(self):
        showinfo("alerte", "Bravo!")

    def alertPerso(self, message):
        showinfo("alerte", message)

    def threadConnexion(self, fileMenu):
        try:
            self.com = ouvrir_liaisonArduino(self.serialPortString)
            self.thread = Thread(target=lambda: self.recupDonnee(fileMenu))
            self.thread.start()
            self.stop = False
            fileMenu.entryconfigure(1, label="Se déconnecter")
        except:
            time.sleep(5)
            print(sys.exc_info()[0])
            self.alertPerso(message="Impossible de se connecter")
        ecranChargement.CONTINUE = False

    def dessiner(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, width=" 5",
                                fill="black")

    def decodageTrame(self):
        print(self.recept)
        tab = str(self.recept).split("$")
        print(tab)
        self.coord_suivante_x = tab[1]
        self.coord_suivante_y = tab[2]

    def connexionRobot(self, fileMenu):
        if self.stop:
            ecranChargement.CONTINUE = True
            Thread(target=ecranChargement.start, args=(photo,)).start()
            Thread(target=self.threadConnexion, args=(fileMenu,)).start()
        else:
            self.stop = True
            fileMenu.entryconfigure(1, label="Se connecter")

    def recupDonnee(self, fileMenu):
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.clavier)
        self.touche = '4'
        self.labelEtatConnexion["text"] = "connecté"
        while not self.stop:
            try:
                self.recept = recpetionArduino(self.com)
                print(self.stop, " : ", self.recept, ", ", len(self.recept))
                if len(self.recept)>3:
                    self.coord_precedente_x = self.coord_suivante_x
                    self.coord_precedente_y = self.coord_suivante_y
                    self.decodageTrame()
                    self.dessiner(self.coord_precedente_x, self.coord_precedente_y, self.coord_suivante_x, self.coord_suivante_y)
            except:
                print(sys.exc_info()[0])
                self.alertPerso(message="Erreur de connexion")
                self.stop = True
                fileMenu.entryconfigure(1, label="Se connecter")
        self.labelEtatConnexion["text"] = "déconnecté"
        self.com.close()

    def initialisationMenu(self):
        menuFile = Menu(self.menuBar, tearoff=0)
        menuFile.add_command(label="Nouveau", command=self.alert)
        menuFile.add_command(label="Se connecter", command=lambda: self.connexionRobot(menuFile))
        menuFile.add_command(label="Changer Configuration", command=self.changementConfig)
        menuFile.add_separator()
        menuFile.add_command(label="Quitter", command=self.quit)

        menuEdit = Menu(self.menuBar, tearoff=0)
        menuEdit.add_command(label="Mode Automatique", command=self.passageModeAuto)
        menuEdit.add_command(label="Mode Manuel", command=self.passageModeManuel)
        menuEdit.add_separator()
        menuEdit.add_command(label="Changer le port de connexion", command=self.changerPort)

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

    def changerPort(self):
        fenetre = tk.Toplevel()
        fenetre.resizable(width=False, height=False)
        fenetre.geometry("150x70")
        Label(fenetre, text="Entrez le nom du port").pack()
        value = StringVar()
        value.set(self.serialPortString)
        entree = Entry(fenetre, textvariable=value, width=30)
        entree.pack()
        Button(fenetre, text="ok", command=lambda: self.validerChangementPort(fenetre, value.get())).pack()

    def validerChangementPort(self, fen, text):
        fen.destroy()
        self.serialPortString = text
        self.labelPort["text"] = "Port Actuel : " + text

    def passageModeManuel(self):
        self.boutonStart.grid_forget()
        self.boutonPause.grid_forget()
        self.boutonStop.grid_forget()
        self.labelTempsRun.grid_forget()
        if self.affichageVertical:
            self.labelManuel["text"] = "Utilisez les flèches directionnelles \n  pour contrôler le robot"
            self.labelManuel.grid(row=1, column=0, rowspan=3)
        else:
            self.labelManuel["text"] = "Utilisez les flèches directionnelles pour contrôler le robot"
            self.labelManuel.grid(row=1, column=0, columnspan=3)
        self.labelCommande["text"] = "Commande Manuelle"

        if not self.stop :
            emissionArduino(self.com,"m")
        self.modeAutomatique = False

    def passageModeAuto(self):
        self.labelManuel.grid_forget()
        if self.affichageVertical:
            self.boutonStart.grid(row=1, column=0, pady=5, sticky='N')
            self.boutonPause.grid(row=2, column=0, pady=5, sticky='N')
            self.boutonStop.grid(row=3, column=0, pady=5, sticky='N')
            self.labelTempsRun.grid(row=4, column=0, pady=5, sticky='N')
        else:
            self.boutonStart.grid(row=1, column=0, pady=5, sticky='N')
            self.boutonPause.grid(row=1, column=1, pady=5, sticky='N')
            self.boutonStop.grid(row=1, column=2, pady=5, sticky='N')
            self.labelTempsRun.grid(row=1, column=3, pady=5, sticky='N')
        self.labelCommande["text"] = "Commande Automatique"

        if not self.stop :
            emissionArduino(self.com,"a")
        self.modeAutomatique = True

    def changementConfig(self):
        self.caseEtat.grid_forget()
        self.telecomande.grid_forget()
        self.labelTempsRun.grid_forget()
        self.labelCommande.grid_forget()
        self.barreControle.grid_forget()
        if self.affichageVertical:
            self.passageConfigHorizontale()
        else:
            self.passageConfigVerticale()
        if self.modeAutomatique:
            self.passageModeAuto()
        else:
            self.passageModeManuel()

    def passageConfigHorizontale(self):
        """     PLACEMENT DES ELEMENTS SUR LA FENETRE    """
        self.caseEtat.grid(row=0, column=1, rowspan=2, sticky='NEWS')
        self.telecomande.grid(row=0, column=0, rowspan=2, sticky='NEWS')
        self.labelTempsRun.grid(row=1, column=3, pady=5, sticky='N')
        self.labelCommande.grid(row=0, column=0, columnspan=4)
        self.barreControle.grid(row=1, sticky='NEWS')
        self.labelEtatConnexion.grid(row=0, column=0)
        self.labelEtatScan.grid(row=0, column=1)
        self.labelPort.grid(row=1, column=0)
        self.labelFreqDenvoie.grid(row=1, column=1)

        '''      CONFIGURATION DES LIGNES & COLONES     '''
        self.barreControle.grid_columnconfigure(1, weight=1)
        self.barreControle.grid_columnconfigure(0, weight=1)
        self.barreControle.grid_rowconfigure(0, weight=1)
        self.barreControle.grid_rowconfigure(1, weight=1)

        self.telecomande.grid_columnconfigure(0, weight=4)
        self.telecomande.grid_columnconfigure(1, weight=2)
        self.telecomande.grid_columnconfigure(2, weight=2)
        self.telecomande.grid_columnconfigure(3, weight=2)
        self.telecomande.grid_rowconfigure(0, weight=1)
        self.telecomande.grid_rowconfigure(1, weight=1)

        self.caseEtat.grid_rowconfigure(0, weight=1)
        self.caseEtat.grid_rowconfigure(1, weight=1)
        self.caseEtat.grid_rowconfigure(2, weight=0)
        self.caseEtat.grid_rowconfigure(3, weight=0)
        self.caseEtat.grid_columnconfigure(0, weight=1)
        self.caseEtat.grid_columnconfigure(1, weight=1)

        '''      CONFIGURATION DES LIGNES & COLONES DE LA FENETRE DE BASE      '''
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=0)

        ''' CHANGEMENT VARIABLE '''
        self.affichageVertical = False

    def passageConfigVerticale(self):
        """     PLACEMENT DES ELEMENTS SUR LA FENETRE    """
        self.caseEtat.grid(row=1, column=0, sticky='NEWS')
        self.telecomande.grid(row=0, column=0, sticky='NEWS')
        self.labelTempsRun.grid(row=4, column=0, pady=5, sticky='N')
        self.labelCommande.grid(row=0, column=0)
        self.barreControle.grid(row=0, column=1, sticky='NEWS')
        self.labelEtatConnexion.grid(row=0, column=0)
        self.labelEtatScan.grid(row=1, column=0)
        self.labelPort.grid(row=2, column=0)
        self.labelFreqDenvoie.grid(row=3, column=0)

        '''      CONFIGURATION DES LIGNES & COLONES     '''
        self.barreControle.grid_columnconfigure(0, weight=1)
        self.barreControle.grid_columnconfigure(1, weight=0)
        self.barreControle.grid_rowconfigure(0, weight=1)
        self.barreControle.grid_rowconfigure(1, weight=1)

        self.telecomande.grid_rowconfigure(0, weight=1)
        self.telecomande.grid_rowconfigure(1, weight=1)
        self.telecomande.grid_rowconfigure(2, weight=1)
        self.telecomande.grid_rowconfigure(3, weight=1)
        self.telecomande.grid_columnconfigure(0, weight=1)
        self.telecomande.grid_columnconfigure(1, weight=0)
        self.telecomande.grid_columnconfigure(2, weight=0)
        self.telecomande.grid_columnconfigure(3, weight=0)

        self.caseEtat.grid_rowconfigure(0, weight=1)
        self.caseEtat.grid_rowconfigure(1, weight=1)
        self.caseEtat.grid_rowconfigure(2, weight=1)
        self.caseEtat.grid_rowconfigure(3, weight=1)
        self.caseEtat.grid_columnconfigure(0, weight=1)
        self.caseEtat.grid_columnconfigure(1, weight=0)

        '''      CONFIGURATION DES LIGNES & COLONES DE LA FENETRE DE BASE      '''
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)

        self.affichageVertical = True

    def startModeAutomatique(self):
        self.labelTempsRun["text"] = "Temps 10.00.00"

        '''    MISE A JOUR GRAPHIQUE   '''
        self.boutonStart["state"] = DISABLED
        self.boutonStop["state"] = ACTIVE
        self.boutonPause["state"] = ACTIVE

    def pauseModeAutomatique(self):
        self.labelTempsRun["text"] = "Temps 10.00.00"

        '''    MISE A JOUR GRAPHIQUE   '''
        self.boutonStart["state"] = ACTIVE
        self.boutonStop["state"] = ACTIVE
        self.boutonPause["state"] = DISABLED

    def stopModeAutomatique(self):
        self.labelTempsRun["text"] = "Temps 10.00.00"

        '''    MISE A JOUR GRAPHIQUE   '''
        self.boutonStart["state"] = ACTIVE
        self.boutonStop["state"] = DISABLED
        self.boutonPause["state"] = DISABLED

    def clavier(self, event):
        self.touche = event.keysym
        if self.nouvelleTouche and not self.modeAutomatique:
            if self.touche == "Up":
                emissionArduino(self.com, "0")
                self.nouvelleTouche = False
            elif self.touche == "Down":
                emissionArduino(self.com, "1")
                self.nouvelleTouche = False
            elif self.touche == "Right":
                emissionArduino(self.com, "2")
                self.nouvelleTouche = False
            elif self.touche == "Left":
                emissionArduino(self.com, "3")
                self.nouvelleTouche = False

    def resetTouche(self, event):
        self.touche = '4'
        self.nouvelleTouche = True
        if not self.modeAutomatique:
            emissionArduino(self.com, str(self.touche))

    def fermer(self):
        self.destroy()
        self.stop = True

if __name__ == "__main__":
    app = Application()
    app.title("Rammus Scanning")
    photo = PhotoImage(file='../img/maquetteLogiciel/vago.png')
    app.mainloop()
