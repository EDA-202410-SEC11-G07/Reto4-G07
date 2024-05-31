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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import folium
from folium.plugins import MarkerCluster
import config as cf
import math
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    model = {
        'graph_comercial_distance': None,
        'graph_comercial_time': None,
        'graph_charge_distance': None,
        'graph_militar_time': None,
        'graph_militar_distance': None,
        'hash_airports': None,
        'hash_routes': None,
        'concurrency_comercial': None,
        'concurrency_charge': None,
        'concurrency_militar': None

        
    }
    model['graph_comercial_distance'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=500)
    model['graph_comercial_time'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=500)
    model['graph_charge_distance'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=500)
    model['graph_militar_time'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=500)
    model['graph_militar_distance'] = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=500)
    model['hash_airports'] = mp.newMap(500, maptype='PROBING')
    model['hash_routes'] = mp.newMap(500, maptype='PROBING')
    model['concurrency_comercial'] = lt.newList('ARRAY_LIST')
    model['concurrency_charge'] = lt.newList('ARRAY_LIST')
    model['concurrency_militar'] = lt.newList('ARRAY_LIST')
    return model



# Funciones para agregar informacion al modelo

def add_vertex(model, vertex):
    """
    Agrega un vertice al grafo
    """
    vertex_name = vertex['ICAO']
    gr.insertVertex(model['graph_comercial_distance'], vertex_name)
    gr.insertVertex(model['graph_comercial_time'], vertex_name)
    gr.insertVertex(model['graph_charge_distance'], vertex_name)
    gr.insertVertex(model['graph_militar_time'], vertex_name)
    gr.insertVertex(model['graph_militar_distance'], vertex_name)
    if not mp.contains(model['hash_airports'], vertex_name):
        vertex['concurrency_comercial'] = 0
        vertex['concurrency_charge'] = 0
        vertex['concurrency_militar'] = 0
        mp.put(model['hash_airports'], vertex_name, vertex)

def add_edge(model, edge):
    """
    Agrega un arco al grafo
    """

    icao_origin = edge['ORIGEN']
    icao_dest = edge['DESTINO']

    vertex_origin = me.getValue(mp.get(model['hash_airports'], icao_origin))
    vertex_dest = me.getValue(mp.get(model['hash_airports'], icao_dest))

    distance = haversine(vertex_origin['LATITUD'], vertex_origin['LONGITUD'], vertex_dest['LATITUD'], vertex_dest['LONGITUD'])
    edge['DISTANCIA'] = distance

    if edge['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
        gr.addEdge(model['graph_comercial_distance'], icao_origin, icao_dest, distance)
        gr.addEdge(model['graph_comercial_time'], icao_origin, icao_dest, edge['TIEMPO_VUELO'])
        vertex_origin['concurrency_comercial'] += 1
        vertex_dest['concurrency_comercial'] += 1
    elif edge['TIPO_VUELO'] == 'AVIACION_CARGA':
        gr.addEdge(model['graph_charge_distance'], icao_origin, icao_dest, distance)
        vertex_origin['concurrency_charge'] += 1
        vertex_dest['concurrency_charge'] += 1
    elif edge['TIPO_VUELO'] == 'MILITAR':
        gr.addEdge(model['graph_militar_time'], icao_origin, icao_dest, edge['TIEMPO_VUELO'])
        gr.addEdge(model['graph_militar_distance'], icao_origin, icao_dest, distance)
        vertex_origin['concurrency_militar'] += 1
        vertex_dest['concurrency_militar'] += 1
    else:
        print('Tipo de vuelo no reconocido')
    
    id_hash = icao_origin + '-' + icao_dest + '-' + edge['TIPO_VUELO']
    mp.put(model['hash_routes'], id_hash, edge)

def concurrencies(data_structs):
    
    list_comercial = data_structs['concurrency_comercial']
    list_cargo = data_structs['concurrency_charge']
    list_militar = data_structs['concurrency_militar']

    list_general = mp.valueSet(data_structs['hash_airports'])

    for airport in lt.iterator(list_general):
        if airport['concurrency_comercial'] > 0:
            lt.addLast(list_comercial, airport)
        if airport['concurrency_charge'] > 0:
            lt.addLast(list_cargo, airport)
        if airport['concurrency_militar'] > 0:
            lt.addLast(list_militar, airport)

    sort_files(list_comercial, 'AVIACION_COMERCIAL')
    sort_files(list_cargo, 'AVIACION_CARGA')
    sort_files(list_militar, 'MILITAR')




def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos en la superficie terrestre
    """
    conversion = math.pi/180
    lat1 = lat1 * conversion
    lon1 = lon1 * conversion
    lat2 = lat2 * conversion
    lon2 = lon2 * conversion

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(dlat/2))**2 + (math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2)
    c = 2 * math.asin(math.sqrt(a))
    d = 6371 * c
    return d





def req_1(data_structs,lat1, long1, lat2, long2):
    """
    Función que soluciona el requerimiento 1
    """
    distancia_total = 0 
    total_aeropuertos = 0
    tiempo_trayecto = 0
    aeropuertos_intermedios = lt.newList("ARRAY_LIST")
    
    hash_airports = data_structs["hash_airports"]
    comercial_graph = data_structs["graph_comercial_distance"]
    vertices = mp.valueSet(hash_airports)

    vertice_origen_full = closest_vertx(vertices, lat1, long1)
    vertice_destino_full = closest_vertx(vertices, lat2, long2)
    vertice_origen = vertice_origen_full["ICAO"]
    vertice_destino = vertice_destino_full["ICAO"]
    search = dfs.DepthFirstSearch(comercial_graph, vertice_destino)
    haspath = dfs.hasPathTo(search, vertice_origen)

    if haspath:
        camino = dfs.pathTo(search, vertice_origen)
        prev = None
        for vertice in lt.iterator(camino):
            total_aeropuertos +=1
            if prev is not None:
                arco = gr.getEdge(comercial_graph, vertice, prev)
                peso = arco["weight"]
                distancia_total += peso
                aeropuerto_info = me.getValue(mp.get(hash_airports, vertice))
                vuelo_info = me.getValue(mp.get(data_structs["hash_routes"], vertice + "-" + prev + "-AVIACION_COMERCIAL"  ))
                info_aeropuerto = {
                        "ICAO": aeropuerto_info["ICAO"],
                        "Nombre": aeropuerto_info["NOMBRE"],
                        "Ciudad": aeropuerto_info["CIUDAD"],
                        "Pais": aeropuerto_info["PAIS"]
                }
                tiempo_trayecto += vuelo_info["TIEMPO_VUELO"]
                lt.addLast(aeropuertos_intermedios,info_aeropuerto)
            else:
                #Para el primer aeropuerto, porque prev = none
                aeropuerto_info = me.getValue(mp.get(hash_airports, vertice))
                info_aeropuerto = {
                        "ICAO": aeropuerto_info["ICAO"],
                        "Nombre": aeropuerto_info["NOMBRE"],
                        "Ciudad": aeropuerto_info["CIUDAD"],
                        "Pais": aeropuerto_info["PAIS"]
                }
                lt.addLast(aeropuertos_intermedios,info_aeropuerto)
            prev = vertice
    
        
    return aeropuertos_intermedios,distancia_total,total_aeropuertos , vertice_origen_full, vertice_destino_full, tiempo_trayecto

            


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
  
    trayectos = lt.newList("ARRAY_LIST")
    
    graph_comercial_distance = data_structs["graph_comercial_distance"]
    
    concurrency_comercial = data_structs["concurrency_comercial"]
    mayor_concurrencia = lt.firstElement(concurrency_comercial)
    
    search = prim.PrimMST(graph_comercial_distance, mayor_concurrencia["ICAO"])
    peso = prim.weightMST(graph_comercial_distance, search)

    subgrafo = gr.newGraph(datastructure="ADJ_LIST", directed = True, cmpfunction = compare_id)
    mst = search["mst"]
    for minicamino in lt.iterator(mst):
        add_vertice(subgrafo, minicamino["vertexA"])
        add_vertice(subgrafo, minicamino["vertexB"])
        add_arco(subgrafo, minicamino["vertexA"], minicamino["vertexB"], minicamino["weight"])
    
    sub_bfs = bfs.BreathFirstSearch(subgrafo, mayor_concurrencia["ICAO"])
    
    lt.deleteElement(concurrency_comercial,1)
    
    for aeropuerto in lt.iterator(concurrency_comercial):
        tiene = bfs.hasPathTo(sub_bfs, aeropuerto["ICAO"])
        if tiene:
            camino = bfs.pathTo(sub_bfs, aeropuerto["ICAO"])
            prev = None
            for vertice in lt.iterator(camino):
                if prev == None:
                    prev = vertice
                else:
                    minipath = {"vertexA" : prev, "vertexB": vertice,"weight" : 0 }
                    prev = vertice
                    v1 = minipath["vertexA"]
                    v2 = minipath["vertexB"]
                    v1_info = me.getValue(mp.get(data_structs["hash_airports"], v1))
                    v2_info = me.getValue(mp.get(data_structs["hash_airports"], v2))
                    lat1_bono = float(v1_info["LATITUD"])
                    long1_bono = float(v1_info["LONGITUD"])
                    lat2_bono = float(v2_info["LATITUD"])
                    long2_bono = float(v2_info["LONGITUD"])
                    minipath["weight"] = haversine(lat1_bono, long1_bono ,lat2_bono, long2_bono)
                    peso += minipath["weight"]
                    vuelo_info = me.getValue(mp.get(data_structs["hash_routes"], v2 + "-" + v1 + "-AVIACION_COMERCIAL"  ))
                    info_trayectos = {
                        "Origen": v1,
                        "Destino": v2,
                        "weight": minipath["weight"],
                        "Tiempo" : vuelo_info["TIEMPO_VUELO"]
                    }
                    lt.addLast(trayectos, info_trayectos)
       
    lt.addFirst(concurrency_comercial, mayor_concurrencia)
    
    return trayectos, peso, mayor_concurrencia





def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    pass


def req_6(data_structs, m_airports):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    list_concurrency_comercial = data_structs['concurrency_comercial']
    most_important = lt.firstElement(list_concurrency_comercial)
    graph_militar_distance = data_structs['graph_militar_distance']
    dijkstra_militar = djk.Dijkstra(graph_militar_distance, most_important['ICAO'])
    paths = lt.newList('ARRAY_LIST')
    i = 2
    
    while lt.size(paths) < m_airports:
        path = djk.pathTo(dijkstra_militar, lt.getElement(list_concurrency_comercial, i)['ICAO'] )
        if path:
            info_path = {
                'total_airports': 1,
                'airports': lt.newList('ARRAY_LIST'),
                'flights': lt.newList('ARRAY_LIST'),
                'total_distance': 0
            }
            for edge in lt.iterator(path):
                dest = edge['vertexB']
                source = edge['vertexA']
                info_path['total_distance'] += edge['weight']
                info_path['total_airports'] += 1
                info_airport_dest = me.getValue(mp.get(data_structs['hash_airports'], dest))
                info_airport_source = me.getValue(mp.get(data_structs['hash_airports'], source))
                if lt.size(info_path['airports']) == 0:
                    lt.addLast(info_path['airports'], info_airport_dest)                
                lt.addLast(info_path['airports'], info_airport_source)
                edge_info = {
                    'destino': dest,
                    'origen': source,
                    'distancia': edge['weight']
                }
                lt.addLast(info_path['flights'], edge_info)
            lt.addLast(paths, info_path)
        i += 1
  
    return paths, most_important



def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass




#FUNCIONES AUXILIARES

def sort_files(data_structs, type):
    """
    Ordena los archivos de acuerdo a un criterio
    """
    if type == 'AVIACION_COMERCIAL':
        merg.sort(data_structs, sort_concurrency_comercial)
    elif type == 'AVIACION_CARGA':
        merg.sort(data_structs, sort_concurrency_charge)
    elif type == 'MILITAR':
        merg.sort(data_structs, sort_concurrency_militar)



def sort_concurrency_comercial(airport1, airport2):
    """
    Ordena los aeropuertos por la cantidad de vuelos comerciales
    """
    c1 = airport1['concurrency_comercial']
    c2 = airport2['concurrency_comercial']
    if c1 > c2:
        return True
    elif c1 < c2:
        return False
    else:
        return airport1['ICAO'] < airport2['ICAO']
    
def sort_concurrency_charge(airport1, airport2):
    """
    Ordena los aeropuertos por la cantidad de vuelos de carga
    """
    c1 = airport1['concurrency_charge']
    c2 = airport2['concurrency_charge']
    if c1 > c2:
        return True
    elif c1 < c2:
        return False
    else:
        return airport1['ICAO'] < airport2['ICAO']

def sort_concurrency_militar(airport1, airport2):
    """
    Ordena los aeropuertos por la cantidad de vuelos militares
    """
    c1 = airport1['concurrency_militar']
    c2 = airport2['concurrency_militar']
    if c1 > c2:
        return True
    elif c1 < c2:
        return False
    else:
        return airport1['ICAO'] < airport2['ICAO']
    
    
def add_vertice(grafo, id_v):
    contains = gr.containsVertex(grafo, id_v)
    if not contains:
        gr.insertVertex(grafo, id_v)
    return grafo

def add_arco(grafo,v1,v2,weigth):
    edge_entry = gr.getEdge(grafo,v1,v2) 
    if edge_entry == None:
        gr.addEdge(grafo,v1,v2,weigth)
    return grafo


def compare_id(data_1, data_2):
    
    if data_1 > me.getKey(data_2):
        return 1
    elif data_1 < me.getKey(data_2):
        return -1
    else:
        return 0
    
def closest_vertx(vertices, lat1, long1):
    closest_vertx = None
    min_distance = None
    for vertice in lt.iterator(vertices):
        lat = vertice["LATITUD"]
        long = vertice["LONGITUD"]
        new_distance = haversine( lat1, long1, lat, long )
        if min_distance == None:
            min_distance = new_distance
        if new_distance < min_distance:
            min_distance = new_distance
            closest_vertx = vertice
    return closest_vertx

