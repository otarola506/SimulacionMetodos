import random
import math
import sys
import time
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
    evento_actual = None # La cola de eventos tiene solo los eventos programados
    ocupado_A = False
    ocupado_B = False
    reloj = 0

    # Variables para las Estadisticas 
    cantLlamadasA = 0  
    cantLlamadasDesviadasA = 0 
    cantLlamadasB = 0 
    tamanoPromedioB = 0 
    cantLlamadasA_A = 0 
    duracionTotalLlamadasA_A = 0 
    tiempoEnColaTotalA_A = 0 
    cantLlamadasLocalesRuteadas = 0 
    cantLlamadasB_B = 0 
    duracionTotalLlamadasB_B = 0 
    tiempoEnColaTotalB_B = 0 
    cantLlamadasA_B = 0 
    duracionTotalLlamadasA_B = 0 
    tiempoEnColaTotalA_B = 0 
    cantLlamadasPerdidasB = 0 

    # (Creo que no es necesario que sean globales pero las puse como en documento)
    tiempoPromedioA_A = 0
    tiempoPromedioB_B = 0
    tiempoPromedioA_B = 0
    tPromedioColaA_A = 0
    tPromedioColaB_B = 0
    tPromedioColaA_B = 0
    porcentajeLlamadasLocalesPerdidas = 0
    eficienciaA_A = 0
    eficienciaB_B = 0
    eficienciaA_B = 0

    @classmethod
    def limpiarVariables(cls):
        #Se limpian variables para hacer varias ejecuciones
        cls.cola_A = ColaLlamadas()
        cls.cola_B = ColaLlamadas()
        cls.cola_A_B = ColaLlamadas()
        cls.cola_eventos = ColaEventos() # La cola de eventos tiene solo los eventos programados
        cls.evento_actual = ColaEventos() # La cola de eventos tiene solo los eventos programados
        cls.ocupado_A = False
        cls.cocupado_B = False
        cls.reloj = 0

        #Se limpian variables para las Estadisticas 
        cls.cantLlamadasA = 0  
        cls.cantLlamadasDesviadasA = 0 
        cls.cantLlamadasB = 0 
        cls.tamanoPromedioB = 0 
        cls.cantLlamadasA_A = 0 
        cls.duracionTotalLlamadasA_A = 0 
        cls.tiempoEnColaTotalA_A = 0 
        cls.cantLlamadasLocalesRuteadas = 0 
        cls.cantLlamadasB_B = 0 
        cls.duracionTotalLlamadasB_B = 0 
        cls.tiempoEnColaTotalB_B = 0 
        cls.cantLlamadasA_B = 0 
        cls.duracionTotalLlamadasA_B = 0 
        cls.tiempoEnColaTotalA_B = 0 
        cls.cantLlamadasPerdidasB = 0 
    
    def imprimirEstadoSimulacion(cls):
        print("Estado de la simulacion")
        print("Reloj: " + str(cls.reloj))
        print("EventoActual: " + str(cls.evento_actual))
        print("Estado ruteador A: " + str(cls.ocupado_A))
        print("Estado ruteador B: " + str(cls.ocupado_B))
        print("Numero de llamadas que han llegado a A: " + str(cls.cantLlamadasA))
        print("Numero de llamadas que han llegado a A y se enviaron a B: " + str(cls.cantLLamadasA_B))
        print("Numero de llamadas que han llegado a B en total: " + str(cls.cantLlamadasB))
        print("Numero de llamadas que A ha ruteado: " + str(cls.cantLlamadasA_A))
        print("Numero de llamadas que B ha ruteado: " + str(cls.cantLlamadasA_B + cls.cantLlamadasA_A))
        print("Numero de llamadas que B ha perdido: " + str(cls.cantLlamadasPerdidasB))

    @classmethod
    def iniciar(cls):
        cant_corridas = int(sys.argv[1])
        max_time = float(sys.argv[2])
        modo_lonto = False
        delay = 0

        if len(sys.argv) == 5 and sys.argv[3] == "-l":
            modo_lonto = True
            delay = int(sys.argv[4])

        for corrida_actual in range(0, cant_corridas):
            # Inicializar Eventos
            e1 = Evento(1, cls.reloj) 
            e2 = Evento(2, cls.reloj)
            cls.cola_eventos.push(e1)
            cls.cola_eventos.push(e2)

            # Ciclo de eventos
            while cls.reloj < max_time:
                cls.evento_actual = cls.cola_eventos.pop()
                cls.evento_actual.iniciar()
                if modo_lonto:
                    time.sleep(delay)
                    # imprimir estado actual simulacion
            # imprimir estadisticias corrida
            cls.limpiarVariables()
        #imprmir estadisticas promedio corridas

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
        llamada = Llamada(Simulacion.reloj, origen = 0, tiempoEnCola = 0)
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
        llamada = Llamada(Simulacion.reloj, 2, 0, 0)
        #Simulacion.cantLlamadasB += 1
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
        #duracionSistema = Simulacion.reloj - self.llamada.inicio
        #Simulacion.duracionTotalLlamadasA_A += duracionSistema
        #Simulacion.tiempoEnColaTotalA_A += self.llamada.tiempoEnCola
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
        #duracionSistema = Simulacion.reloj - self.llamada.inicio
        if self.llamada.tipo == 2:
            pass
            #Simulacion.cantLlamadasLocalesRuteadas += 1
            if Simulacion.cola_B.size > 4 :
                rand = random.randint(0,9)
                if rand == 0:
                    pass
                    #Simulacion.cantLlamadasPerdidasB
        if self.llamada.origen == 0:
            pass
            #Simulacion.cantLlamadasB_B += 1
            #Simulacion.duracionTotalLlamadasB_B += duracionSistema
            #Simulacion.tiempoEnColaTotalB_B += self.llamada.tiempoEnCola
        else:
            pass
            #Simulacion.cantLlamadasA_B += 1
            #Simulacion.duracionTotalLlamadasA_B += duracionSistema
            #Simulacion.tiempoEnColaTotalA_B += self.llamada.tiempoEnCola + 0.5          
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
            Simulacion.cola_eventos.push(e5)


    def TAtencionA1(self):
        r = random.random()
        x = 10 * (5 * r + 4) ** 1 / 2
        return x

    def TAtencionA2(self):
        z = 0.0
        esNegativo=True
        while esNegativo:
            for i in range(0, 11):
                z += random.random()
            z -= 6.0
            x = 1 * z + 15
            if x >= 0:
                esNegativo = False
        return x
             
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