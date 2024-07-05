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

pygame.init()
pygame.mixer.init()

#CONFIGURACIÓN VENTANA
pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)
pygame.display.set_caption("Carrera de Mentes")

logo = configurar_imagen(RUTA_IMAGEN+"logo.png",(350,350))
pygame.display.set_icon(logo)

#IMÁGENES
flecha_a = configurar_imagen(RUTA_IMAGEN+"flecha_a.png",(116,80))
flecha_b = configurar_imagen(RUTA_IMAGEN+"flecha.png",(250,150))
utn = configurar_imagen(RUTA_IMAGEN+"utn.png",(220,190))

#SONIDOS
sonido_error = pygame.mixer.Sound(RUTA_SONIDO+"daño.wav")
sonido_correcto = pygame.mixer.Sound(RUTA_SONIDO+"correcto.wav")

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

#PERSONAJE
personaje = configurar_imagen(RUTA_IMAGEN + "chloe.png",(150, 150))
rect_personaje = personaje.get_rect()

direccion = 0

bandera_avanzar = False
bandera_retroceder = False

posicion_actual = list(LISTA_POSICIONES[direccion])
rect_personaje.topleft = posicion_actual
posicion_x = rect_personaje.x
posicion_y = rect_personaje.y


#RELOJ
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)
reloj = 5

#Variables de estado del juego
posicion = 0
puntos = 0

#Ingreso
fuente_txt = pygame.font.SysFont("Monocraft", 20)
ingreso = ""
ingreso_rect = pygame.Rect(486, 386, 250, 50)
#tabla puntajes
table_txt = fuente_puntaje.render("Tabla de puntos: ",True,COLOR_VIOLETITA)
nombre_txt = fuente_txt.render("Ingrese su nombre: ",True,COLOR_NEGRO)

#BANDERAS
bandera_correcta = False
bandera_incorrecta = False
bandera_comenzar = False
bandera_finalizar = False
bandera_fin_ingreso = False
bandera_fin_juego = False

#Inicializa variables de juego
correr = True

while correr:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = event.pos
            print(click)

            if btn_pregunta.collidepoint(click):
                bandera_comenzar = True
                puntos = 0
                posicion = 0
                reloj = 5
                bandera_fin_ingreso = False
                bandera_finalizar = False
                bandera_fin_juego = False
                ingreso = ""
                #PERSONAJE
                direccion = 0
                posicion_actual = list(LISTA_POSICIONES[direccion])
                rect_personaje.topleft = posicion_actual
                posicion_x = rect_personaje.x
                posicion_y = rect_personaje.y
            elif btn_reinicio.collidepoint(click):
                bandera_comenzar = False
                bandera_finalizar = True
            elif bandera_comenzar:
                if correcta == 'a':
                    if btn_a.collidepoint(click):
                        bandera_correcta = True
                    elif btn_b.collidepoint(click) or btn_c.collidepoint(click):
                        bandera_incorrecta = True
                elif correcta == 'b':
                    if btn_b.collidepoint(click):
                        bandera_correcta = True
                    elif btn_a.collidepoint(click) or btn_c.collidepoint(click):
                        bandera_incorrecta = True
                elif correcta == 'c':
                    if btn_c.collidepoint(click):
                        bandera_correcta = True
                    elif btn_a.collidepoint(click) or btn_b.collidepoint(click):
                        bandera_incorrecta = True
        if event.type == TIMER_EVENT:
            if bandera_comenzar:
                reloj -= 1
                if reloj < 0:
                    bandera_incorrecta = True
        if event.type == pygame.KEYDOWN:
            if bandera_finalizar and not bandera_fin_ingreso:
                if event.key == pygame.K_BACKSPACE:
                    ingreso = ingreso[:-1]  # Borra el último carácter
                else:
                    ingreso += event.unicode
                    print(ingreso)
                if event.key == pygame.K_INSERT:
                    bandera_fin_ingreso = True
                    cargar_puntaje(ingreso, puntos)

    if bandera_correcta:
        puntos += 10
        posicion = cambiar_posicion(posicion, lista_preguntas)
        reloj = 5
        #MOVIMIENTO
        direccion += 2
        bandera_avanzar = True
        sonido_correcto.play()

        bandera_correcta = False
    elif bandera_incorrecta:
        puntos -= 5
        posicion = cambiar_posicion(posicion, lista_preguntas)
        reloj = 5
        #MOVIMIENTO
        direccion -= 1
        bandera_retroceder = True
        sonido_error.play()
        bandera_incorrecta = False

    #MANEJO PERSONAJE
    if bandera_avanzar:
        if direccion > len(lista):
            direccion = 17
            bandera_fin_juego = True
        elif direccion == 7:
            direccion += 1
        elif direccion == 13:
            direccion -= 1

        posicion_actual = list(LISTA_POSICIONES[direccion])
        rect_personaje.topleft = posicion_actual
        bandera_avanzar = False

    elif bandera_retroceder:
        if direccion <= 0:
            direccion = 0
        
        posicion_actual = list(LISTA_POSICIONES[direccion])
        rect_personaje.topleft = posicion_actual
        bandera_retroceder = False

    if  bandera_fin_juego:
        bandera_finalizar = True
        bandera_comenzar = False

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

    for color in LISTA_COLORES:
        pygame.draw.rect(pantalla,color,(300+108*i,420,100,80),border_radius=15)
        i += 1
        pygame.draw.rect(pantalla,color,(300+108*a,580,100,80),border_radius=15)
        a += 1

    #BOTONES
    btn_reinicio = pygame.draw.rect(pantalla,COLOR_BTN,(BTN_REINICIO))
    btn_a = pygame.draw.rect(pantalla, COLOR_BTN, (POS_A), border_radius=15)
    btn_b = pygame.draw.rect(pantalla, COLOR_BTN, (POS_B), border_radius=15)
    btn_c = pygame.draw.rect(pantalla, COLOR_BTN, (POS_C), border_radius=15)

    #DIBUJAR EN PANTALLA
    if bandera_comenzar:
        pantalla.blit(preguntas,(379, 36))
        pantalla.blit(respuesta_a, (400, 130))
        pantalla.blit(respuesta_b, (697, 130))
        pantalla.blit(respuesta_c, (517, 220))

    pantalla.blit(tiempo_txt,(950,200))
    pantalla.blit(tiempito,(950,214))

    pantalla.blit(flecha_a,(170,422))
    pantalla.blit(flecha_b,(1080,473))
    pantalla.blit(logo,(0,0))
    pantalla.blit(avanza,(958,457))
    pantalla.blit(retrocede,(627,611))
    pantalla.blit(utn,(100,505))

    pantalla.blit(boton_reinicio,(700,730))
    pantalla.blit(puntos_txt,(950,90))
    pantalla.blit(puntaje,(950,130))

    pantalla.blit(personaje,rect_personaje)

    if bandera_finalizar and not bandera_comenzar:
        pantalla.fill(COLOR_PANTALLA)
        pantalla.blit(table_txt,(411,41))

        if not bandera_fin_ingreso:
            recuadro = pygame.draw.rect(pantalla,COLOR_CELESTE,(RECUADRO))
            pantalla.blit(nombre_txt,(498,328))
            # Dibuja el cuadro de ingreso de texto
            pygame.draw.rect(pantalla,COLOR_BLANCO,ingreso_rect)
            texto_superficie = fuente_txt.render(ingreso, True, COLOR_NEGRO)
            pantalla.blit(texto_superficie, (ingreso_rect.x + 15, ingreso_rect.y + 15))
        else:
            mostrar_puntajes(fuente_txt,pantalla)

    btn_pregunta = pygame.draw.rect(pantalla,COLOR_BTN,(BTN_PREGUNTA))
    pantalla.blit(boton_pregunta,(440,730))

    pygame.display.flip()
pygame.mixer.quit()
pygame.quit()