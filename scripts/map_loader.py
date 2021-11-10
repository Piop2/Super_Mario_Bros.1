import pygame
import json
from .core_fuc import *
from.animation import Animation


def str_to_turple(s):
    try:
        t = tuple([int(v) for v in s.split('.')])
    except:
        print(s)
    return t

def tuple_to_str(t):
    return f"{t[0]}.{t[1]}"

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
        return self.maps[self.map_name].camera_x, self.maps[self.map_name].map_size, self.maps[self.map_name].start_at, self.maps[self.map_name].map_type

    def play_box(self, dt):
        self.maps[self.map_name].play_box(dt)
        return
    
    def set_tile(self, x, y, tile_data):
        return self.maps[self.map_name].set_tile(x, y, tile_data)

    def get_rects(self, camera_x, pos):
        return self.maps[self.map_name].get_rects(camera_x, pos)

    def set_offset_tile(self, x, y, camera_x, offset):
        return self.maps[self.map_name].set_offset(x, y, camera_x, offset)


    def set_offset_tile_to_xy(self, x, y, offset):
        return self.maps[self.map_name].set_offset_to_xy(x, y, offset)

    def del_tile_to_xy(self, x, y):
        self.maps[self.map_name].del_tile_to_xy(x, y)
        return

    def render(self, surf, layer_n, tiles, camera_x):
        self.maps[self.map_name].render(surf, layer_n, tiles, camera_x)
        return

class Map:
    def __init__(self, map_data):
        self.map_data = map_data

        self.box_ani = Animation((None, None, None, None), (45, 15, 15, 15))

    def play_box(self, dt):
        self.box_ani.play(dt)

    def set_offset(self, x, y, camera_x, offset):
        tile, x, y = self.find_block(int((x + camera_x) / 48), int(y / 48))
        if len(tile) >= 3:
            tile[2] = offset
        else:
            tile.append(offset)
        self.map_layers[1][tuple_to_str((x, y))] = tile
        return tile, x, y
    
    def set_tile(self, x, y, tile_data):
        self.map_layers[1][tuple_to_str((x, y))] = tile_data
        return

    def set_offset_to_xy(self, x, y, offset):
        tile, x, y = self.find_block(x, y)
        tile[2] = offset
        return tile, x, y

    def del_tile_to_xy(self, x, y):
        del self.map_layers[1][tuple_to_str((x, y))]
        return

    def find_block(self, x, y):
        return self.map_layers[1][tuple_to_str((x, y))], x, y

    @property
    def start_at(self):
        return self.map_data["startAt"]

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

    def get_rects(self, camera_x, pos):
        rects = []
        for tile in self.map_layers[1]:
            tile_pos = str_to_turple(tile)
            # if camera_x - 48 <= tile_pos[0] * 48 <= camera_x + 816:
            #     rect = pygame.Rect(tile_pos[0] * 48 - camera_x, tile_pos[1] * 48, 48, 48)
            #     rects.append(rect)
            if camera_x + pos[0] - 96 <= tile_pos[0] * 48 <= camera_x + pos[0] + 96 and pos[1] - 74 <= tile_pos[1] * 48 <= pos[1] + 74:
                rect = pygame.Rect(tile_pos[0] * 48 - camera_x, tile_pos[1] * 48, 48, 48)
                rects.append(rect)

        return rects

    def render(self, surf, layer_n, tiles, camera_x):
        box_ani_num = self.box_ani.layer

        layer = self.map_layers[layer_n]

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
