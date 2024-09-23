import pygame
import random
from constants import ANCHO
from bala import Bala

class Jefe():
    def __init__(self, x, y, vida, velocidad_x=5):
        self.x = x
        self.y = y
        self.ancho = 150
        self.alto = 120
        self.vida = vida  
        self.velocidad_x = velocidad_x
        self.color = "violet"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load(r"assets\enemy\boss\monstruo.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        self.imagen = self.imagen.convert_alpha()
        self.ultima_bala = pygame.time.get_ticks()
        self.tiempo_entre_balas = random.randint(800, 1500)

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))
        
    def movimiento(self):
        
        self.x += self.velocidad_x
        if self.x <= 0 or self.x >= ANCHO - self.ancho:
            self.velocidad_x *= -1  # Cambia de dirección al llegar a los bordes
        self.rect.x = self.x  # Actualiza la posición en x
        
    def disparar(self, balas):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultima_bala > self.tiempo_entre_balas:
            # Dispara una bala desde el centro inferior del rectángulo del jefe
            bala = Bala(self.rect.centerx, self.rect.bottom, velocidad_y=8)
            balas.append(bala)
            bala.movimiento(is_enemy=True)
            self.ultima_bala = ahora

    def recibir_impacto(self):
        self.vida -= 1
        print(f"Vida del jefe: {self.vida}")

    def esta_vivo(self):
        return self.vida > 0
