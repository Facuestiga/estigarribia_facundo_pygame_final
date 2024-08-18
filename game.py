import pygame
from personaje import Player
from enemigo import Enemigo
import random

pygame.init()

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO, ALTO])
FPS = 60
FUENTE = pygame.font.SysFont("Comic Sans", 40)

vida = 5
puntos = 0

reloj = pygame.time.Clock()

tiempo_pasado = 0
tiempo_entre_enemigos = 500

jugando = True

player = Player(ANCHO/2, ALTO - 65)

enemigos = []
#enemigos.append(Enemigo(ANCHO/2, 100))

def gestionar_teclas(teclas):
    # if teclas[pygame.K_w]:
    #     player.y -= player.velocidad
    # if teclas[pygame.K_s]:
    #     player.y += player.velocidad
    if teclas[pygame.K_a]:
        player.x -= player.velocidad
    if teclas[pygame.K_d]:
        player.x += player.velocidad

while jugando and vida > 0:
    
    tiempo_pasado += reloj.tick(FPS)
    #print(f"Tiempo pasado: {tiempo_pasado}")
    
    
    if tiempo_pasado > tiempo_entre_enemigos:
        enemigos.append(Enemigo(random.randint(0, ANCHO), -100))
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
    
    for enemigo in enemigos:
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()
        
        if pygame.Rect.colliderect(player.rect, enemigo.rect):
            print(f"Tocando")
            vida -= 1
            print(f"Vidas: {vida}")
            enemigos.remove(enemigo)
        
        if enemigo.y + enemigo.alto > ALTO:
            puntos += 1
            enemigos.remove(enemigo)
        
    VENTANA.blit(texto_vida, (20,20))
    VENTANA.blit(texto_puntos, (20,60))
    pygame.display.update()

quit()