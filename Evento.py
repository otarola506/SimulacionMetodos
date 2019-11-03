from Llamada import Llamada
import Globales

class Evento:
    def __init__(self, tipo = -1, inicio = -1, llamada = -1, simulacion = -1):
        self.tipo = tipo
        self.inicio = inicio
        self.llamada = llamada
        self.simulacion = simulacion

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

    def evento1(self):
        cola_A = self.simulacion.cola_A
        llamada = Llamada(0, 1, 1)
        cola_A.put(llamada)

    def evento2(self):
        cola_A = self.simulacion.cola_A
        # Aqui ya termina llamada
        llamada = cola_A.get()
        print(llamada)
