from time import sleep
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import (Button, Color)

from systeme import *

# !!! FICHIER NON UTILISE !!!
# Capteur nous permettra de bien détecter les couleurs perçu,
# et nous faire éviter les erreurs de mesures (Blue alors que c'était White)
# technique abordée : 
#   Mesures des couleurs dans une boîte de valeurs. Au cours du parcours,
#   nous feront questionner le robot, si la valeur qu'il a lu correspond
#   bien à la couleur, il le calcule, sinon il le laisse passer 
class Capteur(ColorSensor):
    def __init__(self, port):
        self.port = port

    # === méthode pour évaluer les couleurs entre elles ===
    def __is_min(s, rgb, rgb_min):
        if rgb[0] <= rgb_min[0] and rgb[1] <= rgb_min[1] and rgb[2] <= rgb_min[2]:
            return True
        return False
    
    def __is_max(s, rgb, rgb_max):
        if rgb[0] >= rgb_max[0] and rgb[1] >= rgb_max[1] and rgb[2] >= rgb_max[2]:
            return True
        return False
    
    def __sort_list_col_min_max(s, list_col):
        col_box = [list_col[0], list_col[0]]
        for col in list_col:
            if s.__is_min(col, col_box[0]):
                col_box[0] = col
            if s.__is_max(col, col_box[1]):
                col_box[1] = col
        return col_box
    
    def is_in_rgb_box(s, rgb, rgb_box):
        col_min = rgb_box[0]
        col_max = rgb_box[1]
        # savoir s'il est au dessus du min
        if rgb[0] >= col_min[0] and rgb[1] >= col_min[1] and rgb[2] >= col_min[2]:
            # savoir s'il est en dessous du max
            if rgb[0] <= col_max[0] and rgb[1] <= col_max[1] and rgb[2] <= col_max[2]:
                return True
        return False
    
    # === méthode publique à utiliser pour le robot ===

    # permet de définir si nous avons la bonne couleur pour le robot
    def right_col(s, robot):
        buttons = []
        color = Color.WHITE
        while Button.RIGHT not in buttons:
            sleep(0.01)
            buttons.extend(robot.buttons.pressed())
            color = s.color()
            robot.print(str(color) + " ?\n" + "Left for no\n" + "Right for yes")
        return color
    
    # permet d'obtenir une liste de couleur que l'on évaluera par la suite
    def get_list_col(s, robot):
        list_col = []
        buttons = []
        while Button.CENTER not in buttons:
            robot.light.on(Color.RED)
            sleep(0.4)
            robot.light.off()
            sleep(0.1)
            buttons.extend(robot.buttons.pressed())
            list_col.append(s.rgb())
        return list_col

    # problème avec ce code,
    # il ne faut pas sortir de la couleur qu'on évalue
    def get_min_max_rgb(s, robot, text):
        # première boucle pour prévenir l'utilisateur
        buttons = []
        while Button.CENTER not in buttons:
            sleep(0.1)
            robot.print("Appuyer CENTRE\npour commencer\n"+text)
            buttons.extend(robot.buttons.pressed())
        robot.speaker.beep(500, 100)
        # prise d'échantillon
        list_col = s.get_list_col(robot)
        print(list_col)
        print()
        sort_list_col = s.__sort_list_col_min_max(list_col)
        return sort_list_col
    