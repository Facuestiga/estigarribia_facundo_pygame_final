import pygame
from personaje import Player
from enemigo import Enemigo
from constants import *
import random
pygame.init()
pygame.mixer.init()

nivel = 1
vida = 3   
puntos = 0
enemigos_derrotados = 0

reloj = pygame.time.Clock()

tiempo_pasado = 0
tiempo_entre_enemigos = 500

jugando = True

player = Player(ANCHO/2, ALTO - 65)

enemigos = []
balas = []
ultima_bala = 0
tiempo_entre_balas = 500

#funciones
def gestionar_teclas(teclas):
    global ultima_bala
    ultima_bala = player.movimiento(teclas, ANCHO, balas, ultima_bala, tiempo_entre_balas)
    
# Función para verificar el progreso del nivel
def verificar_nivel():
    global nivel, enemigos_derrotados, puntos
    
    if nivel == 1:
        if enemigos_derrotados >= 5:
            nivel += 1
            enemigos_derrotados = 0
            print("¡Nivel 2!")
    
    elif nivel == 2:
        if puntos >= 70:
            nivel += 1
            print("¡Nivel 3!")
    
    elif nivel == 3:
        if puntos >= 100:
            print("¡Has completado el juego!")

#fin funciones

while jugando and vida > 0:
    
    tiempo_pasado += reloj.tick(FPS)
    #print(f"Tiempo pasado: {tiempo_pasado}")
    
    
    if tiempo_pasado > tiempo_entre_enemigos:
        enemigo_x = random.randint(0, ANCHO -50)
        enemigos.append(Enemigo(enemigo_x, -100))
        tiempo_pasado = 50
    
    eventos = pygame.event.get()
    teclas = pygame.key.get_pressed()
    
    
    texto_vida = FUENTE.render(f"Vidas: {vida}", True, "white")
    texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, "white")
    
    gestionar_teclas(teclas)
    
    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False
    
    VENTANA.fill("black")
    
    player.dibujar(VENTANA)
    
    #dibujo enemigos
    for enemigo in enemigos:
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()
        
        if pygame.Rect.colliderect(player.rect, enemigo.rect):
            print(f"Tocando")
            vida -= 1
            print(f"Vidas: {vida}")
            if vida > 0:
                SONIDO_VIDA_MENOS_PLAYER.play()
            
            enemigos.remove(enemigo)
        
        if enemigo.y > ALTO:
            puntos += 1
            enemigos.remove(enemigo)
        
        #comprobar si las balas colisionan con los rectangulos de los enemigos
        for bala in balas:
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                SONIDO_MUERTE_ENEMIGO.play()
                puntos += 1
                enemigos.remove(enemigo)
                balas.remove(bala)
        
    #dibujo balas
    for bala in balas:
        bala.dibujar(VENTANA)
        bala.movimiento()
        
    VENTANA.blit(texto_vida, (20,20))
    VENTANA.blit(texto_puntos, (20,60))
    pygame.display.update()
    verificar_nivel()
if vida <= 0:
    SONIDO_GAME_OVER.play()
    while pygame.mixer.get_busy():
        pygame.time.delay(100)
#cierro ventana de pygame
pygame.quit()

# nombre = input("Ingresa tu nombre: ")

# with open('puntuaciones.txt', 'a') as archivo:
#     nombre = nombre.lower()
#     nombre = nombre.capitalize()
#     archivo.write(f"{nombre} - {puntos}\n")
#quit()

