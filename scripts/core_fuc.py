import pygame
import json

COLORKEY = (147, 187, 236)

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def read_f(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def load_img(path):
    img = pygame.image.load(path)
    img.set_colorkey(COLORKEY)
    return img.copy()