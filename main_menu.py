import sys
import pygame
from game import Game
from constants import MAIN_MUSIC
from puntuaciones import Puntuaciones
from ajustes_menu import AjustesMenu

class MainMenu:
    def __init__(self, ventana, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ventana = ventana
        pygame.display.set_caption("Space Invaders")
        self.reloj = pygame.time.Clock()
        self.menu_activo = True  # controla el bucle del menú
     

    """ 
    Brief: funcion que dibuja un boton en el menu
    Param: texto (texto a mostrar en el boton), pos(posicion donde dibujar el boton)
    Return: retorna el rectangulo del boton    
    """
    def dibujar_boton(self, texto, pos):
        fuente = pygame.font.SysFont("Arial", 50)
        superficie_texto = fuente.render(texto, True, "White")
        rect_texto = superficie_texto.get_rect(center=pos)
        self.ventana.blit(superficie_texto, rect_texto)
        return rect_texto


    """ 
    Brief: funcion que inicial el main menu actualizando la pantalla siempre que el menu este activo.  
    """
    def iniciar(self):
        pygame.mixer.music.load(r'assets/sounds/musica.mp3')
        pygame.mixer.music.play(-1)
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
                        pygame.mixer.music.stop()
                        game = Game()
                        game.run()
                        if not pygame.get_init():  # verifica si Pygame sigue inicializado
                            self.menu_activo = False
                            break
                    if ajustes_boton.collidepoint(evento.pos):
                        ajustes_menu = AjustesMenu(self.ancho, self.alto)
                        ajustes_menu.iniciar()
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



    
