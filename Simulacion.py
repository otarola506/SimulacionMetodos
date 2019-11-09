import random
import math
from ColaEventos import ColaEventos
from ColaLlamadas import ColaLlamadas
from Llamada import Llamada
from dataclasses import dataclass

class Simulacion:

    # Inicializar Variables
    cola_A = ColaLlamadas()
    cola_B = ColaLlamadas()
    cola_A_B = ColaLlamadas()
    cola_eventos = ColaEventos() # La cola de eventos tiene solo los eventos programados
    ocupado_A = False
    ocupado_B = False
    reloj = 0
    max_time = 100

    @classmethod
    def iniciar(cls):
        # Inicializar Eventos
        e1 = Evento(1, cls.reloj) 
        e2 = Evento(2, cls.reloj)

        cls.cola_eventos.push(e1)
        cls.cola_eventos.push(e2)
        
        while cls.reloj < cls.max_time:
            evento_actual = cls.cola_eventos.pop()
            evento_actual.iniciar()
        # Imprimir estadisticas

@dataclass(order = True)
class Evento:
    def __init__(self, tipo = -1, inicio = -1, llamada = -1):
        self.tipo = tipo
        self.inicio = inicio
        self.llamada = llamada

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
        Simulacion.reloj = self.inicio
        llamada = Llamada(Simulacion.reloj, origen = 0)

        rand = random.randint(0, 9)
        if rand < 2:
            llamada.tipo = 1
        else:
            llamada.tipo = 2
        
        if Simulacion.ocupado_A == True:
            if Simulacion.cola_A.size == 5:
                llamada.origen = 1
                if Simulacion.cola_eventos.exists(3):
                    e3 = Evento(3, Simulacion.reloj + 0.5, llamada)
                    Simulacion.cola_eventos.push(e3)
                else:
                    Simulacion.cola_A_B.push(llamada)
            else:
                Simulacion.cola_A.push(llamada)
        else:
            Simulacion.ocupado_A = True
            if llamada.tipo == 1:
                tiempo_atencion = self.TAtencionA1()
            else:
                tiempo_atencion = self.TAtencionA2()
            e4 = Evento(4, Simulacion.reloj + tiempo_atencion, llamada)
            Simulacion.cola_eventos.push(e4)
        
        tiempo_entre_arribos = self.TEntreArribosA()
        e1 = Evento(1, Simulacion.reloj + tiempo_entre_arribos)
        Simulacion.cola_eventos.push(e1)

    def evento2(self):
        print("Llega llamada externa a B    Inicio: " + str(self.inicio))
        Simulacion.reloj = self.inicio
        llamada = Llamada(Simulacion.reloj, 2, 0)

        if Simulacion.ocupado_B:
            self.cola_B.ultima_modificacion = Simulacion.reloj
            self.cola_B.push(llamada)
        else:
            self.ocupado_B = True
            tiempo_atencion = self.TAtencionB2()
            e5 = Evento(5, Simulacion.reloj + tiempo_atencion, llamada)
            Simulacion.cola_eventos.push(e5)

        tiempo_entre_arribos = self.TEntreArribosB()
        e2 = Evento(2, Simulacion.reloj + tiempo_entre_arribos)
        Simulacion.cola_eventos.push(e2)

    def evento4(self):
        Simulacion.reloj = self.inicio   
        print("Termina de atenderse llamada en A")
        Simulacion.ocupado_A = False
    
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

Simulacion.iniciar()