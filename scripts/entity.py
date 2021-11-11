import pygame
from .core_fuc import *
from .animation import *

class Entity:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.ani = None
        self._direction = 1
        self.rect = None
        self.__entity_name = "Unkown_Entity"
        return
    
    def __str__(self):
        return self.__entity_name
    
    @property
    def speed(self):
        return self._speed
    
    @property
    def direction(self):
        return self._direction

    def check_rect(self):
        self.rect = self.img.get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        return self.rect

    def turn_direction(self):
        self._direction *= -1
        return
    
    def move(self, gravity):
        return
    
    def play_ani(self, dt):
        self.ani.play(dt)
        return
    
    def render(self, surf, camera_x):
        return


class Mushroom_RED(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = load_img("data/images/entity/Mushroom/Mushroom_Red.png")
        self._speed = 4
        self.acc_y = 0
        self.__entity_name = "mushroom_r"

    def __str__(self):
        return self.__entity_name

    def move(self, gravity):
        self.acc_y += gravity
        return [self.direction * self.speed, self.acc_y]
    
    def play_ani(self, dt):
        return
    
    def render(self, surf, camera_x):
        surf.blit(self.img, (self.pos[0] - camera_x, self.pos[1]))

class Mushroom_GREEN(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = load_img("data/images/entity/Mushroom/Mushroom_GREEN.png")
        self._speed = 4
        self.acc_y = 0
        self.__entity_name = "mushroom_g"

    def __str__(self):
        return self.__entity_name

    def move(self, gravity):
        self.acc_y += gravity
        return [self.direction * self.speed, self.acc_y]
    
    def play_ani(self, dt):
        return
    
    def render(self, surf, camera_x):
        surf.blit(self.img, (self.pos[0] - camera_x, self.pos[1]))

class Fire_Flower(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ani = Animation(*load_animation("data/images/entity/Fire_Flower"))
        self.__entity_name = "fire_flower"
        self.rect = None
    
    def __str__(self):
        return self.__entity_name

    def move(self, _):
        return [0, 0]
    
    def play_ani(self, dt):
        return super().play_ani(dt)
    
    def check_rect(self):
        self.rect = self.ani.get_img().get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        return self.rect

    def turn_direction(self):
        return

    def render(self, surf, camera_x):
        surf.blit(self.ani.get_img(), (self.pos[0] - camera_x, self.pos[1]))
        return