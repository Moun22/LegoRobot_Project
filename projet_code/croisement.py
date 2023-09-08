from time import sleep
from pybricks.parameters import Port

from pid import Pid2
from systeme import *
from constante import *

import affichage
import mesure

# lors d'un croisement, on roule très lentement jusqu'à croiser notre intersection
def exec_inter(robot,roue_fort):
    # on arrete complétement le moteur
    robot.hold_motors()
    # on traverse l'intersection
    robot.turn_motors_degree(440, 440, True)

    # on tourne sur nous même vers la droite, puis à gauche si on trouve pas
    robot.turn_motors_degree(360, -360, False)
    while robot.get_speed() != (0,0):
        sleep(0.05)
        actual_col = robot.get_actual_col()
        if actual_col == robot.col[1]:
            robot.hold_motors()
            roue_fort = GAUCHE
            return
    # puis on tourne à droite
    robot.turn_motors_degree(-360, 360, False)
    while robot.get_speed() != (0,0):
        sleep(0.05)
        actual_col = robot.get_actual_col()
        if actual_col == robot.col[1]:
            robot.hold_motors()
            roue_fort = DROITE
            return
        