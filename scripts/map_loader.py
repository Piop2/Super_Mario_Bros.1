import pygame
import json
from .core_fuc import *
from.animation import Animation

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

    def play_box(self, dt):
        self.maps[self.map_name].play_box(dt)
        return

    def render(self, surf, tiles, camera_x):
        self.maps[self.map_name].render(surf, tiles, camera_x)
        return

class Map:
    def __init__(self, map_data):
        self.map_data = map_data

        self.box_ani = Animation((None, None, None, None), (45, 15, 15, 15))

    def play_box(self, dt):
        self.box_ani.play(dt)

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

        box_ani_num = self.box_ani.layer

        for n, layer in enumerate(self.map_layers):
            for tile in layer:
                tile_pos = str_to_turple(tile)
                if camera_x - 48 <= tile_pos[0] * 48 <= camera_x + 816:
                    tile_type = layer[tile][0]
                    tile_num = layer[tile][1]

                    try:
                        offset_pos = layer[tile][2]
                    except IndexError:
                        offset_pos = (0, 0)

                    if tile_num == 100:
                        item_box_img = clip(tiles[tile_type][100], box_ani_num * 48 + box_ani_num, 0, 48, 48)

                        surf.blit(item_box_img, (tile_pos[0] * 48 - camera_x + offset_pos[0],
                                                               tile_pos[1] * 48 + offset_pos[1]))
                    else:
                        surf.blit(tiles[tile_type][tile_num], (tile_pos[0] * 48 - camera_x + offset_pos[0],
                                                           tile_pos[1] * 48 + offset_pos[1]))
