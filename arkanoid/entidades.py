import os
import pygame as pg
from pygame.sprite import Sprite
from . import ALTO, ANCHO, FPS

"""
1. Crear una clase Raqueta
    a. Sea un Sprite -- hecho
    b. Se puede mover. Tendrá un método que se encargue de esto.
    c. Tiene velocidad de movimiento  -- hecho
    d. Tiene que ponder pintarse en pantalla -- hecho
"""


class Raqueta(Sprite):

    margen_inferior = 20
    velocidad = 5
    fps_animacion = 12
    limite_animacion = FPS // fps_animacion
    iteracion = 0

    def __init__(self):
        super().__init__()
        self.imagenes = [
            pg.image.load(
                os.path.join("resources", "images", "electric00.png")
            ),
            pg.image.load(
                os.path.join("resources", "images", "electric01.png")
            ),
            pg.image.load(
                os.path.join("resources", "images", "electric02.png")
            )]
        self.siguiente_imagen = 0
        self.image = self.imagenes[self.siguiente_imagen]
        self.rect = self.image.get_rect(
            midbottom=(ANCHO/2, ALTO-self.margen_inferior))

    def update(self):
        """Actualiza el estado de la raqueta"""

        self.iteracion += 1
        if self.iteracion == self.limite_animacion:
            self.siguiente_imagen += 1
            if self.siguiente_imagen >= len(self.imagenes):
                self.siguiente_imagen = 0
            self.image = self.imagenes[self.siguiente_imagen]
            self.iteracion = 0

        # calcular y establecer la nueva posición
        # en función de la tecla pulsada (si la hay)
        teclas = pg.key.get_pressed()
        if teclas[pg.K_RIGHT]:
            self.rect.x += self.velocidad
            if self.rect.right > ANCHO:
                self.rect.right = ANCHO
        if teclas[pg.K_LEFT]:
            self.rect.x -= self.velocidad
            if self.rect.left < 0:
                self.rect.left = 0


"""
1. Crear una clase Ladrillo -- Done
2. Ladrillo es un Sprite (image, rect, update) -- Done
3. Cargar imagen del ladrillo
4. Posición
"""


class Ladrillo(Sprite):

    def __init__(self, fila, columna):
        super().__init__()
        ruta_verde = os.path.join("resources", "images", "greenTile.png")
        self.image = pg.image.load(ruta_verde)
        self.rect = self.image.get_rect()


class Pelota(Sprite):

    velocidad_x = -7
    velocidad_y = -5

    def __init__(self, posicion):
        super().__init__()
        self.image = pg.image.load(
            os.path.join("resources", "images", "ball1.png")
        )
        self.rect = self.image.get_rect(
            midbottom=posicion)

    def update(self, raqueta, juego_iniciado):
        if not juego_iniciado:
            self.rect = self.image.get_rect(
                midbottom=raqueta.rect.midtop)
        else:
            # calculo de la posición de la pelota
            # en movimiento
            self.rect.x += self.velocidad_x
            # rebote horizontal
            if self.rect.right >= ANCHO or self.rect.left <= 0:
                self.velocidad_x = -self.velocidad_x

            self.rect.y += self.velocidad_y
            # rebote en la parte superior
            if self.rect.top <= 0:
                self.velocidad_y = -self.velocidad_y

            if self.rect.top > ALTO:
                self.pierdes()
                self.reset()

    def pierdes(self):
        print("Has perdido una vida")

    def reset(self):
        print("Volvemos a poner la pelota en la posición inicial")

    def hay_colision(self, otro):
        if self.rect.colliderect(otro):
            # hay colisión
            self.velocidad_y = -self.velocidad_y
