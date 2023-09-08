from time import sleep
from pybricks.parameters import Port

from systeme import *
from constante import *

import affichage

robot = Robot(Port.S1, Port.C, Port.B)
robot.light.off()
robot.speaker.set_volume(5, 'Beep')

# ~~~ Fichier pour tester le robot avec des conditions simple ~~~

# cette fonction nous servira à étudier le nombre d'échantillon pris par "arc"
# pour (400, 10) et un temps de 0.1   : ~13 par arc
# pour (500, -10) et un temps de 0.1  : ~11 par arc
# pour (500, -10) et un temps de 0.2  : ~ 8 par arc
# pour (500, -10) et un temps de 0.02 : ~47 par arc
# pour (500, -10) et un temps de 0.05 : ~20 par arc 
# pour (400, -10) et un temps de 0.05 : ~20 par arc
# pour (400, -50) et un temps de 0.05 : ~19 par arc
# pour (350, 100) et un temps de 0.05 : ~24 par arc 
def measurement_ideal_freq_const_speed():
    switch = True
    roue_fort = DROITE # roue droite qui roule en premier
    freq_mesure = 0.05
    init_vit = (400, -50)
    temp_vit = (init_vit[0], init_vit[0])
    index_arc = 0
    arc = [0,0]
    som_arc = 0
    occur = 0

    buttons = []
    col_circuit = robot.wait_color_button_pressed()
    while Button.CENTER not in buttons :
        sleep(freq_mesure)
        buttons.extend(robot.buttons.pressed())
        # color sensor & changement de roue fort
        actual_color = robot.get_actual_col()
        if (actual_color == col_circuit) :
            switch = True
        else :
            if switch :
                affichage.freq(arc, roue_fort)
                roue_fort = not roue_fort
                switch = False
                som_arc += arc[index_arc]
                index_arc = (index_arc+1)%2
                arc[index_arc] = 0
        arc[index_arc] += 1
        occur += 1
        robot.switch_strong_wheel(roue_fort, temp_vit, init_vit[1])
    print("moy = " + str(som_arc/occur))
    
def measure_init_color():
    robot.init_three_colors()
    # affichage des couleurs
    #for i in robot.dico_col_rgb.items():
    #    print(i)


def test_with_constant_speed():
    switch = True
    roue_fort = DROITE # roue droite qui roule en premier
    freq_mesure = 0.1
    init_vit = (300, 50)

    col_circuit = robot.get_color_until_button_pressed()
    while True :
        sleep(freq_mesure)
        # color sensor & changement de roue fort
        actual_col_rgb = robot.get_actual_col_rgb()
        if (actual_col_rgb == col_circuit) :
            switch = True
        else :
            if switch :
                robot.speaker.beep(500, 100)
                roue_fort = not roue_fort
                switch = False
        # ======
        robot.switch_strong_wheel(roue_fort, init_vit)


def test_pid_with_increase_speed():
    switch = True
    roue_fort = DROITE # roue droite qui roule en premier
    freq_mesure = 0.05
    init_vit = (300, 50)
    temp_vit = [init_vit[1], init_vit[0]]
    palier = 10
    arc = [0,0]

    col_circuit = robot.get_color_until_button_pressed()
    while True :
        sleep(freq_mesure)
        # color sensor & changement de roue fort
        actual_col_rgb = robot.get_actual_col_rgb()
        if (actual_col_rgb == col_circuit) :
            switch = True
        else :
            if switch :
                robot.speaker.beep(500, 100)
                affichage.freq(arc, roue_fort)
                roue_fort = not roue_fort
                if (roue_fort == DROITE):
                    temp_vit[1] = init_vit[0]
                else:
                    temp_vit[0] = init_vit[0]
                switch = False
        # ======
        affichage.wheel_speed(temp_vit)
        robot.switch_strong_wheel_incr(roue_fort, temp_vit, palier, init_vit[1])