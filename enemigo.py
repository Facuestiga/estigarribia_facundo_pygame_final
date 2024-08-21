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
        self.tiempo_entre_balas = random.randint(1000, 3000)
    
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))
        
    def movimiento(self):
        self.y += self.velocidad