from constante import *
from pybricks.ev3devices import ColorSensor

# affichage sur le terminal

def freq(arc, roue_fort):
    roue = "droite" if roue_fort == DROITE else "gauche"
    print("arc " + roue + " : " + str(arc))


def wheel_speed(temp_speeds):
    print("vitesse des roues : " + str(temp_speeds))
