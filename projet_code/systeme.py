from time import sleep
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import (Button, Color, Stop)


from capteur import *
from constante import *

class Robot(EV3Brick):
    def __init__(self, port_sens, port_motor_g, port_motor_d):
        self.capteur  = Capteur(port_sens)
        self.moteur_g = Motor(port_motor_g)
        self.moteur_d = Motor(port_motor_d)
        # [coul. de départ/arrivé, coul. de parcourt, coul. intersection]
        self.col = [Color.WHITE, Color.WHITE, Color.WHITE]
        self.col_rgb = []
        self.state = ALIVE
        # on récupère deux couleurs, si les deux sont bonnes, alors on envoie True
        # sinon on envoie False
        self.uncer_col = [Color.WHITE, Color.WHITE]  

    # === getter et setter attribut ===

    def set_state(s, state):
        s.state = state
    
    def get_state(s):
        return s.state
    
    # === method d'attente de la part de l'utilisateur ===
    def wait_button_pressed(s, text=""):
        while True :
            s.print(text)
            buttons = s.buttons.pressed()
            if buttons :
                break
    
    def wait_color_button_pressed(s, text=""):
        while True :
            sleep(0.1)
            color = s.capteur.color()
            buttons = s.buttons.pressed()
            s.print(text + str(color))
            if buttons :
                return color


    # === instruction donné au robot pour l'utilisateur ===
    
    def sound_3_beeps(s):
        for i in range(3):
            sleep(0.400)
            s.speaker.beep(500, 100)

    # --- écran du robot ---
    def print(s, string):
        s.screen.clear()
        s.screen.print(string)
    
    # === comptortement sur la couleur ===
    def get_actual_col(s):
        return s.capteur.color()
    
    # C'est dans cette partie que se ferra les calculs de couleur,
    # savoir si la couleur perçu est bien la couleur attendu
    def get_actual_col_rgb(s):
        col_mes = s.capteur.color()
        rgb_mes = s.capteur.rgb()
        return (col_mes, rgb_mes)

    def init_three_colors_rgb(s):
        col = s.capteur.right_col(s)
        s.col_rgb.append( (col, s.capteur.get_min_max_rgb(s, "Col dep/arr")) )
        s.sound_3_beeps()
        col = s.capteur.right_col(s)
        s.col_rgb.append( (col, s.capteur.get_min_max_rgb(s, "Parcourt")) )
        s.sound_3_beeps()
        col = s.capteur.right_col(s)
        s.col_rgb.append( (col, s.capteur.get_min_max_rgb(s, "Intersec")) )
        s.sound_3_beeps()
    
    def init_three_colors(s):
        s.col[0] = s.capteur.right_col(s)
        s.sound_3_beeps()
        s.col[1] = s.capteur.right_col(s)
        s.sound_3_beeps()
        s.col[2] = s.capteur.right_col(s)
        s.sound_3_beeps()
    
    def is_right_col_rgb(s, col_rgb_mes, state):
        col_mes = col_rgb_mes[0]
        rgb_mes = col_rgb_mes[1]
        if state == STREND:
            if col_mes == s.col_rgb[0][0]:
                if s.capteur.is_in_rgb_box(rgb_mes, s.col_rgb[0][1]):
                    return True
        elif state == CIRCUIT:
            if col_mes == s.col_rgb[1][0]:
                if s.capteur.is_in_rgb_box(rgb_mes, s.col_rgb[1][1]):
                    return True
        elif state == INTERSEC:
            if col_mes == s.col_rgb[2][0]:
                if s.capteur.is_in_rgb_box(rgb_mes, s.col_rgb[2][1]):
                    return True
        return False

    def same_uncer_col(s):
        if s.uncer_col[0] not in s.col:
            return True
        if s.uncer_col[0] == s.uncer_col[1]:
            return True
        return False
    
    def modif_uncer_col(s, col_mes):
        # [now, before] -> on déplace l'ancien valeur à la case 1
        col_to_move = s.uncer_col[0]
        s.uncer_col[0] = col_mes
        s.uncer_col[1] = col_to_move

    # === comportement du robot par rapport aux moteurs ===

    def stop_motors(s):
        s.moteur_d.stop()
        s.moteur_g.stop()
    
    def brake_motors(s):
        s.moteur_d.brake()
        s.moteur_g.brake()
    
    def hold_motors(s):
        s.moteur_d.hold()
        s.moteur_g.hold()
    
    def get_speed(s):
        return (s.moteur_g.speed(),s.moteur_d.speed())
    
    def turn_motors_degree(s, degree_g, degree_d, wait):
        s.moteur_d.run_time(degree_d, 1000, Stop.HOLD, False)
        if wait :
            s.moteur_g.run_time(degree_g, 1000, Stop.HOLD, True)
        else :
            s.moteur_g.run_time(degree_g, 1000, Stop.HOLD, False)

    def switch_strong_wheel(s, roue_fort, speeds, vit_min):
        if roue_fort == DROITE:
            s.moteur_d.run(speeds[1])
            s.moteur_g.run(vit_min)
        else :
            s.moteur_d.run(vit_min)
            s.moteur_g.run(speeds[0])
    
    def switch_strong_wheel_incr(s, roue_fort, vitesses, palier, vit_mini):
        if roue_fort == DROITE:
            vitesses[1] += palier
            s.moteur_d.run(vitesses[1])
            s.moteur_g.run(vit_mini)
        else :
            vitesses[0] += palier
            s.moteur_d.run(vit_mini)
            s.moteur_g.run(vitesses[0])