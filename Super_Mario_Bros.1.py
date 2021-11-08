import pygame
from scripts.tile import *
from scripts.map_loader import *
from scripts.player import *

pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
fullscreen = True
WINDOW_SIZE = (768, 720)
game_screen = pygame.Surface(WINDOW_SIZE)

pygame.display.set_caption("Super Mario Bros.1")
clock = pygame.time.Clock()


tile_data = {}
for num, tile_style in enumerate(['OverWorld']):
    tiles, _ = load_tiles("data/images/tilesets/OverWorld")
    tile_data[num] = tiles

### PLAYER ###
mario = Mario()

def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

def move(rect,movement,tiles): # movement = [5,2]
    up = False
    down = False
    right = False
    left = False
    rect.x += movement[0]
    collisions = collision_test(rect,tiles)
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.left
            right = True
        if movement[0] < 0:
            rect.left = tile.right
            left = True
    rect.y += movement[1]
    collisions = collision_test(rect,tiles)
    for tile in collisions:
        if movement[1] + 10 >= 0:
            rect.bottom = tile.top
            down = True
        if movement[1] < 0:
            rect.top = tile.bottom
            up = True
    return rect, up, down, right, left


def run_level(level):
    global screen, fullscreen

    test_level = Level.load(f'data/maps/{level}')
    camera_x, map_size, mario.pos = test_level.get_start_data()
    map_size *= 48

    GRAVITY = 0.6

    ### mario ###
    up = False
    right = False
    left = False
    run = False
    WALK_SPEED = 4
    RUN_SPEED = 6
    SMALL_JUMP = 15.5
    BIG_JUMP = 16
    gravity_acc = 0
    jump = 0
    mario_move = [0, 0]
    mario.check_rect()

    on_block = True

    touch_ceiling = False
    bounce = False

    running = True
    while running:
        dt = clock.tick(60)

        ### RENDER ###
        # MAP
        test_level.render(game_screen, tile_data, camera_x)
        mario.render(game_screen)

        screen.fill((0, 0, 0))
        if fullscreen:
            screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
        else:
            screen.blit(game_screen, (0, 0))

        ### ANIMATION ###
        test_level.play_box(dt)

        ### MARIO ###
        mario.check_rect()
        gravity_acc += GRAVITY

        if right:
            mario_move[0] += WALK_SPEED if not run else RUN_SPEED
            mario.look_right()
            mario.status[1] = "walk"
        if left:
            mario_move[0] -= WALK_SPEED if not run else RUN_SPEED
            mario.look_left()
            mario.status[1] = "walk"
        if run: mario.status[1] = "run"
        if up and on_block:
            if mario.status[0] == "big":
                gravity_acc -= BIG_JUMP
            else: jump -= SMALL_JUMP
        if not on_block:
            mario.status[1] = "jump"
        if not jump and right == False and left == False and up == False:
            mario.status[1] = "idle"

        mario.play_ani(dt)

        if gravity_acc <= 1: gravity_acc = 1
        mario_move[1] += jump + gravity_acc if not bounce else gravity_acc
        rect, touch_ceiling, on_block, _, _ = move(mario.rect, mario_move, test_level.get_rects(camera_x))
        mario.pos = [rect.x, rect.y]

        if on_block:
            jump = 0
            gravity_acc = 0
            bounce = False
        if touch_ceiling: bounce = True

        if mario.pos[0] <= 0:
            mario.pos[0] = 0

        # if jump == 0 and gravity_acc <= 1:
        #     on_block = True



        ### CAMERA ###
        if camera_x >= map_size - 768:
            camera_x = map_size - 768

        if mario.pos[0] >= WINDOW_SIZE[0] / 2 - mario.rect.size[0]:
            mario.pos[0] = WINDOW_SIZE[0] / 2 - mario.rect.size[0]
            camera_x += mario_move[0]

        ### reset ###
        mario_move = [0, 0]

        ### EVENT ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(WINDOW_SIZE)

                if event.key == pygame.K_d:
                    right = True
                if event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_w:
                    up = True
                if event.key == pygame.K_RSHIFT:
                    run = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_RSHIFT:
                    run = False

        pygame.display.update()
    return

def main():
    run_level("1-1")
    pygame.quit()

if __name__=="__main__":
    main()