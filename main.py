from main_menu import MainMenu
from constants import ANCHO, ALTO
import pygame

if __name__ == "__main__":
    menu = MainMenu(ANCHO, ALTO )
    menu.iniciar()
    
    if pygame.get_init():
        pygame.display.update()
