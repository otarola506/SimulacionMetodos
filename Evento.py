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
        print("Inicio: " + str(self.inicio))
        if self.tipo == 1: # E1: Llega llamada externa a  A 
            self.evento1()

        if self.tipo == 2: # E2: Llega llamada externa a  B
            self.evento2()

        if self.tipo == 4: # E4: Termina de atender llamada en A
            self.evento4()

    def evento1(self):
        print("Arriba llamada a A")
        self.simulacion.reloj = self.inicio
        llamada = Llamada(self.simulacion.reloj, origen = 0)
        rand = random.randint(0, 9)

        if rand < 2:
            llamada.tipo = 1
        else:
            llamada.tipo = 2
        
        if self.simulacion.ocupado_A == True:
            if self.simulacion.cola_A.qsize() == 5:
                llamada.origen = 1
                if self.cola_eventos.exists(3):
                    e3 = Evento(3, self.simulacion.reloj + 0.5, llamada, simulacion = self.simulacion)
                    self.simulacion.cola_eventos.push(e3)
                else:
                    self.simulacion.cola_A_B.put_nowait(llamada)
            else:
                self.simulacion.cola_A.put_nowait(llamada)
        else:
            self.simulacion.ocupado_A = True
            if llamada.tipo == 1:
                tiempo_atencion = self.TAtencionA1()
            else:
                tiempo_atencion = self.TAtencionA2()
            e4 = Evento(4, self.simulacion.reloj + tiempo_atencion, llamada, simulacion = self.simulacion)
            self.simulacion.cola_eventos.push(e4)
        
        tiempo_entre_arribos = self.TEntreArribosA()
        e1 = Evento(1, self.simulacion.reloj + tiempo_entre_arribos)

    def evento2(self):
        cola_A = self.simulacion.cola_A
        # Aqui ya termina llamada
        llamada = cola_A.get_nowait()
        print(llamada)

    def evento4(self):
        self.simulacion.reloj = self.inicio
        print("Termina de atenderse llamada")
    
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