import pygame
from scripts.tile import *
from scripts.map_loader import *
from scripts.player import *

pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
WINDOW_SIZE = (768, 720)
game_screen = pygame.Surface(WINDOW_SIZE)

pygame.display.set_caption("Super Mario Bros.1")
clock = pygame.time.Clock()


tile_data = {}
for num, tile_style in enumerate(['OverWorld']):
    tiles, _ = load_tiles("data/images/tilesets/OverWorld")
    tile_data[num] = tiles

### PLAYER ###
mario = Mario([0, 0])

def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

def move(rect,movement,tiles): # movement = [5,2]
    rect.x += movement[0]
    collisions = collision_test(rect,tiles)
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.left
        if movement[0] < 0:
            rect.left = tile.right
    rect.y += movement[1]
    collisions = collision_test(rect,tiles)
    on_block = False
    for tile in collisions:
        if movement[1] > 0:
            rect.bottom = tile.top
            on_block = True
        if movement[1] < 0:
            rect.top = tile.bottom
    return rect, on_block


def run_level(level):
    test_level = Level.load(f'data/maps/{level}')
    camera_x, map_size, mario.pos = test_level.get_start_data()
    map_size *= 48

    GRAVITY = 0.5

    ### mario ###
    right = False
    left = False
    IDLE_SPEED = 3
    RUN_SPEED = 6
    mario_acc = [2, 0]

    running = True
    while running:
        dt = clock.tick(60)

        ### RENDER ###
        # MAP
        test_level.render(game_screen, tile_data, camera_x)
        mario.render(game_screen)

        screen.fill((0, 0, 0))
        screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))

        ### MARIO MOVE ###
        mario_acc[1] += GRAVITY

        rect, on_block = move(mario.check_rect(), mario_acc, test_level.get_rects(camera_x))
        mario.pos = [rect.x, rect.y]
        if on_block: mario_acc[1] = 0

        ### ANIMATION ###
        test_level.play_box(dt)

        ### CAMERA ###
        if camera_x <= 0:
            camera_x = 0
        if camera_x >= map_size - 768:
            camera_x = map_size - 768

        if mario.pos[0] >= WINDOW_SIZE[0] / 2 - mario.rect.size[0]:
            mario.pos[0] = WINDOW_SIZE[0] / 2 - mario.rect.size[0]
            camera_x += mario_acc[0]



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
    return

def main():
    run_level("1-1")
    pygame.quit()

if __name__=="__main__":
    main()