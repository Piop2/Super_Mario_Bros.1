import pygame
import os
from .core_fuc import *

def load_tiles(path):
    tiles = {}
    tiles_animation_data = {}

    tiles_path = os.listdir(path)
    for tile_path in tiles_path:
        if tile_path.split('.')[-1] == 'png':
            tile_img = load_img(f"{path}/{tile_path}")
            tiles[int(tile_path.split('.')[0])] = tile_img

            try:
                data = read_f(tile_path.split('.')[0] + '.json')
                tiles_animation_data[int(tile_path.split['.'][0])] = data

            except FileNotFoundError:
                pass
    
    return tiles, tiles_animation_data