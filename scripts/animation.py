import pygame
import time

def load_animation(path):
    pass

class Animation:
    def __init__(self, imgs:tuple, data:tuple):
        self.imgs = imgs
        self.data = data

        self.layer = 0
        self.time = 0
        self.pause = False

    def play(self, dt):
        if self.pause == False:

