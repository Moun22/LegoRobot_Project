from constante import *

# Pid controlleur à temps discret -> ce qui est censé être utiliser pour notre model
class Pid :
    def __init__(self, Kp, Ki, Kd, N, Ts):
        self.e = [0, 0, 0]
        self.u = [0, 0, 0]
        a0 = (1+N*Ts)
        a1 = -(2 + N*Ts)
        a2 = 1

        b0 = Kp*(1+N*Ts) + Ki*Ts*(1+N*Ts) + Kd*N
        b1 = -(Kp*(2+N*Ts) + Ki*Ts + 2*Kd*N)
        b2 = Kp + Kd*N

        self.ku = [a1/a0, a2/a0]
        self.ke = [b0/a0, b1/a0, b2/a0]

    def exec_pid(self, expect, plant):
        e = self.e
        u = self.u
        ku = self.ku
        ke = self.ke
        e[2] =e[1]
        e[1] =e[0]
        u[2] =u[1]
        u[1] =u[0]

        e[0] = expect - plant  # compute new error
        u[0] = - ku[0]* u[1] -  ku[1]* u[2] +  ke[0]* e[0] +  ke[1]* e[1] +  ke[2]* e[2]

        print(u[0])

        if (u[0] > 1000):
            u[0] = 1000  # limit to DAC or PWM range
        elif (u[0] < 500):
            u[0] = 500

        self.e = e
        self.u = u
        self.ku = ku
        self.ke = ke

        return u[0]


class Pid2:
    def __init__(self, Kp, Ki, Kd):
        self.cons = self.err = 0
        self.error = self.prev_error = self.sum_error = 0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
    
    def get_consigne(s):
        return s.cons
    
    def get_error(s):
        return s.err

    def defin_min_pos(s, vit_mes, vit_ref, freq_mes, freq_ref):
        if (freq_mes > freq_ref) :
            if (vit_mes >= vit_ref) :
                s.error = abs(s.error)*(-1)
            elif (vit_mes < vit_ref) :
                s.error = abs(s.error)
        elif (freq_mes < freq_ref) :
            if (vit_mes >= vit_ref) :   
                s.error = abs(s.error)*(-1) #on diminue la vitesse
            elif (vit_mes < vit_ref) :
                s.error = abs(s.error)

    def set_error(s, cons, mes):
        s.error = cons-mes

    # error = consigne - mesure
    def __calcul_pid(s):
        s.sum_error += s.error 
        add_speed = (s.Kp * s.error) + (s.Ki * s.sum_error) + (s.Kd * (s.error - s.prev_error))
        s.prev_error = s.error
        return add_speed

    def exec_pid(s, roue_fort, temp_vit, palier):
        index = 0 if roue_fort == GAUCHE else 1
        vit = temp_vit[index]
        vit_add = s.__calcul_pid()*palier
        temp_vit[index] = vit + vit_add