import pygame

class Bala():
    def __init__(self, x, y, velocidad_y=8, enemy_shoot=False):
        self.x = x
        self.y = y
        self.ancho = 20
        self.alto = 20
        self.velocidad_y = velocidad_y
        self.enemy_shoot = False
        self.color = "white"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load(r"assets\bullet\bullet.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
    
    """ 
    Brief: funcion que dibuja la bala en la pantalla
    Param: ventana(la ventana en donde se dibujara la bala)
    """
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))
        
    """ 
    Brief: funcion que realiza el movimiento. Aumenta en el eje y si la bala es lanzada desde el enemgio.
    Disminuye en el eje y  si la bala es lanzada por el jugador.
    Param: is_enemy: bool (indica si la bala es dispara por el enemigo)
    """
    def movimiento(self, is_enemy=False):
        if not is_enemy and self.enemy_shoot == False:    
            self.y -= self.velocidad_y
            self.rect.y = self.y
            self.enemy_shoot = False
        else:
            self.y += self.velocidad_y
            self.rect.y = self.y
            self.enemy_shoot = True