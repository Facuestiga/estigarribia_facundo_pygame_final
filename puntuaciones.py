import pygame
import sys

class Puntuaciones:
    def __init__(self, ancho, alto):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Space Invaders - Puntuaciones")
        self.fuente = pygame.font.SysFont("Comic Sans", 40)
        self.reloj = pygame.time.Clock()

    def mostrar(self):
        while True:
            self.ventana.fill((0, 0, 0))

            with open('puntuaciones.txt', 'r') as archivo:
                puntuaciones = archivo.readlines()

            for i, puntuacion in enumerate(puntuaciones):
                texto = self.fuente.render(puntuacion.strip(), True, (255, 255, 255))
                self.ventana.blit(texto, (50, 50 + i * 50))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()
            self.reloj.tick(60)
