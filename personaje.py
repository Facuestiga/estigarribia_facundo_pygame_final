import pygame
from utils import crear_bala

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 10
        self.color = "red"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(ventana, self.color, self.rect)
        
    def movimiento(self, teclas, ancho_ventana,  balas, ultima_bala, tiempo_entre_balas):
        if teclas[pygame.K_a] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_d] and self.x < ancho_ventana - self.ancho:
            self.x += self.velocidad
        if teclas[pygame.K_SPACE]:
            ultima_bala = crear_bala(self, balas, ultima_bala, tiempo_entre_balas)
        return ultima_bala