import pygame
from .core_fuc import *
from .animation import *


class Mario:
    def __init__(self):
        self.ani = {
            "big": {
                "idle": load_img("data/images/character/big_idle/img.png"),
                "walk": Animation(*load_animation("data/images/character/big_walk")),
                "run": Animation(*load_animation("data/images/character/big_walk"), speed=2),
                "jump": load_img("data/images/character/big_jump/img.png")
            },
            "small": {
                "idle": load_img("data/images/character/small_idle/img.png"),
                "jump": load_img("data/images/character/small_jump/img.png"),
                "walk": Animation(*load_animation("data/images/character/small_walk")),
                "run": Animation(*load_animation("data/images/character/small_walk"), speed=2),
                "turn": load_img("data/images/character/small_change_direction/img.png"),
                "push_wait": load_img("data/images/character/small_push_wait/img.png"),
                "push_down": load_img("data/images/character/small_push_down/img.png")
            },
            "defalt": {
                "dead": load_img("data/images/character/dead/img.png")
            }
        }

        self.status = ["small", "idle"]
        self.pos = [0, 0]
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

    def play_ani(self, dt):
        try:
            self.ani[self.status[0]][self.status[1]].play(dt)
        except:
            pass
        return

    def render(self, surf):
        img = pygame.transform.flip(self.get_status_img(), True, False) if self.direction < 0 else self.get_status_img()
        surf.blit(img, self.pos)
        return