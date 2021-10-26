import pygame
from .core_fuc import clip

COLORKEY = (147, 187, 236)

def load_tilesets(path):
    img = pygame.image.load(path)
    img.set_colorkey(COLORKEY)
    tiles = []

    offset_x = 0
    offset_y = 0
    for y in range(1, img.get_height() - 16, 16):
        for x in range(1, img.get_width() - 16, 16):
            tiles.append(clip(img, x + offset_x, y + offset_y, 16, 16))
            offset_x += 1

        offset_x = 0
        offset_y += 1
    return tiles