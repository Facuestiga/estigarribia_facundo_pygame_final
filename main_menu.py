import sys
import pygame
from game import Game
from puntuaciones import Puntuaciones

class MainMenu:
    def __init__(self, ancho, alto):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Main Menu")
        self.reloj = pygame.time.Clock()
        self.menu_activo = True  # Flag para controlar el bucle del menú

    def dibujar_boton(self, texto, pos):
        fuente = pygame.font.SysFont("Arial", 50)
        superficie_texto = fuente.render(texto, True, "White")
        rect_texto = superficie_texto.get_rect(center=pos)
        self.ventana.blit(superficie_texto, rect_texto)
        return rect_texto

    def iniciar(self):
        while self.menu_activo:
            self.ventana.fill((0, 0, 0))

            jugar_boton = self.dibujar_boton("Jugar", (self.ancho // 2, 250))
            ajustes_boton = self.dibujar_boton("Ajustes", (self.ancho // 2, 350))
            puntuaciones_boton = self.dibujar_boton("Puntuaciones", (self.ancho // 2, 450))
            salir_boton = self.dibujar_boton("Salir", (self.ancho // 2, 550))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.menu_activo = False
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if jugar_boton.collidepoint(evento.pos):
                        game = Game()
                        game.run()
                        if not pygame.get_init():  # Verifica si Pygame sigue inicializado
                            self.menu_activo = False
                            break
                    if ajustes_boton.collidepoint(evento.pos):
                        pass  # Aquí se implementarán los ajustes en el futuro
                    if puntuaciones_boton.collidepoint(evento.pos):
                        puntuaciones = Puntuaciones(self.ancho, self.alto)
                        puntuaciones.mostrar()
                    if salir_boton.collidepoint(evento.pos):
                        self.menu_activo = False
                        pygame.quit()
                        sys.exit()

            if self.menu_activo:
                pygame.display.update()
                self.reloj.tick(60)


    
