import pygame
pygame.init()

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO, ALTO])
FPS = 60
FUENTE = pygame.font.SysFont("Comic Sans", 40)
SONIDO_DISPARO = pygame.mixer.Sound(r"assets\sounds\shoot_sound.wav")
SONIDO_MUERTE_ENEMIGO = pygame.mixer.Sound(r"assets\sounds\enemy_died_fx.wav")
SONIDO_VIDA_MENOS_PLAYER = pygame.mixer.Sound(r"assets\sounds\sound_hit_player.wav")
SONIDO_GAME_OVER = pygame.mixer.Sound(r"assets\sounds\sound_game_over.wav")
SONIDO_COLISION_BALA_ENEMIGA_PLAYER = pygame.mixer.Sound(r"assets\sounds\sound5.mp3")
MAIN_MUSIC = pygame.mixer.music.load(r'assets/sounds/musica.mp3')