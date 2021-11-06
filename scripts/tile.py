import pygame
import os
from .core_fuc import clip

COLORKEY = (147, 187, 236)
TILESETS_PATH = "data/images/tilesets"

def load_tile(path):
    img = pygame.image.load(path)
    img.set_colorkey(COLORKEY)
    return img.copy()

def load_all_tiles():
    pass