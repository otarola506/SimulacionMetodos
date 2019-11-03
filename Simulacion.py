import queue
from queue import PriorityQueue
from Evento import Evento
# La cola de prioridad tiene solo los eventos programados

class Simulacion:
    def __init__(self):
        self.cola_A = queue.Queue()

    def iniciar(self):  
        # Crea llamada
        # Encolar llamada en colaA
        evento1 = Evento(1, 0, simulacion = self)
        evento1.iniciar()
        # Termina llamada en Reloj + 1
        evento2 = Evento(2, 1, simulacion = self)
        evento2.iniciar()



# Crear todos los eventos

# Ciclo para sacar el siguiente evento
#colaEventos = PriorityQueue()



simulacion = Simulacion()
simulacion.iniciar()