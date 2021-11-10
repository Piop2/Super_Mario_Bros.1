import pygame
from scripts.tile import *
from scripts.map_loader import *

pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
WINDOW_SIZE = (768, 720)
game_screen = pygame.Surface(WINDOW_SIZE)

pygame.display.set_caption("Map Viewer")
clock = pygame.time.Clock()

MAP_BACKGROUND_COLOR = {
    "OverWorld" : (92, 148, 252),
    "UnderGround" : (0, 0, 0),
    "UnderWater" : (92, 148, 252),
    "Castle" : (0, 0, 0)
}

tile_data = {}
for num, tile_style in enumerate(['OverWorld']):
    tiles, _ = load_tiles("data/images/tilesets/OverWorld")
    tile_data[num] = tiles


test_level = Level.load('data/maps/1-1')
camera_x, map_size, _, map_type = test_level.get_start_data()
map_size *= 48

right = False
left = False

running = True
while running:
    dt = clock.tick(60)

    ### RENDER ###
    # MAP
    game_screen.fill(MAP_BACKGROUND_COLOR[map_type])
    test_level.render(game_screen, 0, tile_data, camera_x)
    test_level.render(game_screen, 1, tile_data, camera_x)

    screen.fill((0, 0, 0))
    screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))



    if right:
        camera_x += 16
    if left:
        camera_x -= 16

    if camera_x <= 0:
        camera_x = 0
    if camera_x >= map_size - 768:
        camera_x = map_size - 768

    test_level.play_box(dt)

    ### EVENT ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
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

pygame.quit()