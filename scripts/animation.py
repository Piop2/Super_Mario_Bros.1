import pygame
import time
from .core_fuc import *

def load_animation(path):
    img = load_img(f"{path}/img.png")
    config = read_f(f"{path}/config.json")

    imgs = []
    durations = []
    for layer in config:
        x = config[layer]["x"]
        y = config[layer]["y"]
        w = config[layer]["w"]
        h = config[layer]["h"]
        d = config[layer]["d"]

        imgs.append(clip(img, x, y, w, h))
        durations.append(d)
    return imgs, durations


class Animation:
    def __init__(self, imgs:tuple, duration:tuple, speed:int=1):
        self.imgs = imgs
        self.duration = duration
        self._speed = speed

        self._layer = 0
        self.frame = 0
        self.pause = False

    @property
    def layer(self):
        return self._layer

    @property
    def speed(self):
        return self._speed

    def set_speed(self, i:int=1):
        self._speed = i
        return

    def play(self, dt):
        if self.pause == False:
            self.frame += dt / 10
            if self.frame >= self.duration[self.layer] / self.speed:
                self._layer += 1
                self.frame = 0
                if self.layer >= len(self.imgs):
                    self._layer = 0
            return

    def get_img(self):
        return self.imgs[self.layer]

