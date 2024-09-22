from constants import ALTO, ANCHO
import pygame
from main_menu import MainMenu
if __name__ == "__main__": 
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    
    menu = MainMenu(ANCHO, ALTO)
    menu.iniciar()

    pygame.quit()

