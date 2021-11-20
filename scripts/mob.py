import pygame
from .animation import *

class Mob:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.rect = None
        self.ani = {}
        self.status = "defalt"
        self.direction = -1
        self.speed = 0
    
    def __str__(self):
        return "Mob"
    
    def turn_direction(self):
        self.direction *= -1
        return
    
    def check_rect(self):
        self.rect = self.img.get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        return self.rect
    
    def move(self, gravity):
        return [self.direction * self.speed, gravity]
    

    def get_img(self):
        return self.ani[self.status].get_img()

    def render(self, surf, camera_x):
        surf.blit(self.get_img(), (self.pos[0] - camera_x, self.pos[1]))
        return

class Mushroom_mob(Mob):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ani = {
            "walk": Animation(*load_animation("data/images/mob/mushroom/OverWorld/walk")),
            "push_down": load_img("data/images/mob/mushroom/OverWorld/push_down/img.png")
        }
        self.status = "walk"
        self.speed = 3
    
