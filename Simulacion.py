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
    max_time = 1000

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
        
        if self.tipo == 3: # E3: Llega llamada de A a B.
            self.evento3()

        if self.tipo == 4: # E4: Termina de atender llamada en A
            self.evento4()

        if self.tipo == 5: # E5: Termina de atender llamada en B
            self.evento5()
    


    def evento1(self):
        print("Llega llamada externa a A    Inicio: " + str(self.inicio))
        Simulacion.reloj = self.inicio
        llamada = Llamada(Simulacion.reloj, origen = 0)
        #Simulacion.cantLlamadasA += 1

        rand = random.randint(0, 9)
        if rand < 2:
            llamada.tipo = 1
        else:
            llamada.tipo = 2
        
        if Simulacion.ocupado_A == True:
            if Simulacion.cola_A.size == 5:
                llamada.origen = 1
                if Simulacion.cola_eventos.exists(3) == False:
                    e3 = Evento(3, Simulacion.reloj + 0.5, llamada)
                    Simulacion.cola_eventos.push(e3) 
                    #Simulacion.cantLlamadasDesviadasA += 1
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
        #Simulacion.cantLlamadasB += 1
        #Simulacion.cantLlamadasLocalesB += 1
        if Simulacion.ocupado_B:
            #Simulacion.tamanoPromedioB += (Simulacion.reloj - Simulacion.cola_B.ultimaModificacion) * Simulacion.cola_B.size
            Simulacion.cola_B.ultima_modificacion = Simulacion.reloj
            Simulacion.cola_B.push(llamada)
        else:
            self.ocupado_B = True
            tiempo_atencion = self.TAtencionB2()
            e5 = Evento(5, Simulacion.reloj + tiempo_atencion, llamada)
            Simulacion.cola_eventos.push(e5)

        tiempo_entre_arribos = self.TEntreArribosB()
        e2 = Evento(2, Simulacion.reloj + tiempo_entre_arribos)
        Simulacion.cola_eventos.push(e2)

    def evento3(self):
        print("Llega llamada de A a B    Inicio: " + str(self.inicio))
        Simulacion.reloj = self.inicio
        #Simulacion.cantLlamadasB += 1
        if Simulacion.ocupado_B:
            #Simulacion.tamanoPromedioB += (Simulacion.reloj - Simulacion.cola_B.ultimaModificacion) * Simulacion.cola_B.size
            Simulacion.cola_B.ultima_modificacion = Simulacion.reloj
            Simulacion.cola_B.push(self.llamada)
        else:
            Simulacion.ocupado_B = True
            if self.llamada.tipo == 1:
                tiempo_atencion = self.TAtencionB1() 
            else:
                tiempo_atencion = self.TAtencionB2()
            e5 = Evento(5, Simulacion.reloj + tiempo_atencion, self.llamada)
            Simulacion.cola_eventos.push(e5)
        if Simulacion.cola_A_B.size > 0:
            llamada = Simulacion.cola_A_B.pop()
            inicio = llamada.inicio + 0.5
            e3 = Evento(3, inicio, llamada)
            Simulacion.cola_eventos.push(e3)


    def evento4(self):
        print("Termina de atenderse llamada en A")
        Simulacion.reloj = self.inicio   
        Simulacion.ocupado_A = False
        #Simulacion.cantLlamadasA_A += 1
        #Simulacion.duracionSistema = Simulacion.reloj - self.llamada.inicio
        #Simulacion.duracionTotalLlamadasA_A += Simulacion.duracionSistema
        #Simulacion.tiempoEnColaA_A = Simulacion.reloj - self.llamada.inicio
        #Simulacion.tiempoEnColaTotalA_A += Simulacion.tiempoEnColaA_A
        if self.llamada.tipo == 2 :
            pass
            #Simulacion.cantLlamadasLocalesRuteadas += 1
            
        if Simulacion.cola_A.size > 0:
            llamada = Simulacion.cola_A.pop()
            Simulacion.ocupado_A = True
            if llamada.tipo == 1:
                tiempo_atencion = self.TAtencionA1()
            else:
                tiempo_atencion = self.TAtencionA2()
            inicio = Simulacion.reloj + tiempo_atencion
            e4 = Evento(4, inicio, llamada)
            Simulacion.cola_eventos.push(e4)


    def evento5(self):
        print("Termina de atenderse llamada en B")
        Simulacion.reloj = self.inicio
        Simulacion.ocupado_B = False
        #Simulacion.duracionSistema = Simulacion.reloj - self.llamada.inicio
        if self.llamada.origen == 0:
            pass
            #Simulacion.cantLLamadasB_B += 1
            #Simulacion.duracionTotalLlamadasB_B += Simulacion.duracionSistema 
            #Simulacion.tiempoEnColaB_B = Simulacion.reloj - self.llamada.inicio
            #Simulacion.tiempoEnColaTotalB_B += Simulacion.tiempoEnColaB_B
        else:
            pass
            #Simulacion.cantLLamadasA_B += 1
            #Simulacion.duracionTotalLlamadasA_B += Simulacion.duracionSistema
            #Simulacion.tiempoEnColaA_B = Simulacion.reloj - self.llamada.inicio
            #Simulacion.tiempoEnColaTotalA_B += Simulacion.tiempoEnColaA_B
        if Simulacion.cola_B.size > 4:
            if self.llamada.tipo == 2:
                #Simulacion.cantLlamadasLocalesB += 1 ***SE DEBE DE HABLAR PORQUE LA PROFE LO CORRIGIO**** creo que se debe eliminar
                rand = random.randint(0, 9)
                if rand == 0:
                    pass
                    #Simulacion.cantLlamadasPerdidasB += 1
                else:
                    pass
                    #Simulacion.cantLlamadasLocalesRuteadas += 1
        if Simulacion.cola_B.size > 0:
            #Simulacion.tamanoPromedioB += (Simulacion.reloj - Simulacion.cola_B.ultima_modificacion) * Simulacion.cola_B.size
            #Simulacion.cola_B.ultima_modificacion = Simulacion.reloj
            llamada = Simulacion.cola_B.pop()
            if llamada.tipo == 1:
                tiempo_atencion = self.TAtencionB1()
            else:
                tiempo_atencion = self.TAtencionB2()
            inicio = Simulacion.reloj + tiempo_atencion
            e5 = Evento(5, inicio, llamada)


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
        esUno=True
        while esUno:
            r = random.random()
            if r != 1:
                esUno = False
        x = - math.log(1 - r) / (2 / 3)
        return x

    def TAtencionB1(self):
        r = random.random()
        if r <= 0.5:
            x = 2 * r
        else:
            x = 3 - 2 * math.sqrt(2- 2 * r)
        return x
        
    def TAtencionB2(self):
        esUno=True
        while esUno:
            r = random.random()
            if r != 1:
                esUno = False
        x = - math.log(1 - r) / (4 / 3)
        return x
    
    def TEntreArribosB(self):
        r = random.random()
        x = 2 *  r + 1

        return x

Simulacion.iniciar()