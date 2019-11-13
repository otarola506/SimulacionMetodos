#Clase que representa la llamada tiene tiempo_arribo, tipo, origen, tiempoEnCola
class Llamada:
    origen_string = {0: "Externa", 1: "A"}
    tipo_string = {1: "Larga distancia", 2: "Local"}

    def __init__(self, tiempo_arribo = -1, tipo = -1, origen = -1 , tiempoEnCola = 0 ):
        self.tiempo_arribo = tiempo_arribo
        self.tipo = tipo  # tipo 1 larga distancia tipo 2 locales 
        self.origen = origen # origen
        self.tiempoEnCola = tiempoEnCola

    def __str__(self):
        return "Inicio: " + str(self.tiempo_arribo) + " Tipo: " + self.__class__.tipo_string[self.tipo] + " Origen: " + self.__class__.origen_string[self.origen]

    def set_tiempo_arribo(self, tiempo_arribo):
        self.tiempo_arribo = tiempo_arribo

    def set_tipo(self, tipo):
        self.tipo = tipo
        
    def set_origen(self, origen):
        self.origen = origen
