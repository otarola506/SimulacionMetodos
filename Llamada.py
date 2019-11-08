
class Llamada:
    def __init__(self, inicio = -1, tipo = -1, origen = -1):
        self.inicio = inicio
        self.tipo = tipo
        self.origen = origen
    def __str__(self):
        return repr(self) + "\ninicio: " + str(self.inicio) + "\ntipo: " + str(self.tipo) + "\norigen: " + str(self.origen)

    def set_inicio(self, inicio):
        self.inicio = inicio

    def set_tipo(self, tipo):
        self.tipo = tipo
        
    def set_origen(self, origen):
        self.origen = origen
