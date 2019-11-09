import random
import math
from Llamada import Llamada
from dataclasses import dataclass, field
from typing import Any

@dataclass(order = True)
class Evento:
    def __init__(self, tipo = -1, inicio = -1, llamada = -1, simulacion = -1):
        self.tipo = tipo
        self.inicio = inicio
        self.llamada = llamada
        self.simulacion = simulacion

    def __str__(self):
        return repr(self) + "\ntipo: " + str(self.tipo) + "\ninicio: " + str(self.inicio) + "\nllamada: " + str(self.llamada)

    def set_inicio(self, inicio):
        self.inicio = inicio

    def set_llamada(self, llamada):
        self.llamada = llamada
        
    def set_tipo(self, tipo):
        self.tipo = tipo


    def iniciar(self):
        if self.tipo == 1: # E1: Llega llamada externa a  A 
            self.evento1()

        if self.tipo == 2: # E2: Llega llamada externa a  B
            self.evento2()

        if self.tipo == 4: # E4: Termina de atender llamada en A
            self.evento4()

    def evento1(self):
        print("Llega llamada externa a A    Inicio: " + str(self.inicio))
        self.simulacion.reloj = self.inicio
        llamada = Llamada(self.simulacion.reloj, origen = 0)

        rand = random.randint(0, 9)
        if rand < 2:
            llamada.tipo = 1
        else:
            llamada.tipo = 2
        
        if self.simulacion.ocupado_A == True:
            if self.simulacion.cola_A.size == 5:
                llamada.origen = 1
                if self.simulacion.cola_eventos.exists(3):
                    e3 = Evento(3, self.simulacion.reloj + 0.5, llamada, simulacion = self.simulacion)
                    self.simulacion.cola_eventos.push(e3)
                else:
                    self.simulacion.cola_A_B.push(llamada)
            else:
                self.simulacion.cola_A.push(llamada)
        else:
            self.simulacion.ocupado_A = True
            if llamada.tipo == 1:
                tiempo_atencion = self.TAtencionA1()
            else:
                tiempo_atencion = self.TAtencionA2()
            e4 = Evento(4, self.simulacion.reloj + tiempo_atencion, llamada, simulacion = self.simulacion)
            self.simulacion.cola_eventos.push(e4)
        
        tiempo_entre_arribos = self.TEntreArribosA()
        e1 = Evento(1, self.simulacion.reloj + tiempo_entre_arribos, simulacion = self.simulacion)
        self.simulacion.cola_eventos.push(e1)

    def evento2(self):
        print("Llega llamada externa a B    Inicio: " + str(self.inicio))
        self.simulacion.reloj = self.inicio
        llamada = Llamada(self.simulacion.reloj, 2, 0)

        if self.simulacion.ocupado_B:
            self.cola_B.ultima_modificacion = self.simulacion.reloj
            self.cola_B.push(llamada)
        else:
            self.ocupado_B = True
            tiempo_atencion = self.TAtencionB2()
            e5 = Evento(5, self.simulacion.reloj + tiempo_atencion, llamada)
            self.simulacion.cola_eventos.push(e5)

        tiempo_entre_arribos = self.TEntreArribosB()
        e2 = Evento(2, self.simulacion.reloj + tiempo_entre_arribos, simulacion = self.simulacion)
        self.simulacion.cola_eventos.push(e2)

    def evento4(self):
        self.simulacion.reloj = self.inicio   
        print("Termina de atenderse llamada en A")
        self.simulacion.ocupado_A = False
    
    def TAtencionA1(self):
        r = random.random()
        x = 10 * (5 * r + 4) ** 1 / 2
        return x

    def TAtencionA2(self):
        z = 0.0
        for i in range(0, 11):
            z += random.random()
        z -= 6.0
        return 1 * z + 15

    def TEntreArribosA(self):
        r = random.random()
        x = - math.log(1 - r) / (2 / 3)

        return x

    def TAtencionB2(self):
        r = random.random()
        x = - math.log(1 - r) / (4 / 3)

        return x
    
    def TEntreArribosB(self):
        r = random.random()
        x = 2 * r + 1

        return x