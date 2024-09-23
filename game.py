import pygame
import sys
from personaje import Player
from enemigo import Enemigo
from item import Item
from jefe import Jefe
from pausa_menu import PausaMenu
from puntuaciones import Puntuaciones
from textbox import Textbox
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
        self.jefe = None 
        self.jefe_derrotado = False
        self.balas_enemigas_jefe = []
        self.items = []
        self.tiempo_pasado_items = 0
        self.tiempo_entre_items = 10000
        self.suma_puntos = True


    """ 
    Brief: funcion que se encarga de gestionar las teclas presionadas durante la partida
    Param: teclas(lista de teclas presionadas)
    """
    def gestionar_teclas(self, teclas):
        self.ultima_bala = self.player.movimiento(teclas, ANCHO, self.balas, self.ultima_bala, self.tiempo_entre_balas)
        if teclas[pygame.K_p]:
            self.mostrar_pausa()

    """
    Brief: funcion que muestra el menu de pausa al presionar la teclas 'P'
    """
    def mostrar_pausa(self):
        pausa_menu = PausaMenu(VENTANA, ANCHO, ALTO)
        pausa_menu.iniciar(self)
    
    """
    Brief: funcion que muestra el menu principal
    """
    def mostrar_menu_principal(self):
        from main_menu import MainMenu
        menu_principal = MainMenu(VENTANA,ANCHO, ALTO) 
        menu_principal.iniciar()

    """
    Brief: funcion que verifica el nivel en el se encuentra el juegos y crea una instancia del Jefe
        segun los parametros deseados. El jugador no puede sumar puntos si el Jefe esta activo.
        Los enemigos derrotados son reinicializados a 0 hasta pasar al siguiente nivel
    """
    def verificar_nivel(self):
        if self.nivel == 1 and not self.jefe:
            if self.enemigos_derrotados >= 2:
                self.jefe = Jefe(ANCHO // 2 - 25, 60, vida=1, velocidad_x=5)
                self.suma_puntos = False
                self.enemigos_derrotados = 0
        
        elif self.nivel == 2 and not self.jefe:
            if self.enemigos_derrotados >= 5:
                self.jefe = Jefe(ANCHO // 2 - 25, 60, vida=1, velocidad_x=7)
                self.suma_puntos = False
                self.enemigos_derrotados = 0;
        
        elif self.nivel == 3 and not self.jefe:
            if self.enemigos_derrotados >= 8:
                self.jefe = Jefe(ANCHO // 2 - 25, 60, vida=1, velocidad_x=10) 
                self.suma_puntos = False
                self.enemigos_derrotados = 0

    """ 
    Brief: funcion que se encarga de spawnear a los enemigos en una posicion random.
        Spawnean entre los valores del ancho de la pantalla y -100 pixeles por encima del alto de la pantalla
    """
    def spawn_enemigo(self):
        enemigo_x = random.randint(0, ANCHO - 50)
        self.enemigos.append(Enemigo(enemigo_x, -100))
        self.tiempo_pasado = 0
        
    def spawn_item(self):
        item_x = random.randint(0, ANCHO - 20)
        self.items.append(Item(item_x, -100))
        self.tiempo_pasado_items = 0
        
        

    """
    Brief: function que actualiza para el juego esta corriendo.
    Actualiza dentro de la pantalla los enemgios, colision con el jugador,
    suma de puntos, actualiza al jefe si esta vivo, colisiones de balas enemigas con jugador y viceversa,
    
    """
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
                if self.jefe is not None:
                    if pygame.Rect.colliderect(bala.rect, self.jefe.rect):
                        self.jefe.recibir_impacto()
                        self.balas.remove(bala)
                        if not self.jefe.esta_vivo():
                            self.suma_puntos = True
                            self.jefe = None  # eliminar al jefe
                            self.nivel += 1
                            if self.nivel == 3:
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
    
    
        for item in self.items:
            item.dibujar(VENTANA)
            item.movimiento()
            
            if item.y > ALTO:
                self.items.remove(item)

            if pygame.Rect.colliderect(self.player.rect, item.rect):
                if self.vida != 3:
                    SONIDO_COLISION_VIDA_ITEM.play()
                    self.vida += 1
                self.items.remove(item)
                
                
        
        texto_vida = FUENTE.render(f"Vidas: {self.vida}", True, "white")
        texto_puntos = FUENTE.render(f"Puntos: {self.puntos}", True, "white")
        VENTANA.blit(texto_vida, (20, 20))
        VENTANA.blit(texto_puntos, (20, 60))
        pygame.display.update()


    """ 
    Brief. funcion que se encarga de correr el juego mientra el jugador este jugando y la vida sea mayor a 0.
    Se encarga de spawnear a los enemigos, gestionar las teclas, actualizar la pantalla, verifica el nivel,
    y finalizar la partida si la vida es igual a 0
    """
    def run(self):
        while self.jugando and self.vida > 0:
            tiempo_transcurrido = self.reloj.tick(FPS)
            self.tiempo_pasado += tiempo_transcurrido
            self.tiempo_pasado_items  += tiempo_transcurrido
          
            if self.nivel == 2:
                self.tiempo_entre_enemigos = 400  
            elif self.nivel == 3:
                self.tiempo_entre_enemigos = 370
            
            if self.tiempo_pasado > self.tiempo_entre_enemigos:
                self.spawn_enemigo()
            
            if self.nivel in [2, 3]:  
                if self.tiempo_pasado_items > self.tiempo_entre_items:
                    self.spawn_item()

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
        
        
    """ 
    Brief: funcion que reinicia los valores del juego.
    """
    def reiniciar(self):
        pygame.display.set_caption("Space Invaders - F.Estigarribia")
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
    
   
    def game_over(self):
        textbox = Textbox(350, 320, 300, 50, FUENTE)
        ingreso_nombre = True
        while ingreso_nombre:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            
            nombre = textbox.manejar_eventos(eventos)
            if nombre is not None:
                Puntuaciones.guardar_puntuacion(nombre, self.puntos)
                ingreso_nombre = False
            VENTANA.fill("black")
            textbox.dibujar(VENTANA)
            mensaje = FUENTE.render("Ingrese su nombre: ", True, "white")
            VENTANA.blit(mensaje, (350, 250))
            pygame.display.flip()
        self.jugando = False
        self.mostrar_menu_principal()



# nombre = input("Ingresa tu nombre: ")

# with open('puntuaciones.txt', 'a') as archivo:
#     nombre = nombre.lower()
#     nombre = nombre.capitalize()
#     archivo.write(f"{nombre} - {puntos}\n")
#quit()