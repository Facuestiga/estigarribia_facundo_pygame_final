import pygame
from personaje import Player
from enemigo import Enemigo
from pausa_menu import PausaMenu
from constants import *
import random

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.nivel = 1
        self.vida = 3   
        self.puntos = 0
        self.enemigos_derrotados = 0

        self.reloj = pygame.time.Clock()
        self.tiempo_pasado = 0
        self.tiempo_entre_enemigos = 500
        self.jugando = True

        self.player = Player(ANCHO/2, ALTO - 65)
        self.enemigos = []
        self.balas = []
        self.ultima_bala = 0
        self.tiempo_entre_balas = 250
        self.balas_enemigas = []

    def gestionar_teclas(self, teclas):
        self.ultima_bala = self.player.movimiento(teclas, ANCHO, self.balas, self.ultima_bala, self.tiempo_entre_balas)
        if teclas[pygame.K_p]:
            self.mostrar_pausa()

    def mostrar_pausa(self):
        pausa_menu = PausaMenu(VENTANA, ANCHO, ALTO)
        pausa_menu.iniciar(self)

    def verificar_nivel(self):
        if self.nivel == 1:
            if self.enemigos_derrotados >= 5:
                self.nivel += 1
                self.enemigos_derrotados = 0
                print("¡Nivel 2!")
        
        elif self.nivel == 2:
            if self.puntos >= 70:
                self.nivel += 1
                print("¡Nivel 3!")
        
        elif self.nivel == 3:
            if self.puntos >= 100:
                print("¡Has completado el juego!")

    def spawn_enemigo(self):
        enemigo_x = random.randint(0, ANCHO - 50)
        self.enemigos.append(Enemigo(enemigo_x, -100))
        self.tiempo_pasado = 50

    def actualizar_pantalla(self):
        VENTANA.fill("black")
        self.player.dibujar(VENTANA)
        
        for enemigo in self.enemigos:
            enemigo.dibujar(VENTANA)
            enemigo.movimiento()
            enemigo.disparar(self.balas_enemigas)
            
            if pygame.Rect.colliderect(self.player.rect, enemigo.rect):
                self.vida -= 1
                if self.vida > 0:
                    SONIDO_VIDA_MENOS_PLAYER.play()
                self.enemigos.remove(enemigo)
            
            elif enemigo.y > ALTO:
                if self.nivel != 1:
                    self.puntos += 1
                self.enemigos.remove(enemigo)
            
            for bala in self.balas:
                if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                    SONIDO_MUERTE_ENEMIGO.play()
                    self.puntos += 1
                    self.enemigos_derrotados += 1
                    self.enemigos.remove(enemigo)
                    self.balas.remove(bala)
        
        for bala in self.balas:
            bala.dibujar(VENTANA)
            bala.movimiento()
        
        for bala_enemiga in self.balas_enemigas:
            bala_enemiga.movimiento()
            bala_enemiga.dibujar(VENTANA)
            if bala_enemiga.y > ALTO:
                self.balas_enemigas.remove(bala_enemiga)

            if pygame.Rect.colliderect(self.player.rect, bala_enemiga.rect):
                self.vida -= 1
                self.balas_enemigas.remove(bala_enemiga)
        
        texto_vida = FUENTE.render(f"Vidas: {self.vida}", True, "white")
        texto_puntos = FUENTE.render(f"Puntos: {self.puntos}", True, "white")
        VENTANA.blit(texto_vida, (20, 20))
        VENTANA.blit(texto_puntos, (20, 60))
        pygame.display.update()

    def run(self):
        while self.jugando and self.vida > 0:
            self.tiempo_pasado += self.reloj.tick(FPS)
            
            if self.tiempo_pasado > self.tiempo_entre_enemigos:
                self.spawn_enemigo()

            eventos = pygame.event.get()
            teclas = pygame.key.get_pressed()
            
            self.gestionar_teclas(teclas)
            
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.jugando = False

            self.actualizar_pantalla()
            self.verificar_nivel()

        if self.vida <= 0:
            SONIDO_GAME_OVER.play()
            while pygame.mixer.get_busy():
                pygame.time.delay(100)
            
            # Aquí cerramos el juego después de que el sonido termine.
            pygame.quit()
            return  # Salimos de la función para evitar que se intente actualizar la pantalla después de cerrar

        pygame.quit()
    
    def reiniciar(self):
        self.nivel = 1
        self.vida = 3   
        self.puntos = 0
        self.enemigos_derrotados = 0

        self.tiempo_pasado = 0
        self.jugando = True

        self.player = Player(ANCHO / 2, ALTO - 65)
        self.enemigos = []
        self.balas = []
        self.ultima_bala = 0
        self.balas_enemigas = []

        SONIDO_GAME_OVER.stop()

