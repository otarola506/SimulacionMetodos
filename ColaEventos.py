import queue
from Evento import Evento

class ColaEventos:
    def __init__(self):
        self.cola = queue.PriorityQueue()

    def __str__(self):
        return str(list(self.cola.queue))

    def push(self, evento):
        self.cola.put_nowait((evento.inicio, evento))

    def pop(self):
        inicio, evento = self.cola.get_nowait()
        return evento
        
    def exists(self, tipo_evento):
        existe = False
        l = list(self.cola.queue)
        for item in l:
            if tipo_evento == item[1].tipo:
                existe = True
                return existe
            return existe
        