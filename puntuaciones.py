import pygame
import json
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

            with open('puntuaciones.json', 'r') as archivo:
                puntuaciones = json.load(archivo)
                
            puntuaciones_ordenadas = sorted(puntuaciones, key=lambda x: x['puntos'], reverse=True)

            for i, puntuacion in enumerate(puntuaciones_ordenadas):
                texto = self.fuente.render(f"{puntuacion['nombre']}: {puntuacion['puntos']}", True, (255, 255, 255))
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

    @staticmethod
    def guardar_puntuacion(nombre, puntos):
        try:
            with open('puntuaciones.json', 'r') as archivo:
                puntuaciones = json.load(archivo)
        except FileNotFoundError:
            puntuaciones = []

        puntuaciones.append({"nombre": nombre, "puntos": puntos})

        with open('puntuaciones.json', 'w') as archivo:
            json.dump(puntuaciones, archivo, indent=4)
