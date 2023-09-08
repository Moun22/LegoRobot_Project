#!/usr/bin/env pybricks-micropython
from time import sleep
from pybricks.parameters import Port

from pid import Pid2
from systeme import *
from constante import *

import affichage
import mesure
import croisement

# definition de notre ROBOT
robot = Robot(Port.S1, Port.C, Port.B)
robot.light.off()
robot.speaker.set_volume(10, 'Beep')

"""
def test_freq_pid_constant_speed_rgb():
    switch = True # si on est en dehors de la piste on commence à changer de roue
    roue_fort = DROITE # roue droite qui roule en premier
    freq_mesure = 0.05
    init_vit = (500, -10)
    temp_vit = [init_vit[0], init_vit[0]]   # indicateur de vitesses dans la référence
    ref_arc = 11
    palier = 15
    arc_solo_temp = 0
    premier_arc = True # enlever le premier arc qui est faux

    pid_droit  = Pid2(0.5,0.3,0.1)
    pid_gauche = Pid2(0.3,0.3,0.1)

    # préléminaire
    #col_parc = robot.get_color_until_button_pressed()
    robot.init_three_colors()
    robot.wait_button_pressed()
    for i in robot.col_rgb :
        print(i)
    print()

    # boucle "sans fin"
    while True :
        sleep(freq_mesure)
        # on récupère la valeur de la couleur mesurer
        actual_col_rgb = robot.get_actual_col_rgb()
        print(actual_col_rgb)
        # --- cas où on est sur la ligne de départ/arrivée ---
        if (robot.is_right_col_rgb(actual_col_rgb, STREND)):
            if robot.get_state() == CONTINUOUS:
                robot.hold_motors()
                break
            switch = True
        # --- cas où on est sur le parcourt ---
        if (robot.is_right_col_rgb(actual_col_rgb, CIRCUIT)):
            robot.set_state(CONTINUOUS) # indication qu'on est tjrs sur le parcourt
            switch = True
        # --- cas des couleurs inconnues ---
        else :
            if switch :
                switch = False
                affichage.freq(arc_solo_temp, roue_fort)
                print()
                # execution du pid pour la roue droite et gauche
                if roue_fort == DROITE and not premier_arc:
                    pid_droit.set_error(ref_arc, arc_solo_temp)
                    pid_droit.defin_min_pos(temp_vit[1], init_vit[0], arc_solo_temp, ref_arc)
                    pid_droit.exec_pid(roue_fort,temp_vit,palier)
                elif roue_fort == GAUCHE and not premier_arc:
                    pid_gauche.set_error(ref_arc, arc_solo_temp)
                    pid_gauche.defin_min_pos(temp_vit[0], init_vit[0], arc_solo_temp, ref_arc)
                    pid_gauche.exec_pid(roue_fort,temp_vit,palier)
                # réinitialisation des variables
                premier_arc = False
                roue_fort = not roue_fort
                arc_solo_temp = 0
        arc_solo_temp += 1
        # si cela fait trop longtemps qu'on est sur l'arc on braque
        if(arc_solo_temp > ref_arc):
            robot.switch_strong_wheel_incr(roue_fort, temp_vit, palier, -100)
        # sinon on roule normalement
        else :
            robot.switch_strong_wheel(roue_fort, temp_vit, init_vit[1])
        affichage.wheel_speed(temp_vit)
"""

def main_freq_pid_constant_speed():
    switch = True # si on est en dehors de la piste on commence à changer de roue
    roue_fort = DROITE # roue droite qui roule en premier
    freq_mesure = 0.05
    init_vit = (400, -10)
    temp_vit = [init_vit[0], init_vit[0]]   # indicateur de vitesses dans la référence
    ref_arc = 19
    palier = 15
    arc_solo_temp = 0
    premier_arc = True

    pid_droit  = Pid2(0.5,0.1,0.3)
    pid_gauche = Pid2(0.5,0.1,0.3)

    # préléminaire
    #col_parc = robot.get_color_until_button_pressed()
    robot.init_three_colors()
    robot.wait_button_pressed()
    # boucle "sans fin"
    while True :
        sleep(freq_mesure)

        # on récupère la valeur de la couleur mesurer
        actual_col = robot.get_actual_col()
        robot.modif_uncer_col(actual_col)

        # si nous avons les deux même couleur on continue
        if robot.same_uncer_col() :
            # --- cas où on est sur la ligne de départ/arrivée ---
            if (actual_col == robot.col[0]):
                if robot.get_state() == CONTINUOUS:
                    robot.stop_motors()
                    break
                switch = True
            # --- cas où on est sur le parcourt ---
            elif (actual_col == robot.col[1]):
                robot.set_state(CONTINUOUS) # indication qu'on est tjrs sur le parcourt
                switch = True
            # --- cas où on est sur l'intersection ---
            elif (actual_col == robot.col[2]):
                croisement.exec_inter(robot, roue_fort)
            # --- cas des couleurs inconnues ---
            else :
                if switch :
                    switch = False
                    # execution du pid pour la roue droite et gauche
                    if roue_fort == DROITE and not premier_arc:
                        pid_droit.set_error(ref_arc, arc_solo_temp)
                        pid_droit.defin_min_pos(temp_vit[1], init_vit[0], arc_solo_temp, ref_arc)
                        pid_droit.exec_pid(roue_fort,temp_vit,palier)
                    elif roue_fort == GAUCHE and not premier_arc:
                        pid_gauche.set_error(ref_arc, arc_solo_temp)
                        pid_gauche.defin_min_pos(temp_vit[0], init_vit[0], arc_solo_temp, ref_arc)
                        pid_gauche.exec_pid(roue_fort,temp_vit,palier)
                    # réinitialisation des variables
                    premier_arc = False
                    roue_fort = not roue_fort
                    arc_solo_temp = 0
        arc_solo_temp += 1
        # si cela fait trop longtemps qu'on est sur l'arc on braque
        if(arc_solo_temp > ref_arc):
            robot.switch_strong_wheel_incr(roue_fort, temp_vit, palier, -200)
        # sinon on roule normalement
        else :
            robot.switch_strong_wheel(roue_fort, temp_vit, init_vit[1])

main_freq_pid_constant_speed()
