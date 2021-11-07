import pygame
from scripts.tile import *
from scripts.map_loader import *

pygame.init()
WINDOW_SIZE = (256, 224)
screen = pygame.display.set_mode((WINDOW_SIZE[0] * 3, WINDOW_SIZE[1] * 3))
pygame.display.set_caption("Super Mario Bros.1")
clock = pygame.time.Clock()


tile_data = {}
for num, tile_style in enumerate(['OverWorld']):
    tiles, _ = load_tiles("data/images/tilesets/OverWorld")
    tile_data[num] = tiles


def run_level(level):
    test_level = Level.load(f"data/maps/{level}")
    camera_x, map_size = test_level.get_start_data()

    down = False
    up = False
    right = False
    left = False

    running = True
    while running:
        dt = clock.tick(60)

        if camera_x <= 0:
            camera_x = 0
        if camera_x >= map_size * 16 - 256:
            camera_x = map_size * 16 - 256

        test_level.play_box(dt)

        ### RENDER ###
        # MAP
        test_level.render(screen, tile_data, camera_x)


        ### EVENT ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_LEFT:
                    left = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False

        pygame.display.update()
    return

def main():
    return

run_level("1-1")