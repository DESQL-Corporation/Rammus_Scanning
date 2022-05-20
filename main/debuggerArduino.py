import serial  # Importation de la bibliothèque « pySerial »
import serial.tools.list_ports

SERIALPORT = 'COM3'
BAUDRATE = 9600


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


if __name__ == "__main__":
    com = ouvrir_liaisonArduino(SERIALPORT)
    print("connecte")
    while 1:
        message = recpetionArduino(com)
        print(message)
