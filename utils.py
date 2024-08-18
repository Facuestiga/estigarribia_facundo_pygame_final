import pygame
from bala import Bala
def crear_bala(player, balas, ultima_bala, tiempo_entre_balas):
    if (pygame.time.get_ticks() - ultima_bala) > tiempo_entre_balas:
        balas.append(Bala(player.rect.centerx, player.rect.centery))
        ultima_bala = pygame.time.get_ticks()
    return ultima_bala