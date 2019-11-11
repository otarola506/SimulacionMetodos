
class Llamada:
    def __init__(self, inicio = -1, tipo = -1, origen = -1 , tiempoEnCola = 0 ):
        self.inicio = inicio
        self.tipo = tipo  # tipo 1 larga distancia tipo 2 locales 
        self.origen = origen
        self.tiempoEnCola = tiempoEnCola

    def __str__(self):
        return repr(self) + "\ninicio: " + str(self.inicio) + "\ntipo: " + str(self.tipo) + "\norigen: " + str(self.origen)

    def set_inicio(self, inicio):
        self.inicio = inicio

    def set_tipo(self, tipo):
        self.tipo = tipo
        
    def set_origen(self, origen):
        self.origen = origen
