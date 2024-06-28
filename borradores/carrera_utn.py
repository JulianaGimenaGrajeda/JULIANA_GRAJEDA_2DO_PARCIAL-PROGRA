import pygame
from constantes import *
from funciones import *

#Separa set de datos en sub-listas
lista_preguntas = enlistar_datos(lista,"pregunta")
lista_rta_a = enlistar_datos(lista,"a")
lista_rta_b = enlistar_datos(lista,"b")
lista_rta_c = enlistar_datos(lista,"c")
lista_rta_correcta = enlistar_datos(lista,"correcta")
lista_tema = enlistar_datos(lista,"tema")

lista_colores = [COLOR_CARMIN,COLOR_AZUL,COLOR_CELESTE,\
    COLOR_MOSTAZA,COLOR_VERDE,COLOR_VERDEAGUA,COLOR_VIOLETA,\
        COLOR_VIOLETITA]

pygame.init()
pygame.mixer.init()

#CONFIGURACIÓN VENTANA
pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)
pygame.display.set_caption("Carrera de Mentes")

logo = pygame.image.load(RUTA_IMAGEN+"logo.png")
pygame.display.set_icon(logo)
logo = pygame.transform.scale(logo,(350,350))


#IMÁGENES
flecha_a = pygame.image.load(RUTA_IMAGEN+"flecha_a.png")
flecha_a = pygame.transform.scale(flecha_a,(116,80,))
flecha_b = pygame.image.load(RUTA_IMAGEN+"flecha.png")
flecha_b = pygame.transform.scale(flecha_b,(250,150))
utn = pygame.image.load(RUTA_IMAGEN+"utn.png")
utn = pygame.transform.scale(utn,(220,190))

#Inicializa variables de juego
correr = True

#Fuentes
fuente = pygame.font.SysFont("Monocraft",15)
fuente_puntaje = pygame.font.SysFont("Monocraft",40)

#Textos
boton_pregunta = fuente.render("Comenzar",True,COLOR_NEGRO)
boton_reinicio = fuente.render("Finalizar",True,COLOR_NEGRO)
puntos_txt = fuente.render("Puntos: ",True,COLOR_NEGRO)
tiempo_txt = fuente.render("Tiempo: ",True,COLOR_NEGRO)

avanza = fuente.render("Avanza 1",True,COLOR_NEGRO)
retrocede = fuente.render("Retrocede 1",True,COLOR_NEGRO)

#Variables de estado del juego
posicion = 0
puntos = 0
vidas = 2
bandera_incorrecta = False
bandera_comienza = False
bandera_correcta = False
respondida = False
primer_comienzo = True
bandera_perdio = False
bandera_gano = False

#PERSONAJE
personaje = pygame.image.load(RUTA_IMAGEN + "chloe.png")
personaje = pygame.transform.scale(personaje, (150, 150))
rect_personaje = personaje.get_rect()


#tiempo
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # Evento cada segundo (1000 ms)
reloj = 5

while correr:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = event.pos
            print(click)

            if btn_pregunta.collidepoint(click) and not \
                bandera_perdio and not bandera_gano:
                reloj = 5
                #Banderas
                bandera_comienza = True
                if not primer_comienzo:
                    posicion = cambiar_posicion(posicion, lista_preguntas)
                else:
                    primer_comienzo = False
                respondida = False
            elif btn_reinicio.collidepoint(click):
                #Reinicia el juego
                puntos = 0
                posicion = 0
                reloj = 5
                vidas = 2
                #Banderas
                respondida = False
                primer_comienzo = True
                bandera_comienza = False
                bandera_perdio = False
                bandera_gano = False
                fin_tiempo = False
                #PERSONAJE
            elif not respondida and not \
                bandera_perdio and not bandera_gano and bandera_comienza:
                if correcta == 'a':
                    if btn_a.collidepoint(click):
                        bandera_correcta = True
                    elif btn_b.collidepoint(click) or btn_c.collidepoint(click):
                        vidas -= 1
                        bandera_incorrecta = True
                elif correcta == 'b':
                    if btn_b.collidepoint(click):
                        bandera_correcta = True
                    elif btn_a.collidepoint(click) or btn_c.collidepoint(click):
                        vidas -= 1
                        bandera_incorrecta = True
                elif correcta == 'c':
                    if btn_c.collidepoint(click):
                        bandera_correcta = True
                    elif btn_a.collidepoint(click) or btn_b.collidepoint(click):
                        vidas -= 1
                        bandera_incorrecta = True
        if event.type == TIMER_EVENT:
            if bandera_comienza and not respondida and not bandera_perdio and not bandera_gano:
                reloj -= 1
                if reloj <= 0:
                    reloj = "Fin"
                    vidas -= 1
                    respondida = True

    if bandera_correcta == True and not \
        respondida and bandera_perdio == False:
        puntos += 10
        respondida = True
        bandera_correcta = False

    if vidas == 0 and not bandera_perdio:
        bandera_perdio = True


    #Actualiza la pregunta y las respuestas
    pregunta = lista_preguntas[posicion]
    respuesta_A = lista_rta_a[posicion]
    respuesta_B = lista_rta_b[posicion]
    respuesta_C = lista_rta_c[posicion]
    correcta = lista_rta_correcta[posicion]
    tema = lista_tema[posicion]

    #RENDER TEXTO(CONVERTIR TEXTO A IMAGEN)
    preguntas = fuente.render(str(pregunta), True, COLOR_BLANCO)
    respuesta_a = fuente.render(str(respuesta_A), True, COLOR_BLANCO)
    respuesta_b = fuente.render(str(respuesta_B), True, COLOR_BLANCO)
    respuesta_c = fuente.render(str(respuesta_C), True, COLOR_BLANCO)
    puntaje = fuente_puntaje.render(str(puntos),True,COLOR_NEGRO)
    tiempito = fuente_puntaje.render(str(reloj),True,COLOR_NEGRO)

    #RELLENAR PANTALLA
    pantalla.fill(COLOR_PANTALLA)

    #RECTÁNGULOS
    pygame.draw.rect(pantalla,COLOR_PANTALLITA,(POS_RECT_PANTALLITA))

    i = 0
    a = 0

    for color in lista_colores:
        pygame.draw.rect(pantalla,color,(300+108*i,420,100,80),border_radius=15)
        i += 1
        pygame.draw.rect(pantalla,color,(300+108*a,580,100,80),border_radius=15)
        a += 1

    #BOTONES
    btn_pregunta = pygame.draw.rect(pantalla,COLOR_BTN,(420,700,150,70))
    btn_reinicio = pygame.draw.rect(pantalla,COLOR_BTN,(675,700,150,70))
    btn_a = pygame.draw.rect(pantalla, COLOR_BTN, (POS_A), border_radius=15)
    btn_b = pygame.draw.rect(pantalla, COLOR_BTN, (POS_B), border_radius=15)
    btn_c = pygame.draw.rect(pantalla, COLOR_BTN, (POS_C), border_radius=15)

    #DIBUJAR EN PANTALLA
    if bandera_comienza:
        pantalla.blit(preguntas,(379, 36))

        if respondida != True and bandera_perdio != True:
            pantalla.blit(respuesta_a, (400, 130))
            pantalla.blit(respuesta_b, (697, 130))
            pantalla.blit(respuesta_c, (517, 220))

    pantalla.blit(puntos_txt,(950,90))
    pantalla.blit(puntaje,(950,130))
    pantalla.blit(tiempo_txt,(950,200))
    pantalla.blit(tiempito,(950,214))

    pantalla.blit(flecha_b,(1080,473))
    pantalla.blit(flecha_a,(170,422))
    pantalla.blit(logo,(0,0))
    pantalla.blit(avanza,(958,457))
    pantalla.blit(retrocede,(627,611))
    pantalla.blit(utn,(100,505))
    pantalla.blit(personaje, rect_personaje.topleft)

    pantalla.blit(boton_pregunta,(440,730))
    pantalla.blit(boton_reinicio,(700,730))

    pygame.display.flip()
pygame.mixer.quit()
pygame.quit()
