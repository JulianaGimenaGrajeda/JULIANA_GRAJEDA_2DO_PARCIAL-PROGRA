import pygame
import json
from datos import * 
from constantes import *

def enlistar_datos(lista:list,clave:str):
    '''Toma los datos de una lista y los 
    agrega a otra en base a una clave
    parametro. Lista a trabajar, 
    clave de la cual se traeran los 
    datos.
    Retorno: Nueva lista con los datos.
    '''
    lista_nueva = []

    for dicc in lista:
        lista_nueva.append(dicc[clave])

    return lista_nueva

def dibujar_rects(pantalla):
    i = 0
    a = 0

    for color in LISTA_COLORES:
        pygame.draw.rect(pantalla,color,(300+108*i,420,100,80),border_radius=15)
        i += 1
        pygame.draw.rect(pantalla,color,(300+108*a,580,100,80),border_radius=15)
        a += 1

def configurar_imagen(archivo:str,tamaño:tuple):
    archivo = pygame.image.load(archivo)
    archivo = pygame.transform.scale(archivo,tamaño)
    return archivo

def cambiar_posicion(posicion,lista:str):
    '''Recibe un valor numérico, en este caso
    la posicion y aumenta su valor siempre
    y cuando sea menor al tamaño de una  lista
    menos 1.
    Parámetros: Posicion o valor numérico y
    lista a comparar.
    Retorno: Posicion con el valor sumado'''
    if posicion < len(lista)-1:
        posicion += 1
    else:
        posicion = 0

    return posicion

def crear_archivo():
    try:
        with open(RUTA_PUNTAJE,'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def cargar_puntaje(nombre_jugador,puntaje_jugador):
    puntaje = crear_archivo()
    puntaje.append({'nombre':nombre_jugador,'puntaje':puntaje_jugador})

    with open(RUTA_PUNTAJE,'w') as archivo:
        json.dump(puntaje,archivo,indent=4)

def obtener_mejores_puntajes(n=10):
    puntajes = crear_archivo()
    puntajes_ordenados = sorted(puntajes, key=lambda x:x['puntaje'],reverse=True)
    return puntajes_ordenados[:n]

def mostrar_puntajes(fuente,pantalla):
    mejores_puntajes = obtener_mejores_puntajes()
    ubicacion_y = 100
    for puntaje in mejores_puntajes:
        nombre = puntaje["nombre"]
        puntos = puntaje["puntaje"]
        texto_puntaje = fuente.render(f"{nombre}: {puntos}",True,COLOR_NEGRO)
        pantalla.blit(texto_puntaje,(450,ubicacion_y))
        ubicacion_y += 40