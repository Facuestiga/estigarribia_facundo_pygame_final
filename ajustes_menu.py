import pygame
pygame.init()

class AjustesMenu:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Space Invaders - Ajustes")
        self.volumen = pygame.mixer.music.get_volume() * 100  
        self.reloj = pygame.time.Clock()
        self.ajustes_activo = True
        self.arrastrando_slider = False  

    """
    Brief: funcion que dibuja el slider para el seteo del volumen de la musica
    """
    def dibujar_slider(self, volumen):
        pygame.draw.rect(self.ventana, "White", (self.ancho // 4, self.alto // 2 - 20, self.ancho // 2, 40), 2)
        pygame.draw.rect(self.ventana, "Green", (self.ancho // 4, self.alto // 2 - 20, (self.ancho // 2) * (volumen / 100), 40))

    """ 
    Brief: funcion que dibuja un boton en el menu de ajustes
    Param: texto (texto a mostrar en el boton), pos(posicion donde dibujar el boton)
    Return: retorna el rectangulo del boton    
    """
    def dibujar_boton(self, texto, pos):
        fuente = pygame.font.SysFont("Arial", 40)
        superficie_texto = fuente.render(texto, True, "White")
        rect_texto = superficie_texto.get_rect(center=pos)
        self.ventana.blit(superficie_texto, rect_texto)


    """
    Brief: funcion que actualiza el volumen de la musica
    """
    def actualizar_volumen(self, mouse_x):
        if self.ancho // 4 <= mouse_x <= (self.ancho // 4 + self.ancho // 2):
            self.volumen = ((mouse_x - self.ancho // 4) / (self.ancho // 2)) * 100
            pygame.mixer.music.set_volume(self.volumen / 100)

    def iniciar(self):
        while self.ajustes_activo:
            self.ventana.fill("black")
            self.dibujar_boton("Ajustes", (self.ancho // 2, 100))
            self.dibujar_boton(f"Volumen: {int(self.volumen)}%", (self.ancho // 2, self.alto // 2 - 60))
            self.dibujar_slider(self.volumen)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ajustes_activo = False
                    pygame.quit()
                    exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.ancho // 4 <= evento.pos[0] <= (self.ancho // 4 + self.ancho // 2):
                        self.arrastrando_slider = True
                        self.actualizar_volumen(evento.pos[0])

                if evento.type == pygame.MOUSEBUTTONUP:
                    self.arrastrando_slider = False

                if evento.type == pygame.MOUSEMOTION and self.arrastrando_slider:
                    self.actualizar_volumen(evento.pos[0])

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.ajustes_activo = False  

            pygame.display.update()
            self.reloj.tick(60)
