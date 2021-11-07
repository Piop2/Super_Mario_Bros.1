import pygame
import json
from .core_fuc import *

MAP_BACKGROUND_COLOR = {
    "OverWorld" : (92, 148, 252),
    "UnderGround" : (0, 0, 0),
    "UnderWater" : (92, 148, 252),
    "Castle" : (0, 0, 0)
}

def str_to_turple(s):
    return tuple([int(v) for v in s.split('.')])


class Level:
    def __init__(self, level_data, maps):
        self.level_data = level_data
        self.maps = maps
        self._map_name = level_data["mapPath"][0]
        return

    @property
    def map_name(self):
        return self._map_name

    @map_name.getter
    def set_map(self, name):
        self._map_name = str(name)
        return self.map_name

    @classmethod
    def load(cls, path):
        level_data = read_f(f"{path}/config.json")

        maps = {}
        for map_path in level_data["mapPath"]:
            maps[map_path.split('.')[0]] = Map(read_f(f"{path}/{map_path.split('.')[0]}.json"))

        return Level(level_data, maps)

    def get_start_data(self):
        return self.maps[self.map_name].camera_x, self.maps[self.map_name].map_size

    def render(self, surf, dt, tiles, camera_x):
        self.maps[self.map_name].render(surf, tiles, camera_x)
        return


class Map:
    def __init__(self, map_data):
        self.map_data = map_data

    @property
    def map_layers(self):
        return self.map_data["map"]

    @property
    def map_type(self):
        return self.map_data["worldType"]

    @property
    def camera_x(self):
        return self.map_data["cameraX"]

    @property
    def map_size(self):
        return self.map_data["mapSize"]

    def render(self, surf, tiles, camera_x):
        surf.fill(MAP_BACKGROUND_COLOR[self.map_type])

        for n, layer in enumerate(self.map_layers):
            for tile in layer:
                tile_pos = str_to_turple(tile)
                if camera_x -48 <= tile_pos[0] * 48 <= camera_x + 272 and - 48 <= tile_pos[1] * 48 <= 240:

                    tile_type = layer[tile][0]
                    tile_num = layer[tile][1]
                    surf.blit(tiles[tile_type][tile_num], (tile_pos[0] * 48 - camera_x, tile_pos[1] * 48))
