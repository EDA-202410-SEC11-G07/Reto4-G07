"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc
import math
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp 

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {}
    control['model'] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos

    # Cargar los vertices
    load_vertex(control)

    # Cargar los arcos
    load_edges(control)

    model.concurrencies(control['model'])

    return control

def load_vertex(control):
    """
    Carga los datos de los vertices
    """
    dir_airports = cf.data_dir + 'airports-2022.csv'
    input_file = csv.DictReader(open(dir_airports), delimiter=';')
    for airport in input_file:
        airport['LATITUD'] = float(airport['LATITUD'].replace(',', '.'))
        airport['LONGITUD'] = float(airport['LONGITUD'].replace(',', '.'))
        airport['ALTITUD'] = float(airport['ALTITUD'].replace(',', '.'))
        model.add_vertex(control['model'], airport)


def load_edges(control):
    """
    Carga los datos de los arcos
    """
    dir_routes = cf.data_dir + 'fligths-2022.csv'
    input_file = csv.DictReader(open(dir_routes), delimiter=';')
    for flight in input_file:
        flight['TIEMPO_VUELO'] = float(flight['TIEMPO_VUELO'])
        model.add_edge(control['model'], flight)



# Funciones de consulta sobre el catálogo

def get_first_last(list):
    filtered = lt.newList("ARRAY_LIST")
    for i in range(1, 6):
        lt.addLast(filtered, lt.getElement(list, i))
    for i in range(-4, 1):
        lt.addLast(filtered, lt.getElement(list, i))
    return filtered


def req_1(control,latitud1, longitud1, latitud2, longitud2):
    """
    Retorna el resultado del requerimiento 1
    """
    itime=get_time()
    aeropuertos_intermedios,distancia_total,total_aeropuertos , vertice_origen, vertice_destino, tiempo_trayecto =  model.req_1(control["model"],latitud1, longitud1, latitud2, longitud2)
    ftine=get_time()
    dtine=round(delta_time(itime, ftine),2)
    print(f"\nEl tiempo que se demora algoritmo en encontrar la solución : {dtine} ms\n")
    return aeropuertos_intermedios,distancia_total,total_aeropuertos , vertice_origen, vertice_destino, tiempo_trayecto


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    itime=get_time()
    vertices, weight, mayor_concurrencia =  model.req_3(control["model"])
    ftine=get_time()
    dtine=round(delta_time(itime, ftine),2)
    print(f"\nEl tiempo que se demora algoritmo en encontrar la solución : {dtine} ms\n")
    return vertices, weight, mayor_concurrencia

def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    itime = get_time()
    vertices, weight, mayor_concurrencia = model.req_4(control["model"])
    ftime = get_time()
    dtime = round(delta_time(itime, ftime), 2)
    print(f"\nEl tiempo que se demora el algoritmo en encontrar la solución: {dtime} ms\n")
    return vertices, weight, mayor_concurrencia


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    pass

def req_6(control, m_airports):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    i_time = get_time()
    paths, most_important = model.req_6(control["model"], m_airports)
    f_time = get_time()
    d_time = round(delta_time(i_time, f_time), 2)
    print(f"\nEl tiempo que se demora algoritmo en encontrar la solución : {d_time} ms\n")
    return paths, most_important


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
