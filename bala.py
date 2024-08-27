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
    
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))
        
    def movimiento(self, is_enemy=False):
        if not is_enemy:    
            self.y -= self.velocidad_y
            self.rect.y = self.y
            self.enemy_shoot = False
        else:
            self.y += self.velocidad_y
            self.rect.y = self.y
            self.enemy_shoot = True