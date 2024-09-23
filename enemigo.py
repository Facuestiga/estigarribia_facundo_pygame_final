import pygame
import random
from bala import Bala

class Enemigo():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 5
        self.color = "purple"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load(r"assets\enemy\enemy_androide.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        self.imagen = self.imagen.convert_alpha()
        self.ultima_bala = pygame.time.get_ticks()
        self.tiempo_entre_balas = random.randint(750, 1750)
    
    """ 
    Brief: funcion que dibuja al enemigo en la pantalla,
    Param: ventana(la ventana donde sera dibujado)
    """
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))
    
    """ 
    Brief: funcion que incrementa el valor del eje y del enemigo en funcion de la velocidad
    y actualiza el eje de y del rectangulo segun el eje y del enemigo
    """
    def movimiento(self):
        self.y += self.velocidad
        self.rect.y = self.y
    
    """ 
    Brief: funcion que dibuja una bala del enemigo en un intervalo de tiempo
    """
    def disparar(self, balas):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultima_bala > self.tiempo_entre_balas:
            bala = Bala(self.rect.centerx, self.rect.bottom, velocidad_y=8)
            balas.append(bala)
            bala.movimiento(is_enemy=True)
            self.ultima_bala = ahora