from constants import ALTO, ANCHO
if __name__ == "__main__":
    import pygame
    from main_menu import MainMenu
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    
    menu = MainMenu( ANCHO, ALTO)
    menu.iniciar()

    pygame.quit()

