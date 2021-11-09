import pygame
from scripts.tile import *
from scripts.map_loader import *
from scripts.player import *

pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
WINDOW_SIZE = (768, 720)
screen = pygame.display.set_mode(WINDOW_SIZE)
fullscreen = False
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
    block_u = None
    down = False
    block_d = None
    right = False
    block_r = None
    left = False
    block_l = None

    rect.x += movement[0]
    collisions = collision_test(rect,tiles)[::-1]
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.left
            right = True
        if movement[0] < 0:
            rect.left = tile.right
            left = True
    rect.y += movement[1]
    collisions = collision_test(rect,tiles)[::-1]
    for tile in collisions:
        if movement[1] + 10 >= 0:
            rect.bottom = tile.top
            down = True
        if movement[1] < 0:
            rect.top = tile.bottom
            up = True
            block_u = tile
    return rect, (up, block_u), down, right, left


def run_level(level):
    global screen, fullscreen

    test_level = Level.load(f'data/maps/{level}')
    camera_x, map_size, mario.pos = test_level.get_start_data()
    map_size *= 48

    GRAVITY = 0.6
    pause = False

    ### mario ###
    up = False
    right = False
    left = False
    run = False
    run_direction = ""
    change_direction = False
    WALK_SPEED = 4
    RUN_SPEED = 6
    SMALL_JUMP = 15.5
    BIG_JUMP = 16
    gravity_acc = 0
    jump = 0
    mario_move = [0, 0]
    mario.check_rect()
    game_over = False

    on_block = True

    touch_ceiling = False
    bounce = False

    touched_blocks = []

    running = True
    while running:
        dt = clock.tick(50)

        ### RENDER ###
        # MAP
        test_level.render(game_screen, tile_data, camera_x)
        mario.render(game_screen)

        screen.fill((0, 0, 0))
        if fullscreen:
            screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
        else:
            screen.blit(game_screen, (0, 0))

        if not pause:
            ### ANIMATION ###
            test_level.play_box(dt)

            ### MARIO ###
            mario.check_rect()
            blocks_rect = test_level.get_rects(camera_x, mario.pos)
            gravity_acc += GRAVITY

            if right:
                mario.look_right()

                if run_direction == "left" and on_block and not change_direction:
                    run_direction = "right"
                    change_direction = True
                    mario_move[0] = - RUN_SPEED
                if change_direction and run_direction == "right":
                    if mario_move[0] > 0:
                        change_direction = False

                if not run:
                    mario_move[0] += WALK_SPEED
                elif change_direction:
                    mario_move[0] += 0.5
                else:
                    mario_move[0] += RUN_SPEED

                if not change_direction:
                    mario.status[1] = "walk"
                else:
                    mario.status[1] = "change_direction"
            if left:
                mario.look_left()

                if run_direction == "right" and on_block and not change_direction:
                    run_direction = "left"
                    change_direction = True
                    mario_move[0] = RUN_SPEED
                if change_direction and run_direction == "left":
                    if mario_move[0] < 0:
                        change_direction = False

                if not run:
                    mario_move[0] -= WALK_SPEED
                elif change_direction:
                    mario_move[0] -= 0.5
                else:
                    mario_move[0] -= RUN_SPEED

                if not change_direction:
                    mario.status[1] = "walk"
                else:
                    mario.status[1] = "change_direction"

            # if right and left:
            #     change_direction = False
            #     run_direction = ""

            if run and not change_direction:
                mario.status[1] = "run"
                if right:
                    run_direction = "right"
                else:
                    run_direction = "left"

            if up and on_block:
                if mario.status[0] == "big":
                    gravity_acc -= BIG_JUMP
                else: jump -= SMALL_JUMP

            if not on_block:
                mario.status[1] = "jump"

            if not jump and right == False and left == False and up == False:
                mario.status[1] = "idle"
                change_direction = False
                run_direction = ""

            if mario.pos[1] >= WINDOW_SIZE[1]:
                pause = True
                game_over = True
                gravity_acc = 0
                jump = - 20
                pygame.time.delay(1000)

            mario.play_ani(dt)

            if gravity_acc <= 1: gravity_acc = 1
            if bounce:
                mario_move[1] += gravity_acc
            else:
                mario_move[1] += jump + gravity_acc

            # speed range
            if abs(mario_move[1]) >= 25:
                mario_move[1] = gravity_acc
                print(mario_move)
            if abs(mario_move[0]) >= 10:
                change_direction = False
                run_direction = ""

            rect, (touch_ceiling, block_u), on_block, _, _ = move(mario.rect, mario_move, blocks_rect)
            mario.pos = [rect.x, rect.y]

            if not block_u == None:
                try:
                    tile, x, y = test_level.set_offset_tile(block_u.x, block_u.y, camera_x, [0, -24])
                except KeyError:
                    pass
                else:
                    block_num = tile[1]

                    if block_num in [3, 4]:
                        try:
                            test_level.del_tile_to_xy(x, y)
                        except KeyError: pass
                    else:
                        touched_blocks.append([x, y, tile[2]])

            for n, tile in enumerate(touched_blocks):
                x = tile[0]
                y = tile[1]
                offset = tile[2]

                offset_y = 2.5
                offset[1] += - offset[1] if offset[1] + offset_y >= 0 else offset_y

                tile, x, y = test_level.set_offset_tile_to_xy(x, y, offset)
                touched_blocks[n] = [x, y, tile[2]]



            if on_block:
                jump = 0
                gravity_acc = 0
                bounce = False
            if touch_ceiling: bounce = True

            if mario.pos[0] <= 0:
                mario.pos[0] = 0



            ### CAMERA ###
            if camera_x >= map_size - 768:
                camera_x = map_size - 768

            if mario.pos[0] >= WINDOW_SIZE[0] / 2 - mario.rect.size[0]:
                if not camera_x >= map_size - 768:
                    mario.pos[0] = WINDOW_SIZE[0] / 2 - mario.rect.size[0]
                    camera_x += mario_move[0]

            ### reset ###
            if not change_direction:
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
        else:
            if game_over:
                mario.status[1] = "dead"
                gravity_acc += GRAVITY
                mario.pos[1] += jump + gravity_acc
                if mario.pos[1] >= WINDOW_SIZE[1] + 48:
                    pygame.time.delay(1000)
                    return


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

        pygame.display.update()
    return

def main():
    run_level("1-1")
    pygame.quit()

if __name__=="__main__":
    main()