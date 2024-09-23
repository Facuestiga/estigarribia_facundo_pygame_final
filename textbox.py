import pygame

class Textbox:
    def __init__(self, x, y, ancho, alto, fuente):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_inactivo = pygame.Color('lightskyblue3')
        self.color_activo = pygame.Color('dodgerblue2')
        self.color = self.color_inactivo
        self.activo = False
        self.texto = ''
        self.fuente = fuente
        self.text_surface = fuente.render(self.texto, True, (255, 255, 255))

    """ 
    Brief: funcion que se encarga de manejar los eventos en el textbox si esta activo
    Param: eventos(lista de eventos)
    Return: retorna el texto ingresado por el usuario
    """
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(evento.pos):
                    self.activo = True
                    self.color = self.color_activo
                else:
                    self.activo = False
                    self.color = self.color_inactivo
            if evento.type == pygame.KEYDOWN:
                if self.activo:
                    if evento.key == pygame.K_RETURN:
                        return self.texto
                    elif evento.key == pygame.K_BACKSPACE:
                        self.texto = self.texto[:-1]
                    else:
                        self.texto += evento.unicode
                    self.text_surface = self.fuente.render(self.texto, True, (255, 255, 255))
        return None

    """
    Brief: funcion que dibuja el textbox en la pantalla
    """
    def dibujar(self, pantalla):
        pantalla.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(pantalla, self.color, self.rect, 2)
