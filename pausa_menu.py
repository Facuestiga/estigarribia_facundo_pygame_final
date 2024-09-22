import sys
import pygame

pygame.init()
class PausaMenu:
    def __init__(self, ventana, ancho, alto):
        pygame.display.set_caption("Space Invaders")
        self.ventana = ventana
        self.ancho = ancho
        self.alto = alto
        self.reloj = pygame.time.Clock()

    """ 
    Brief: funcion que dibuja un boton en el menu de pausa
    Param: texto (texto a mostrar en el boton), pos(posicion donde dibujar el boton)
    Return: retorna el rectangulo del boton    
    """
    def dibujar_boton(self, texto, pos):
        fuente = pygame.font.Font(None, 74)
        texto_render = fuente.render(texto, True, "white")
        texto_rect = texto_render.get_rect(center=pos)
        self.ventana.blit(texto_render, texto_rect)
        return texto_rect

    def iniciar(self, game):
        while True:
            self.ventana.fill((0, 0, 0))

            reanudar_boton = self.dibujar_boton("Renaudar", (self.ancho // 2, 250))
            reiniciar_boton = self.dibujar_boton("Reiniciar", (self.ancho // 2, 350))
            volver_main_menu = self.dibujar_boton("Volver al menu principal", (self.ancho // 2, 450))
            salir_boton = self.dibujar_boton("Salir del Juego", (self.ancho // 2, 550))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if reanudar_boton.collidepoint(evento.pos):
                        return  
                    if reiniciar_boton.collidepoint(evento.pos):
                        game.reiniciar()
                        return
                    if volver_main_menu.collidepoint(evento.pos):
                        game.mostrar_menu_principal()
                    if salir_boton.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.reloj.tick(60)
