import pygame
from scripts.tile import *
from scripts.map_loader import *

pygame.init()
WINDOW_SIZE = (256, 224)
screen = pygame.display.set_mode((WINDOW_SIZE[0] * 3, WINDOW_SIZE[1] * 3))
pygame.display.set_caption("Map Viewer")
clock = pygame.time.Clock()

test = [load_tilesets('data/images/tilesets/OverWorld.png')]
test_map, camera_x, map_size = Map.load('data/maps/debug.json')

right = False
left = False

_screen = pygame.Surface(WINDOW_SIZE)

running = True
while running:
    clock.tick(60)

    test_map, _, map_size = Map.load('data/maps/debug.json')

    if right:
        camera_x += 4
    if left:
        camera_x -= 4

    if camera_x <= 0:
        camera_x = 0
    if camera_x >= map_size * 16 - 256:
        camera_x = map_size * 16 - 256

    test_map.render(_screen, test, camera_x)

    screen.blit(pygame.transform.scale(_screen, (WINDOW_SIZE[0] * 3, WINDOW_SIZE[1] * 3)), (0, 0))
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

pygame.quit()
