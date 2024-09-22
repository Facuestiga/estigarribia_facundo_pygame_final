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
        self.imagen = pygame.image.load(r"assets\player_ship\nave.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        self.imagen = pygame.transform.rotate(self.imagen, 90)

    """
    Brief: funcion que se encarga de dibujar la nave del jugador en la pantalla
    """    
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))
      
    """ 
    Brief: funcion que se encarga de gestionar el movimiento del personaje y crear una bala cuando el jugador presioa 'SPACE'
    Param: teclas(lista de teclas presionadas), ancho_ventana(limite de ancho de ventana para el movimiento del personaje),
        balas(lista de balas creadas en el juego), ultima_bala(tiempo en el que se creo la ultima bala), tiempo_entre_balas(espacio de tiempo
        para poder crear otra bala)
    Return: retorna el tiempo en el que se creo la utlima bala
    """   
    def movimiento(self, teclas, ancho_ventana,  balas, ultima_bala, tiempo_entre_balas):
        if teclas[pygame.K_a] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_d] and self.x < ancho_ventana - self.ancho:
            self.x += self.velocidad
        if teclas[pygame.K_SPACE]:
            ultima_bala = crear_bala(self, balas, ultima_bala, tiempo_entre_balas)
        return ultima_bala