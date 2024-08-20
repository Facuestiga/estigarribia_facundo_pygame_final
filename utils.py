import pygame
from constants import SONIDO_DISPARO
from bala import Bala
def crear_bala(player, balas, ultima_bala, tiempo_entre_balas):
    if (pygame.time.get_ticks() - ultima_bala) > tiempo_entre_balas:
        SONIDO_DISPARO.play()
        balas.append(Bala(player.rect.centerx, player.rect.centery))
        ultima_bala = pygame.time.get_ticks()
    return ultima_bala