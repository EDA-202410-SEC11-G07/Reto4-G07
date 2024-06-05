
"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    data = controller.load_data(control)
    comercial = control['model']['concurrency_comercial']
    charge = control['model']['concurrency_charge']
    militar = control['model']['concurrency_militar']

    print(f"Se cargaron {mp.size(data['model']['hash_airports'])} aeropuertos")
    print(f"Se cargaron {mp.size(data['model']['hash_routes'])} vuelos")

    print("\nAeropuertos de aviación comercial")
    table_comercial = print_tabulate(comercial, ['NOMBRE', 'ICAO', 'CIUDAD', 'concurrency_comercial'])
    print(table_comercial)

    print("\nAeropuertos de aviación de carga")
    table_charge = print_tabulate(charge, ['NOMBRE', 'ICAO', 'CIUDAD', 'concurrency_charge'])
    print(table_charge)

    print("\nAeropuertos de aviación militar")
    table_militar = print_tabulate(militar, ['NOMBRE', 'ICAO', 'CIUDAD', 'concurrency_militar'])
    print(table_militar)
 


def print_tabulate(data_struct, columns):
    data = data_struct

    if lt.isEmpty(data):
        return 'No hay datos'

    #Filtrar solo ultimos y primeros 3 datos si es muy grande la lista
    if lt.size(data_struct) > 10:
        data = controller.get_first_last(data_struct)
        print(f'Se encontraron {lt.size(data_struct)}  resultados. Imprimiendo primeros y ultimos 5...')

    #Lista vacía para crear la tabla
    reduced = []

    #Iterar cada línea de la lista
    for result in lt.iterator(data):
        line = []
        #Iterar las columnas para solo imprimir las deseadas
        for column in columns:
            line.append(result[column])
        reduced.append(line)
    table = tabulate(reduced, headers=columns, tablefmt="grid", maxcolwidths=30)
    return table

def print_tabulate_5(lista, columnas):
    lista = lista["elements"][:40]
    reduced = []
    for result in lista:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla

def print_tabulate_full(lista, columnas):
    lista = lista["elements"]
    reduced = []
    for result in lista:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    latitud1 = float(input("Ingrese la latitud del punto de origen: "))
    longitud1 = float(input("Ingrese la longitud del punto de origen: "))
    latitud2 = float(input("Ingrese la latitud del punto de destino: "))
    longitud2 = float(input("Ingrese la longitud del punto de destino: "))
    aeropuertos_intermedios,distancia_total,total_aeropuertos , vertice_origen, vertice_destino, tiempo_trayecto = controller.req_1(control, latitud1, longitud1, latitud2, longitud2)
    print("-------------------REQ 1 INFO -------------------")
    print( "La distancia total es de: " + str(distancia_total) + " km")
    print("El número de aeropuertos que se visitan en el camino encontrado es de: " + str(total_aeropuertos) + "\n")
    print("-------------------INFO AEROPUETOS -------------------")
    print("Origen: " + vertice_origen['ICAO'] + " - " + vertice_origen['NOMBRE'] + " - " + vertice_origen['CIUDAD'] + " - " + vertice_origen['PAIS'] )
    print("Destino: " + vertice_destino['ICAO'] + " - " + vertice_destino['NOMBRE'] + " - " + vertice_destino['CIUDAD'] + " - " + vertice_destino['PAIS'] + "\n")
    print("-------------------INFO SECUENCIA DE TRAYECTOS -------------------")
    print_tabulate_full(aeropuertos_intermedios, ['ICAO',"Nombre",'Ciudad',"Pais"])
    print("\n" + "El tiempo total del trayecto es de: " + str(tiempo_trayecto) + " minutos o " + str(tiempo_trayecto/60) + " horas"  + "\n")

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    
    vertices, weight, mayor_concurrencia  = controller.req_3(control)
    weight = round(weight,2)
    print("-------------------REQ 3 INFO -------------------")
    print("INFORMACION DEL AEROPUERTO MÁS IMPORTANTE SEGÚN LA CONCURRENCIA COMERCIAL: \n")
    print("Identificador ICAO: " + mayor_concurrencia['ICAO'])
    print("Nombre: " + mayor_concurrencia['NOMBRE'])
    print("Ciudad: " + mayor_concurrencia['CIUDAD'])
    print("pais: " + mayor_concurrencia['PAIS'])
    print("Valor de concurrencia comercial: " + str(mayor_concurrencia['concurrency_comercial']))
    print("Suma de la distancia total de los trayectos: " + str(weight) + " km")
    print("Numero total de trayectos posible: " + str(len(vertices)) + "\n")
    print("-------------------INFO SECUENCIA DE TRAYECTOS -------------------")
    print_tabulate_5(vertices, ['Origen',"Destino",'weight',"Tiempo"])
    
    
def print_req_4(control):
    """
    Función que imprime la solución del Requerimiento 4 en consola
    """
    vertices, weight, mayor_concurrencia = controller.req_4(control)
    weight = round(weight, 2)
    print("-------------------REQ 4 INFO -------------------")
    print("INFORMACION DEL AEROPUERTO MÁS IMPORTANTE SEGÚN LA CONCURRENCIA DE CARGA: \n")
    print("Identificador ICAO: " + mayor_concurrencia['ICAO'])
    print("Nombre: " + mayor_concurrencia['NOMBRE'])
    print("Ciudad: " + mayor_concurrencia['CIUDAD'])
    print("País: " + mayor_concurrencia['PAIS'])
    print("Valor de concurrencia de carga: " + str(mayor_concurrencia['concurrency_comercial']))
    print("Suma de la distancia total de los trayectos: " + str(weight) + " km")
    print("Número total de trayectos posibles: " + str(len(vertices)) + "\n")
    print("-------------------INFO SECUENCIA DE TRAYECTOS -------------------")
    print_tabulate_5(vertices, ['Origen', "Destino", 'weight', "Tiempo"])




def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    m = input("Ingrese el número de aeropuertos a buscar: ")
    paths, most_important = controller.req_6(control, int(m))
    print("Aeropuerto con mayor concurrencia comercial: ")
    print("ICAO: " + most_important['ICAO'] + "\n" + "Nombre: " + most_important['NOMBRE'] + "\n" + "Ciudad: " + most_important['CIUDAD'] + "\n" + "Pais: " + most_important['PAIS'] + "\n" + "Concurrencia: " + str(most_important['concurrency_comercial']) + "\n")
    print("-"*20)
    print("Rutas de los aeropuertos más importantes: \n")
    i = 1
    for info_path in lt.iterator(paths):
        print("-"*100)
        print("RUTA #" + str(i) + "\n")
        print("Total de los aeropuertos en la ruta: " + str(info_path['total_airports']) + "\n")
        print("Aeropuertos en la ruta: \n")
        print_tabulate_5(info_path['airports'], ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS'])
        print("\nVuelos en la ruta: \n")
        print_tabulate_5(info_path['flights'], ['origen', 'destino', 'distancia', ])
        print("\nTotal de distancia recorrida: " + str(info_path['total_distance']) + " KM\n")
        i += 1
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')






        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)
        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
