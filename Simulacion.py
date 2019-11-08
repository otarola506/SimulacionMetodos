import queue
from Evento import Evento
from ColaEventos import ColaEventos
# La cola de prioridad tiene solo los eventos programados

class Simulacion:
    def __init__(self):
        # Inicializar Variables
        self.cola_A = queue.Queue()
        self.cola_B = queue.Queue()
        self.cola_A_B = queue.Queue()
        self.cola_eventos = ColaEventos()
        self.ocupado_A = False
        self.ocupado_B = False
        self.cola_eventos = ColaEventos()
        self.reloj = 0
        self.max = 3


    def iniciar(self):
        # Inicializar Eventos
        e1 = Evento(1, self.reloj, simulacion = self)  
        self.cola_eventos.push(e1)
        while self.reloj < self.max:
            evento_actual = self.cola_eventos.pop()
            evento_actual.iniciar()
        # Imprimir estadisticas

simulacion = Simulacion()
simulacion.iniciar()