import pygame
from .core_fuc import *
from .animation import *

class Entity:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.ani = {}
        self.status = "defalt"
        self._direction = 1
        self._speed = 0
        self.rect = self.check_rect
        return
    
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
    
    def play_ani(self, dt):
        return
    
    def render(self, surf):
        return


class Mushroom_RED(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = load_img("data/images/entity/Mushroom_Red.png")
        self._speed = 3
    
    def render(self, surf, camera_x):
        surf.blit(self.img, (self.pos[0] - camera_x, self.pos[1]))
