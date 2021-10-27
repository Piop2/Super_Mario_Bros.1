import pygame
import json

MAP_BACKGROUND_COLOR = {
    "OverWorld" : (92, 148, 252)
}

def str_to_turple(s):
    return tuple([int(v) for v in s.split('.')])

class Map:
    def __init__(self, map_layers, world_type):
        self.map_layers = map_layers
        self.world_type = world_type

    @classmethod
    def load(cls, path):
        with open(path, 'r') as f:
            map_data = json.load(f)
        return Map(map_data["map"], map_data["worldType"]), map_data["cameraX"], map_data["mapSize"]

    def render(self, surf, tiles, camera_x):
        surf.fill(MAP_BACKGROUND_COLOR[self.world_type])

        for n, layer in enumerate(self.map_layers):
            for tile in layer:
                tile_pos = str_to_turple(tile)
                if camera_x -16 <= tile_pos[0] * 16 <= camera_x + 272 and \
                         - 16 <= tile_pos[1] * 16 <= 240:

                    tile_type = layer[tile][0]
                    tile_num = layer[tile][1]
                    surf.blit(tiles[tile_type][tile_num], (tile_pos[0] * 16 - camera_x, tile_pos[1] * 16))
