import queue
from Llamada import Llamada

class ColaLlamadas:
    def __init__(self):
        self.cola = queue.Queue()
        self.ultima_modificacion = -1
        self.size = 0
        
    def __str__(self):
        return str(list(self.cola.queue))

    def push(self, llamada):
        self.cola.put_nowait(llamada)
        self.size += 1

    def pop(self):
        if(self.size > 0):
            self.size -= 1
        return self.cola.get_nowait()
