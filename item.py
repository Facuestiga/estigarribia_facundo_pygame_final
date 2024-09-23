import pygame
import random

class Item():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 20
        self.alto = 20
        self.velocidad = 7
        self.color = "yellow"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load(r"assets\items\health_item.jpg")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        self.imagen = self.imagen.convert_alpha()
    
    """ 
    Brief: funcion que dibuja el item en la pantalla,
    Param: ventana(la ventana donde sera dibujado)
    """
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(ventana, self.color, self.rect)
        #ventana.blit(self.imagen, (self.x, self.y))
    
    """ 
    Brief: funcion que incrementa el valor del eje y del item en funcion de la velocidad
    y actualiza el eje de y del rectangulo segun el eje y del item
    """
    def movimiento(self):
        self.y += self.velocidad
        self.rect.y = self.y