#include <SoftwareSerial.h>
#include <Servo.h>
#include <NewPing.h>

//define Orientation
#define NORD 20
#define SUD 21
#define EST 22
#define OUEST 23
//define pin carte
#define rxPin 5
#define txPin 4
#define baudrate 9600
// déclarations des capteurs/moteurs.
SoftwareSerial Bluetooth(rxPin , txPin);
NewPing sonar_face(11, 12);
NewPing sonar_droite(6, 7);
Servo portS1;
Servo portS2;

//variables d'état
int EtatPresent = 0;
int EtatSuivant = 0;
int boucle = 0;
int mode = 1;
//les entrees
int a , b, tempo, tempoMax;
char val;
boolean md, mf, mfExt;
//les sorties
boolean g, d, av, ar;
//variables de positions
int x;
int y;
int orientation;

// fonctions de deplacement
void envoie_trame(int xp, int yp) {
  String message = '$' + (String)xp + '$' + (String)yp + '$';
  Bluetooth.println(message);
}

// fonctions de deplacement
void robot_stop() {
  portS1.writeMicroseconds(1500);
  portS2.writeMicroseconds(1500);
  delay(1000);
}

void robot_forward() {
  portS1.writeMicroseconds(1800);
  portS2.writeMicroseconds(1860);
}

void robot_backward() {
  portS1.writeMicroseconds(1350);
  portS2.writeMicroseconds(1350);
}

void robot_left_turn() {
  portS1.writeMicroseconds(1300);
  portS2.writeMicroseconds(1900);
}

void robot_right_turn() {
  portS1.writeMicroseconds(1900);
  portS2.writeMicroseconds(1305);
}

void setup()
{
  //var
  tempo = 0;
  tempoMax = 4;
  x = 250;
  y = 250;
  orientation = NORD;
  //init
  Serial.begin(baudrate);
  portS1.attach(2);
  portS2.attach(3);
  Bluetooth.begin(baudrate);
  robot_stop();
}


void loop()
{
  Serial.print(String(mode));
  if (mode == 0) {
    mode_auto();
  } else {
    mode_manuel();
  }

  delay(200);
}

void mode_manuel() {
  robot_stop();
  val = 'o';
  while (mode) {
    Serial.print("ATTENTE");
    if (Bluetooth.available()) {
      val = Bluetooth.read();
      Serial.println(val);
      if (val == '0') { //avance
        portS1.writeMicroseconds(1750);
        portS2.writeMicroseconds(1750);
      }
      if (val == '1') { //recule
        portS1.writeMicroseconds(1300);
        portS2.writeMicroseconds(1300);
      }
      if (val == '2') { //gauche
        portS1.writeMicroseconds(1300);
        portS2.writeMicroseconds(1900);
      }
      if (val == '3') { //droite
        portS1.writeMicroseconds(1900);
        portS2.writeMicroseconds(1300);
      }
      if (val == '4') { //stop
        portS1.writeMicroseconds(1500);
        portS2.writeMicroseconds(1500);
      }
      if (val == 'a') {
        portS1.writeMicroseconds(1500);
        portS2.writeMicroseconds(1500);
        mode = 0;
      }
    }
    delay(100);
  }
}

//mode AUTOMATIQUE
void mode_auto() {
  if (boucle == 0) {
    robot_stop();
    if (Bluetooth.available()) {
      val = Bluetooth.read();
      if (val == 'p') {
        boucle = 1;
      }
    }
  } if (boucle == 1) {
    if (Bluetooth.available()) {
      val = Bluetooth.read();
      if (val = 's') {
        boucle = 0;
      }
    }
    a = sonar_face.ping_cm();
  b = sonar_droite.ping_cm();

  mf = ((a < 60) && (a > 0)); // Capte un mur devant
  md = ((b < 50) && (b > 0)); // Capte un mur a droite

  // bloc F
  switch (EtatPresent) { 
    case 0 : //Avance jusqu'a trouver un mur devant
       if (mf) {
          robot_stop();
          EtatSuivant = 2;
       }
       break;
     
    case 1 : 
      if (mf) {
        EtatSuivant = 2;
        robot_stop();
      }
      else if (!mf && !md) {
        EtatSuivant = 4;
        robot_stop();
      }
      break;

    case 2 : //Tourne a gauche
        tempo ++;
        if (tempo >= tempoMax) {
          switch (orientation){
            case NORD :
              orientation = OUEST;
              break;
              
            case OUEST :
              orientation = SUD;
              break;
              
            case SUD :
              orientation = EST;
              break;
              
            case EST :
              orientation = NORD;
              break;
              
            default : 
              orientation = NORD;
              break;
          }
          robot_stop();
          EtatSuivant = 3;
          tempo = 0;
        }
        break;

        
    case 3 : 
      if (md) {
        EtatSuivant = 1;
        robot_stop();
      }
      if (mf) {
        EtatSuivant = 2;
        robot_stop();
      }
      break;
      
    case 4 : 
      tempo ++;
      if (tempo >= tempoMax) {
        switch (orientation){
            case NORD :
              orientation = OUEST;
              break;
              
            case OUEST :
              orientation = SUD;
              break;
              
            case SUD :
              orientation = EST;
              break;
              
            case EST :
              orientation = NORD;
              break;
              
            default : 
              orientation = NORD;
              break;
          }
        robot_stop();
        EtatSuivant = 3;
        tempo = 0;
      }
      break;
      
    default:
      exit(1);
      break;
  }
  //bloc M
  EtatPresent = EtatSuivant;
  //bloc G

  av = ((EtatPresent == 0) || (EtatPresent == 1) || (EtatPresent == 3 ));
  g = (EtatPresent == 2);
  d = (EtatPresent == 4);

  // bloc sortie
  if (av) {
    robot_forward();
    switch (orientation){
            case NORD :
              y = y--;
              break;
              
            case OUEST :
              x = x--;
              break;
              
            case SUD :
              y = y++;
              break;
              
            case EST :
              x = x++;
              break;
              
            default :
              break;
    }
    envoie_trame(x,y);
  }
  if (g) robot_left_turn();
  if (d) robot_right_turn();
  
  delay(100);
  }
}
