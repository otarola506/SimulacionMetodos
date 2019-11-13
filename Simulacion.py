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
    evento_actual = None
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

    # Variables para el promedio de los promedios de estadisticas al final de todas las corridas
    sumTamanosPromedioColaB = 0
    sumTiemposPromedioA_A = 0
    sumTiemposPromedioB_B = 0
    sumTiemposPromedioA_B = 0
    sumTPromedioColaA_A = 0
    sumTPromedioColaB_B = 0
    sumTPromedioColaA_B = 0
    sumPorcentajesLlamadasLocalesPerdidas = 0
    sumEficienciaA_A = 0
    sumEficienciaB_B = 0
    sumEficienciaA_B = 0

    @classmethod
    #Metodo para limpiar las variables cada vez que se ejecuta una corrida
    def limpiarVariables(cls):
        #Se limpian variables para hacer varias ejecuciones
        cls.cola_A = ColaLlamadas()
        cls.cola_B = ColaLlamadas()
        cls.cola_A_B = ColaLlamadas()
        cls.cola_eventos = ColaEventos() # La cola de eventos tiene solo los eventos programados
        cls.evento_actual = None
        cls.ocupado_A = False
        cls.ocupado_B = False
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

    @classmethod
    #Metodo para imprimir el estado de la simulacion 
    def imprimirEstadoSimulacion(cls):
        print("----------------------------------------------------------------------------------------")
        print("Estado de la simulacion")
        print("----------------------------------------------------------------------------------------\n")
        print("Reloj: " + str(cls.reloj))
        print("EventoActual: " + str(cls.evento_actual))
        print("Ruteador A ocupado?: " + str(cls.ocupado_A))
        print("Ruteador B ocupado?: " + str(cls.ocupado_B))
        print("La longitud de la cola en A: " + str(cls.cola_A.size))
        print("La longitud de la cola en B: " + str(cls.cola_B.size))
        print("Numero de llamadas que han llegado a A: " + str(cls.cantLlamadasA))
        print("Numero de llamadas que han llegado a A y se enviaron a B: " + str(cls.cantLlamadasA_B))
        print("Numero de llamadas que han llegado a B en total: " + str(cls.cantLlamadasB))
        print("Numero de llamadas que A ha ruteado: " + str(cls.cantLlamadasA_A))
        print("Numero de llamadas que B ha ruteado: " + str(cls.cantLlamadasA_B + cls.cantLlamadasA_A))
        print("Numero de llamadas que B ha perdido: " + str(cls.cantLlamadasPerdidasB))

    @classmethod
    #Metodo para imprimir las estadisticas por corrida de la simulacion
    def imprimirEstadisticasCorrida(cls, corrida):
        print("----------------------------------------------------------------------------------------")
        print("Estadisticas de la Corrida " + str(corrida))
        print("----------------------------------------------------------------------------------------\n")
        #Tamano Promedio de la cola en B 
        cls.tamanoPromedioB += (cls.reloj - cls.cola_B.ultima_modificacion) * cls.cola_B.size
        tamanoPromedioColaB = cls.tamanoPromedioB / cls.reloj 
        cls.sumTamanosPromedioColaB += tamanoPromedioColaB
        print("Tamano Promedio de la cola en B: " + str(tamanoPromedioColaB))
        #Tiempo promedio de permanencia de una llamada en el sistema
        #Llegaron a A y A las ruteo
        tiempoPromedioA_A = 0
        if cls.cantLlamadasA_A != 0:
            tiempoPromedioA_A = cls.duracionTotalLlamadasA_A / cls.cantLlamadasA_A
        cls.sumTiemposPromedioA_A += tiempoPromedioA_A
        print("Tiempo promedio de permanencia de una llamada que llego a A y A la ruteo: " +  str (tiempoPromedioA_A))
        #Llegaron a B y B las ruteo
        tiempoPromedioB_B = 0
        if cls.cantLlamadasB_B != 0:
            tiempoPromedioB_B = cls.duracionTotalLlamadasB_B / cls.cantLlamadasB_B
        cls.sumTiemposPromedioB_B += tiempoPromedioB_B
        print("Tiempo promedio de permanencia de una llamada que llego a B y B la ruteo: " +  str (tiempoPromedioB_B))
        #Se desviaron de A y B las ruteo
        tiempoPromedioA_B = 0
        if cls.cantLlamadasA_B != 0:
            tiempoPromedioA_B = cls.duracionTotalLlamadasA_B / cls.cantLlamadasA_B
        cls.sumTiemposPromedioA_B += tiempoPromedioA_B
        print("Tiempo promedio de permanencia de una llamada que la desvio A y B la ruteo: " +  str (tiempoPromedioA_B))
        #Tiempo promedio en cola
        #Llegaron a A y A las ruteo
        tPromedioColaA_A = 0
        if cls.cantLlamadasA_A != 0:
            tPromedioColaA_A =  cls.tiempoEnColaTotalA_A / cls.cantLlamadasA_A
        cls.sumTPromedioColaA_A += tPromedioColaA_A
        print("Tiempo promedio en cola de una llamada que llego a  A y A la ruteo: " + str (tPromedioColaA_A))
        #Llegaron a B y B las ruteo
        tPromedioColaB_B = 0
        if cls.cantLlamadasB_B != 0:
            tPromedioColaB_B = cls.tiempoEnColaTotalB_B / cls.cantLlamadasB_B
        cls.sumTPromedioColaB_B += tPromedioColaB_B
        print("Tiempo promedio en cola de una llamada que llego a  B y B la ruteo: " + str (tPromedioColaB_B))
        #Se desviaron de A y B las ruteo
        tPromedioColaA_B = 0
        if cls.cantLlamadasA_B != 0:
            tPromedioColaA_B = cls.tiempoEnColaTotalA_B / cls.cantLlamadasA_B
        cls.sumTPromedioColaA_B += tPromedioColaA_B
        print("Tiempo promedio en cola de una llamada que la desvio A y B la ruteo: " + str (tPromedioColaA_B))
        #Porcentaje de llamadas perdidas por B
        porcentajeLlamadasLocalesPerdidas = 0
        if cls.cantLlamadasLocalesRuteadas != 0:
            porcentajeLlamadasLocalesPerdidas = (cls.cantLlamadasPerdidasB / cls.cantLlamadasLocalesRuteadas) * 100 
        cls.sumPorcentajesLlamadasLocalesPerdidas += porcentajeLlamadasLocalesPerdidas
        print("Porcentaje de llamadas perdidas por B: " + str(porcentajeLlamadasLocalesPerdidas))
        #Eficiencia
        #Llegaron a A y A las ruteo
        eficienciaA_A = 0
        if tiempoPromedioA_A != 0:
            eficienciaA_A = tPromedioColaA_A / tiempoPromedioA_A
        cls.sumEficienciaA_A += eficienciaA_A
        print("Eficiencia de las llamadas que llegaron a A y A las ruteo: " + str(eficienciaA_A))
        #Llegaron a B y B las ruteo
        eficienciaB_B = 0
        if tiempoPromedioB_B != 0:
            eficienciaB_B = tPromedioColaB_B / tiempoPromedioB_B
        cls.sumEficienciaB_B += eficienciaB_B
        print("Eficiencia de las llamadas que llegaron a B y B las ruteo: " + str(eficienciaB_B))
        #Se desviaron de A y B las ruteo
        eficienciaA_B = 0
        if tiempoPromedioA_B != 0:
            eficienciaA_B = tPromedioColaA_B / tiempoPromedioA_B
        cls.sumEficienciaA_B += eficienciaA_B
        print("Eficiencia de las llamadas que se desviaron de A y B las ruteo: " + str(eficienciaA_B))
    
    @classmethod
    #Metodo para imprimir las estadisticas globales al finalizar todo el programa (despues de todas las corridas)
    def imprimirEstadisticasGlobales(cls, cant_corridas):
        print("----------------------------------------------------------------------------------------")
        print("Estadisticas Globales al final de las corridas ")
        print("----------------------------------------------------------------------------------------\n")
        #Tamano promedio global de la cola en B
        tamanoPromedioColaBGlobal = cls.sumTamanosPromedioColaB / cant_corridas
        print("Tamano Promedio Global de la cola en B: " + str(tamanoPromedioColaBGlobal))
        #Tiempo promedio global de permanencia de una llamada en el sistema
        #Llegaron a A y A las ruteo  
        tiempoPromedioA_AGlobal = cls.sumTiemposPromedioA_A / cant_corridas
        print("Tiempo promedio global de permanencia de una llamada que llego a A y A la ruteo: " +  str (tiempoPromedioA_AGlobal))
        #Llegaron a B y B las ruteo
        tiempoPromedioB_BGlobal = cls.sumTiemposPromedioB_B / cant_corridas
        print("Tiempo promedio global de permanencia de una llamada que llego a B y B la ruteo: " +  str (tiempoPromedioB_BGlobal))
        #Se desviaron de A y B las ruteo
        tiempoPromedioA_BGlobal = cls.sumTiemposPromedioA_B / cant_corridas
        print("Tiempo promedio global permanencia de una llamada que la desvio A y B la ruteo: " +  str (tiempoPromedioA_BGlobal))
        #Tiempo promedio en cola global
        #Llegaron a A y A las ruteo
        tPromedioColaA_AGlobal = cls.sumTPromedioColaA_A / cant_corridas
        print("Tiempo promedio global en cola de una llamada que llego a  A y A la ruteo: " + str (tPromedioColaA_AGlobal))
        #Llegaron a B y B las ruteo 
        tPromedioColaB_BGlobal = cls.sumTPromedioColaB_B / cant_corridas
        print("Tiempo promedio global en cola de una llamada que llego a  B y B la ruteo: " + str (tPromedioColaB_BGlobal))
        #Se desviaron de A y B las ruteo
        tPromedioColaA_BGlobal = cls.sumTPromedioColaA_B / cant_corridas
        print("Tiempo promedio global en cola de una llamada que la desvio A y B la ruteo: " + str (tPromedioColaA_BGlobal))
        #Porcentaje global de llamadas perdidas por B
        porcentajeLlamadasLocalesPerdidasGlobal = cls.sumPorcentajesLlamadasLocalesPerdidas / cant_corridas
        print("Porcentaje global de llamadas perdidas por B: " + str(porcentajeLlamadasLocalesPerdidasGlobal))
        #Eficiencia Global
        #Llegaron a A y A las ruteo
        eficienciaA_AGlobal = cls.sumEficienciaA_A / cant_corridas
        print("Eficiencia global de las llamadas que llegaron a A y A las ruteo: " + str(eficienciaA_AGlobal))
        #Llegaron a B y B las ruteo
        eficienciaB_BGlobal = cls.sumEficienciaB_B / cant_corridas
        print("Eficiencia global de las llamadas que llegaron a B y B las ruteo: " + str(eficienciaB_BGlobal))
        #Se desviaron de A y B las ruteo
        eficienciaA_BGlobal = cls.sumEficienciaA_B / cant_corridas
        print("Eficiencia global de las llamadas que se desviaron de A y B las ruteo: " + str(eficienciaA_BGlobal))    

    @classmethod
    def iniciar(cls):
        cant_corridas = int(sys.argv[1])
        max_time = float(sys.argv[2])
        modo_lonto = False
        delay = 0
        # Analisis de argumentos
        if len(sys.argv) == 5 and sys.argv[3] == "-l":
            modo_lonto = True
            delay = int(sys.argv[4])

        # Ejecutar cant_corridas corridas
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
                cls.imprimirEstadoSimulacion()
            cls.imprimirEstadisticasCorrida(corrida_actual)
            cls.limpiarVariables()
        cls.imprimirEstadisticasGlobales(cant_corridas)


@dataclass(order = True)
#Clase que representa el evento, tiene tipo, inicio y llamada
class Evento:
    nombre_evento = dict()
    nombre_evento[1] = "E1-> Llega llamada externa a  A"
    nombre_evento[2] = "E2-> Llega llamada externa a  B"
    nombre_evento[3] = "E3-> Llega llamada de A a B"
    nombre_evento[4] = "E4-> Termina de atender llamada en A"
    nombre_evento[5] = "E5-> Termina de atender llamada en B"

    def __init__(self, tipo = -1, inicio = -1, llamada = None):
        self.tipo = tipo
        self.inicio = inicio
        self.llamada = llamada

    def __str__(self):
        if self.llamada != None:
            return self.__class__.nombre_evento[self.tipo] + " Inicio: " + str(self.inicio) + " Llamada: " + str(self.llamada)
        return self.__class__.nombre_evento[self.tipo] + " Inicio: " + str(self.inicio)

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
    
    #E1: Llega llamada externa a A.
    def evento1(self):
        Simulacion.reloj = self.inicio
        llamada = Llamada(Simulacion.reloj, origen = 0, tiempoEnCola = 0)
        Simulacion.cantLlamadasA += 1
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
                    Simulacion.cantLlamadasDesviadasA += 1
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

    #E2: Llega llamada externa a B
    def evento2(self):
        Simulacion.reloj = self.inicio
        llamada = Llamada(Simulacion.reloj, 2, 0, 0)
        Simulacion.cantLlamadasB += 1
        if Simulacion.ocupado_B:
            Simulacion.tamanoPromedioB += (Simulacion.reloj - Simulacion.cola_B.ultima_modificacion) * Simulacion.cola_B.size
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
    #E3: Llega llamada de A a B
    def evento3(self):
        Simulacion.reloj = self.inicio
        Simulacion.cantLlamadasB += 1
        if Simulacion.ocupado_B:
            Simulacion.tamanoPromedioB += (Simulacion.reloj - Simulacion.cola_B.ultima_modificacion) * Simulacion.cola_B.size
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
            tiempo_arribo = llamada.tiempo_arribo + 0.5
            e3 = Evento(3, tiempo_arribo, llamada)
            Simulacion.cola_eventos.push(e3)

    #E4:Termina de atenderse llamada en A
    def evento4(self):
        Simulacion.reloj = self.inicio   
        Simulacion.ocupado_A = False
        Simulacion.cantLlamadasA_A += 1
        duracionSistema = Simulacion.reloj - self.llamada.tiempo_arribo
        Simulacion.duracionTotalLlamadasA_A += duracionSistema
        Simulacion.tiempoEnColaTotalA_A += self.llamada.tiempoEnCola
        if self.llamada.tipo == 2 :
            Simulacion.cantLlamadasLocalesRuteadas += 1
            
        if Simulacion.cola_A.size > 0:
            llamada = Simulacion.cola_A.pop()
            llamada.tiempoEnCola = Simulacion.reloj - llamada.tiempo_arribo
            Simulacion.ocupado_A = True
            if llamada.tipo == 1:
                tiempo_atencion = self.TAtencionA1()
            else:
                tiempo_atencion = self.TAtencionA2()
            tiempo_arribo = Simulacion.reloj + tiempo_atencion
            e4 = Evento(4, tiempo_arribo, llamada)
            Simulacion.cola_eventos.push(e4)

    # E5: Termina de atenderse llamada en B
    def evento5(self):
        Simulacion.reloj = self.inicio
        Simulacion.ocupado_B = False
        duracionSistema = Simulacion.reloj - self.llamada.tiempo_arribo
        if self.llamada.tipo == 2:
            Simulacion.cantLlamadasLocalesRuteadas += 1
            if Simulacion.cola_B.size > 4 :
                rand = random.randint(0,9)
                if rand == 0:
                    Simulacion.cantLlamadasPerdidasB += 1
        if self.llamada.origen == 0:
            Simulacion.cantLlamadasB_B += 1
            Simulacion.duracionTotalLlamadasB_B += duracionSistema
            Simulacion.tiempoEnColaTotalB_B += self.llamada.tiempoEnCola
        else:
            Simulacion.cantLlamadasA_B += 1
            Simulacion.duracionTotalLlamadasA_B += duracionSistema
            Simulacion.tiempoEnColaTotalA_B += self.llamada.tiempoEnCola + 0.5          
        if Simulacion.cola_B.size > 0:
            Simulacion.tamanoPromedioB += (Simulacion.reloj - Simulacion.cola_B.ultima_modificacion) * Simulacion.cola_B.size
            Simulacion.cola_B.ultima_modificacion = Simulacion.reloj
            llamada = Simulacion.cola_B.pop()
            llamada.tiempoEnCola = Simulacion.reloj - llamada.tiempo_arribo
            if llamada.tipo == 1:
                tiempo_atencion = self.TAtencionB1()
            else:
                tiempo_atencion = self.TAtencionB2()
            tiempo_arribo = Simulacion.reloj + tiempo_atencion
            e5 = Evento(5, tiempo_arribo, llamada)
            Simulacion.cola_eventos.push(e5)

    #Tiempo de atención de una llamada tipo 1 en el ruteador A
    def TAtencionA1(self):
        r = random.random()
        x = 10 * (5 * r + 4) ** 1 / 2 # ** es el operador de Potenciación en python
        return x
    
    #Tiempo de atención de una llamada de tipo 2 en el ruteador A
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

    # Tiempo entre arribos de A         
    def TEntreArribosA(self):
        esUno = True
        while esUno:
            r = random.random()
            if r != 1:
                esUno = False
        x = - math.log(1 - r) / (2 / 3)
        return x

    # Tiempo de atención de una llamada tipo 1 en el ruteador B 
    def TAtencionB1(self):
        r = random.random()
        if r <= 0.5:
            x = 2 * r
        else:
            x = 3 - 2 * math.sqrt(2 - 2 * r)
        return x

    #Tiempo de atención de una llamada tipo 2 en el ruteador B
    def TAtencionB2(self):
        esUno = True
        while esUno:
            r = random.random()
            if r != 1:
                esUno = False
        x = - math.log(1 - r) / (4 / 3)
        return x
    
    # Tiempo entre arribos de B
    def TEntreArribosB(self):
        r = random.random()
        x = 2 *  r + 1

        return x

#Llamado para iniciar la simulacion
Simulacion.iniciar()