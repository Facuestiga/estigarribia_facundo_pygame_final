import pygame
from personaje import Player
from enemigo import Enemigo
from bala import Bala
import random
pygame.init()
ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO, ALTO])
FPS = 60
FUENTE = pygame.font.SysFont("Comic Sans", 40)

vida = 1
puntos = 0

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
#fin funciones

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
    
    #dibujo enemigos
    for enemigo in enemigos:
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()
        
        if pygame.Rect.colliderect(player.rect, enemigo.rect):
            print(f"Tocando")
            vida -= 1
            print(f"Vidas: {vida}")
            enemigos.remove(enemigo)
        
        if enemigo.y > ALTO:
            puntos += 1
            enemigos.remove(enemigo)
        
        #comprobar si las balas colisionan con los rectangulos de los enemigos
        for bala in balas:
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
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

#cierro ventana de pygame
pygame.quit()

nombre = input("Ingresa tu nombre: ")

with open('puntuaciones.txt', 'a') as archivo:
    nombre = nombre.lower()
    nombre = nombre.capitalize()
    archivo.write(f"{nombre} - {puntos}\n")
quit()

