import pygame
import time

def load_animation(path):
    pass

class Animation:
    def __init__(self, imgs:tuple, data:tuple):
        self.imgs = imgs
        self.data = data

        self._layer = 0
        self.frame = 0
        self.pause = False

    @property
    def layer(self):
        return self._layer

    def play(self, dt):
        if self.pause == False:
            self.frame += dt / 10
            if self.frame >= self.data[self.layer]:
                self._layer += 1
                self.frame = 0
                if self._layer >= len(self.imgs):
                    self._layer = 0
            return


