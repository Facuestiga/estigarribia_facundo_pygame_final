import pygame
from personaje import Player
from enemigo import Enemigo
from jefe import Jefe
from pausa_menu import PausaMenu
from puntuaciones import Puntuaciones
from constants import *
import random

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Space Invaders - F.Estigarribia")
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
        self.jefe = None #jefe del nivel actual
        self.jefe_derrotado = False
        self.balas_enemigas_jefe = []
        self.suma_puntos = True

    def gestionar_teclas(self, teclas):
        self.ultima_bala = self.player.movimiento(teclas, ANCHO, self.balas, self.ultima_bala, self.tiempo_entre_balas)
        if teclas[pygame.K_p]:
            self.mostrar_pausa()

    def mostrar_pausa(self):
        pausa_menu = PausaMenu(VENTANA, ANCHO, ALTO)
        pausa_menu.iniciar(self)
    
    def mostrar_menu_principal(self):
        from main_menu import MainMenu
        menu_principal = MainMenu(ANCHO, ALTO) 
        menu_principal.iniciar()

    def verificar_nivel(self):
        if self.nivel == 1 and not self.jefe:
            if self.enemigos_derrotados >= 2:
                self.jefe = Jefe(ANCHO // 2 - 25, 60, vida=2, velocidad_x=5)
                self.suma_puntos = False
                self.enemigos_derrotados = 0
        
        elif self.nivel == 2 and not self.jefe:
            if self.enemigos_derrotados >= 5:
                self.jefe = Jefe(ANCHO // 2 - 25, 60, vida=3, velocidad_x=7)
                self.suma_puntos = False
                self.enemigos_derrotados = 0;
        
        elif self.nivel == 3 and not self.jefe:
            if self.enemigos_derrotados >= 8:
                self.jefe = Jefe(ANCHO // 2 - 25, 60, vida=5, velocidad_x=10) 
                self.suma_puntos = False
                self.enemigos_derrotados = 0

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
                self.enemigos.remove(enemigo)
            
            for bala in self.balas:
                if self.suma_puntos:
                    if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                        SONIDO_MUERTE_ENEMIGO.play()
                        self.puntos += 1
                        self.enemigos_derrotados += 1
                        self.enemigos.remove(enemigo)
                        self.balas.remove(bala)
        
        if self.jefe:
            self.jefe.dibujar(VENTANA)
            self.jefe.movimiento()
            self.jefe.disparar(self.balas_enemigas_jefe)
            
            for bala_enemiga in self.balas_enemigas_jefe:
                bala_enemiga.movimiento()
                bala_enemiga.dibujar(VENTANA)
                if bala_enemiga.y > ALTO:
                    self.balas_enemigas_jefe.remove(bala_enemiga)

                if pygame.Rect.colliderect(self.player.rect, bala_enemiga.rect):
                    self.vida -= 1
                    self.balas_enemigas_jefe.remove(bala_enemiga)
                    if self.vida > 0: 
                        SONIDO_COLISION_BALA_ENEMIGA_PLAYER.play()
            
        
            for bala in self.balas:
                if pygame.Rect.colliderect(bala.rect, self.jefe.rect):
                    self.jefe.recibir_impacto()
                    self.balas.remove(bala)
                    if not self.jefe.esta_vivo():
                        self.suma_puntos = True
                        self.jefe = None  # Eliminar al jefe
                        self.nivel += 1
                        if self.nivel == 2:
                            self.vida = min(self.vida + 2, 3) 
                        print(f"¡Has derrotado al jefe del nivel {self.nivel - 1}!")
        
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
                if self.vida > 0: 
                    SONIDO_COLISION_BALA_ENEMIGA_PLAYER.play()
        
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

        if self.vida == 0:
            SONIDO_GAME_OVER.play()
            while pygame.mixer.get_busy():
                pygame.time.delay(100)
                
            self.game_over()
        
        
    
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
        self.jefe = None
        self.suma_puntos = True

        SONIDO_GAME_OVER.stop()


    def obtener_nombre_jugador(self):
        nombre = input("Ingresa tu nombre: ")
        return nombre
    
   
    def game_over(self):
        nombre = self.obtener_nombre_jugador()
        Puntuaciones.guardar_puntuacion(nombre, self.puntos)
        self.jugando = False
        self.mostrar_menu_principal()
    
    def mostrar_menu_principal(self):
        from main_menu import MainMenu
        menu_principal = MainMenu(ANCHO, ALTO)
        menu_principal.iniciar()

# nombre = input("Ingresa tu nombre: ")

# with open('puntuaciones.txt', 'a') as archivo:
#     nombre = nombre.lower()
#     nombre = nombre.capitalize()
#     archivo.write(f"{nombre} - {puntos}\n")
#quit()