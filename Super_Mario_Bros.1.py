import pygame
from scripts.tile import *
from scripts.map_loader import *
from scripts.player import *
from scripts.entity import *

pygame.init()
pygame.joystick.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
WINDOW_SIZE = (768, 720)
screen = pygame.display.set_mode(WINDOW_SIZE)
fullscreen = False
game_screen = pygame.Surface(WINDOW_SIZE)

pygame.display.set_caption("Super Mario Bros.1")
clock = pygame.time.Clock()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

tile_data = {}
for num, tile_style in enumerate(['OverWorld']):
    tiles, _ = load_tiles("data/images/tilesets/OverWorld")
    tile_data[num] = tiles

MAP_BACKGROUND_COLOR = {
    "OverWorld" : (92, 148, 252),
    "UnderGround" : (0, 0, 0),
    "UnderWater" : (92, 148, 252),
    "Castle" : (0, 0, 0)
}

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
    camera_x, map_size, mario.pos, map_type = test_level.get_start_data()
    map_size *= 48

    GRAVITY = 0.6
    pause = False

    entity_mob = {"entity": {"summon": [], "move": []}, "mob": []}
    ### mario ###
    up = False
    right = False
    left = False
    run = False
    run_r = True
    run_l = True
    change_direction = False
    run_timer = 0
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
        game_screen.fill(MAP_BACKGROUND_COLOR[map_type])
        test_level.render(game_screen, 0,  tile_data, camera_x)

        for entity in entity_mob["entity"]["summon"]:
            erase = pygame.Surface((48, 48))
            erase.fill(MAP_BACKGROUND_COLOR[map_type])
            entity[0].render(game_screen, camera_x)
            game_screen.blit(erase, (entity[1][0] * 48 - camera_x, entity[1][1] * 48))
        for entity in entity_mob["entity"]["move"]:
            entity.render(game_screen, camera_x)

        test_level.render(game_screen, 1,  tile_data, camera_x)
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

                if run_l and not left and on_block and \
                        not change_direction and pygame.time.get_ticks() - run_timer >= 1000:

                    run_r = True
                    run_l = False
                    change_direction = True
                    mario_move[0] = - RUN_SPEED
                if change_direction and run_r:
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

                if run_r and not right and on_block and \
                        not change_direction and pygame.time.get_ticks() - run_timer >= 1000:

                    run_r = False
                    run_l = True
                    change_direction = True
                    mario_move[0] = RUN_SPEED
                if change_direction and run_l:
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

            if run and not change_direction:
                mario.status[1] = "run"
                if right:
                    if not run_r:
                        run_timer = pygame.time.get_ticks()
                    run_r = True
                    run_l = False
                else:
                    if not run_l:
                        run_timer = pygame.time.get_ticks()
                    run_r = False
                    run_l = True

            if up and on_block:
                if mario.status[0] == "big":
                    gravity_acc -= BIG_JUMP
                else: jump -= SMALL_JUMP

            if not on_block:
                mario.status[1] = "jump"

            if not jump and right == False and left == False and up == False:
                mario.status[1] = "idle"
                change_direction = False
                run_r = False
                run_l = False

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
            

            rect, (touch_ceiling, block_u), on_block, _, _ = move(mario.rect, mario_move, blocks_rect)
            mario.pos = [rect.x, rect.y]

            if not block_u == None:
                try:
                    tile, x, y = test_level.set_offset_tile(block_u.x, block_u.y, camera_x, [0, 0])
                except KeyError:
                    pass
                else:
                    block_num = tile[1]


                    if len(tile) >= 4 and tile[1] != 2:
                        item = tile[3][0]
                        item_n = tile[3][1]
                        item_n -= 1
                        if item == "mushroom_r":
                            entity = Mushroom_RED(x * 48, y * 48)
                            
                        if item_n <= 0:
                            test_level.set_tile(x, y, [0, 2, tile[2]])
                        else:
                            test_level.set_tile(x, y, [0, tile[1], tile[2], [item, item_n]])

                        entity_mob["entity"]["summon"].append([entity, (x, y)])
                        


                    if block_num in [3, 4] and not len(tile) >= 4:
                        try:
                            test_level.del_tile_to_xy(x, y)
                        except KeyError: pass
                    elif block_num in [0, 1, 2]:
                        pass
                    else:
                        touched_blocks.append([x, y, tile[2], -4, False])

            for n, tile in enumerate(touched_blocks):
                x = tile[0]
                y = tile[1]
                offset = tile[2]
                push_power = tile[3]
                block_down = tile[4]

                offset[1] += push_power if not block_down else - push_power
                if offset[1] <= -24: block_down = True
                if offset[1] >= 0 and block_down: offset[1] = 0

                tile, x, y = test_level.set_offset_tile_to_xy(x, y, offset)

                if offset[1] == 0:
                    del touched_blocks[n]
                else:
                    touched_blocks[n] = [x, y, offset, push_power, block_down]

            if on_block:
                jump = 0
                gravity_acc = 0
                bounce = False
            if touch_ceiling: bounce = True

            if mario.pos[0] <= 0:
                mario.pos[0] = 0

            ### ENTITY & MOB ###
            for i, entity in enumerate(entity_mob["entity"]["summon"]):
                entity[0].pos[1] -= 1
                if entity[0].pos[1] <= (entity[1][1] - 1) * 48:
                    entity[0].pos[1] = (entity[1][1] - 1) * 48
                    entity_mob["entity"]["move"].append(entity[0])
                    del entity_mob["entity"]["summon"][i]
            
            for i, entity in enumerate(entity_mob["entity"]["move"]):
                pass
                

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

                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0 or event.button == 3:
                        up = True
                    if event.button == 1 or event.button == 2:
                        run = True

                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 0 or event.button == 3:
                        up = False
                    if event.button == 1 or event.button == 2:
                        run = False

                if event.type == pygame.JOYHATMOTION:
                    if not event.value[0] == 0:
                        if event.value[0] == 1:
                            right = True
                        if event.value[0] == -1:
                            left = True
                    else:
                        if right:
                            right = False
                        if left:
                            left = False

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