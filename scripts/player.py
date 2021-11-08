import pygame
from .core_fuc import *
from .animation import *


class Mario:
    def __init__(self, pos):
        self.ani = {
            "big": {
            },
            "small": {
                "idle": load_img("data/images/character/small_idle/img.png"),
                "jump": load_img("data/images/character/small_jump/img.png")
            }
        }

        self.status = ["small", "idle"]
        self.pos = pos
        self.direction = 1

        self.rect = None
        return

    def look_right(self):
        self.direction = 1
        return

    def look_left(self):
        self.direction = -1
        return

    def get_status_img(self):
        try:
            img = self.ani[self.status[0]][self.status[1]].get_img()
        except:
            img = self.ani[self.status[0]][self.status[1]]
        return img

    def check_rect(self):
        self.rect = self.get_status_img().get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        return self.rect

    def render(self, surf):
        surf.blit(self.get_status_img(), self.pos)
        return