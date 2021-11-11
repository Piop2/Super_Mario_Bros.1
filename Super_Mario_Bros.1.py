import pygame
import sys

from pygame import color
from scripts.core_fuc import *
from scripts.text import *
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


MAP_BACKGROUND_COLOR = {
    "OverWorld" : (92, 148, 252),
    "UnderGround" : (0, 0, 0),
    "UnderWater" : (92, 148, 252),
    "Castle" : (0, 0, 0)
}

big_font_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', 'x', '!', 'c', 'a', '_', '.']
big_font = Font("data/font/big_font.png", (0, 0, 0), (0, 0, 0), big_font_order)
colored_big_font = Font("data/font/big_font.png", (252, 252, 252), (252, 188, 176), big_font_order)


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
        if movement[1] >= 0:
            rect.bottom = tile.top
            down = True
        if movement[1] < 0:
            rect.top = tile.bottom
            up = True
            block_u = tile
    return rect, (up, block_u), (down, block_d), (right, block_r), (left, block_l)

class Game:
    def __init__(self):
        self.level = "1-1"
        self.life = 0
        self.score = 0
        self.coin = 0
        self.best_score = read_f("data/saves/save1.json")["bestScore"]
        self.time = 0
        return

    def run_level(self):
        global screen, fullscreen

        tile_data = {}
        for num, tile_style in enumerate(['OverWorld']):
            tiles, _ = load_tiles("data/images/tilesets/OverWorld")
            tile_data[num] = tiles

        ### PLAYER ###
        mario = Mario()


        level_map = Level.load(f'data/maps/{self.level}')
        camera_x, map_size, mario.pos, map_type = level_map.get_start_data()
        map_size *= 48

        GRAVITY = 0.7
        pause = False
        game_over = False
        game_clear = False

        
        small_coin = Animation(*load_animation(f"data/images/small_coin/{map_type}"))
        game_timer_s = pygame.time.get_ticks()


        entity_mob = {"entity": {"summon": [], "move": []}, "mob": []}
        ### mario ###
        up = False
        steel_up = False
        right = False
        left = False
        run = False
        run_r = True
        run_l = True
        change_direction = False
        run_timer = 0
        WALK_SPEED = 4
        RUN_SPEED = 6
        # SMALL_JUMP = 18
        # BIG_JUMP = 18
        JUMP = 17
        gravity_acc = 0
        jump = 0
        mario_move = [0, 0]
        mario.check_rect()

        on_block = True

        touch_ceiling = False
        bounce = False

        touched_blocks = []

        block_break_partickle = Animation(*load_animation(f"data/images/particle/break_block/{map_type}"))
        particles = []
        

        running = True
        while running:
            dt = clock.tick(60)


            ### RENDER ###
            # MAP
            game_screen.fill(MAP_BACKGROUND_COLOR[map_type])
            level_map.render(game_screen, 0,  tile_data, camera_x)

            for entity in entity_mob["entity"]["summon"]:
                erase = pygame.Surface((48, 48))
                erase.fill(MAP_BACKGROUND_COLOR[map_type])
                entity[0].render(game_screen, camera_x)
                game_screen.blit(erase, (entity[1][0] * 48 - camera_x, entity[1][1] * 48))
            for entity in entity_mob["entity"]["move"]:
                entity.render(game_screen, camera_x)

            mario.render(game_screen)

            level_map.render(game_screen, 1,  tile_data, camera_x)

            for particle in particles:
                game_screen.blit(particle[0].get_img(), (particle[1][0] - camera_x, particle[1][1]))


            big_font.render(game_screen, "MARIO", (72, 24))
            big_font.render(game_screen, "{0:06}".format(self.score), (72, 48))

            game_screen.blit(small_coin.get_img(), (264, 48))
            big_font.render(game_screen, "x{0:02}".format(self.coin), (288, 48))
            
            big_font.render(game_screen, "WORLD", (432, 24))
            big_font.render(game_screen, self.level, (456, 48))
            
            big_font.render(game_screen, "TIME", (600, 24))
            big_font.render(game_screen, "{0:03}".format(self.time), (624, 48))

            screen.fill((0, 0, 0))
            if fullscreen:
                screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
            else:
                screen.blit(game_screen, (0, 0))
            
            small_coin.play(dt)

            if not pause:
                ### GAME ###
                game_timer_e = pygame.time.get_ticks()
                if game_timer_e - game_timer_s >= 1000:
                    self.time -= 1
                    game_timer_s = game_timer_e
                    if self.time <= -1:
                        running = False

                ### ANIMATION ###
                level_map.play_box(dt)

                ### MARIO ###
                mario.check_rect()
                blocks_rect = level_map.get_rects(camera_x, mario.pos)
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

                if up:
                    if on_block:
                        jump = - JUMP
                        steel_up = True
                    else:
                        if -1 <= jump + gravity_acc <= 1:
                            steel_up = False

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
                    steel_up = False
                    pygame.time.delay(1000)

                mario.play_ani(dt)

                if gravity_acc <= 1: gravity_acc = 1
                if bounce:
                    mario_move[1] += gravity_acc
                else:
                    mario_move[1] += jump + gravity_acc

                rect, (touch_ceiling, block_u), (on_block, _), (_, _), (_, _) = move(mario.rect, mario_move, blocks_rect)
                mario.pos = [rect.x, rect.y]

                if not block_u == None:
                    on_block = False
                    steel_up = False
                    try:
                        tile, x, y = level_map.set_offset_tile(block_u.x, block_u.y, camera_x, [0, 0])
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
                            elif item == "mushroom_g":
                                entity = Mushroom_GREEN(x * 48, y * 48)
                            elif item == "fire_flower":
                                entity = Fire_Flower(x * 48, y * 48)
                            else: raise ValueError
                                
                            if item_n <= 0:
                                level_map.set_tile(x, y, [0, 2, tile[2]])
                            else:
                                level_map.set_tile(x, y, [0, tile[1], tile[2], [item, item_n]])
                            print(f"Summon: {str(entity)} - position:{entity.pos}")
                            entity_mob["entity"]["summon"].append([entity, (x, y)])
                            


                        if block_num in [3, 4] and not len(tile) >= 4:
                            try:
                                level_map.del_tile_to_xy(x, y)
                            except KeyError: pass
                            else:
                                particles.append([block_break_partickle, [x * 48 + 24, y * 48 + 24], 20, 1, 0])
                                particles.append([block_break_partickle, [x * 48 + 24, y * 48 + 24], 15, 1, 0])
                                particles.append([block_break_partickle, [x * 48 + 24, y * 48 + 24], 20, -1, 0])
                                particles.append([block_break_partickle, [x * 48 + 24, y * 48 + 24], 15, -1, 0])
                                print("Add: particle")
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

                    tile, x, y = level_map.set_offset_tile_to_xy(x, y, offset)

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

                ### PARTICLE ###
                for i, particle in enumerate(particles):
                    particle[0].play(dt)
                    particle[4] += GRAVITY
                    particle[1][0] += 5 * particle[3]
                    particle[1][1] += - particle[2] + particle[4]
                    if particle[1][1] >= WINDOW_SIZE[1]:
                        del particles[i]
                        print("Delete: particle")

                ### ENTITY & MOB ###
                for i, entity in enumerate(entity_mob["entity"]["summon"]):
                    entity[0].play_ani(dt)
                    entity[0].pos[1] -= 1
                    if entity[0].pos[1] <= (entity[1][1] - 1) * 48:
                        entity[0].pos[1] = (entity[1][1] - 1) * 48
                        entity[0].check_rect()
                        entity_mob["entity"]["move"].append(entity[0])
                        del entity_mob["entity"]["summon"][i]
                
                for i, entity in enumerate(entity_mob["entity"]["move"]):
                    entity.play_ani(dt)
                    entity_blocks_rect = level_map.get_rects_to_xy(entity.pos)
                    entity_move = entity.move(GRAVITY)
                    rect, (_, _), (touch_down, _), (touch_r, _), (touch_l, _) = move(entity.rect, entity_move, entity_blocks_rect)
                    if touch_r or touch_l:
                        entity.turn_direction()
                    
                    if touch_down:
                        entity.acc_y = 0
                    
                    entity.pos = [rect.x, rect.y]
                    
                    if entity.pos[0] + 48 - camera_x <= 0 or entity.pos[1] >= WINDOW_SIZE[1]:
                        print(f"Kill: {str(entity)} - position:{entity.pos}")
                        del entity_mob["entity"]["move"][i]
                    

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
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0 or event.button == 3:
                            up = True
                        if event.button == 1 or event.button == 2:
                            run = True

                    if event.type == pygame.JOYBUTTONUP:
                        if event.button == 0 or event.button == 3:
                            up = False
                            if steel_up:
                                jump += 5
                            steel_up = False
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
                        if event.key == pygame.K_e:
                            game_clear = True
                            running = False

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_d:
                            right = False
                        if event.key == pygame.K_a:
                            left = False
                        if event.key == pygame.K_w:
                            up = False
                            if steel_up:
                                jump += 5
                            steel_up = False

                        if event.key == pygame.K_RSHIFT:
                            run = False

            else:
                if game_over:
                    mario.status[1] = "dead"
                    gravity_acc += GRAVITY
                    mario.pos[1] += jump + gravity_acc
                    if mario.pos[1] >= WINDOW_SIZE[1] + 48:
                        pygame.time.delay(1000)
                        running = False


                ### EVENT ###
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            fullscreen = not fullscreen
                            if fullscreen:
                                pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                            else:
                                screen = pygame.display.set_mode(WINDOW_SIZE)

            pygame.display.update()
        
        return game_clear

    def title_screen(self):
        global screen, fullscreen
        title = load_img("data/images/title.png")
        mario_img = load_img("data/images/title_mario.png")
        map_img = load_img("data/images/title_map.png")
        pointer = load_img("data/images/title_pointer.png")
        small_coin = Animation(*load_animation("data/images/small_coin/OverWorld"))

        pointer_y = [408, 456]
        select_num = 0

        colored_text = "c2021 SEOUN"

        running = True
        while running:
            dt = clock.tick(50)

            game_screen.fill(MAP_BACKGROUND_COLOR["OverWorld"])
            game_screen.blit(map_img, (0, WINDOW_SIZE[1] - map_img.get_height()))
            game_screen.blit(mario_img, (123, 576))
            game_screen.blit(title, (120, 72))
            game_screen.blit(pointer, (216, pointer_y[select_num]))

            # text

            big_font.render(game_screen, "MARIO", (72, 24))
            big_font.render(game_screen, "000000", (72, 48))

            game_screen.blit(small_coin.get_img(), (264, 48))
            big_font.render(game_screen, "x00", (288, 48))
            
            big_font.render(game_screen, "WORLD", (432, 24))
            big_font.render(game_screen, "1-1", (456, 48))
            
            big_font.render(game_screen, "TIME", (600, 24))


            big_font.render(game_screen, "1 PLAYER GAME", (264, 408))
            if select_num == 1:
                big_font.render(game_screen, "a SNGYN_P", (264, 456))
            else:
                big_font.render(game_screen, "2 PLAYER GAME", (264, 456))
            big_font.render(game_screen, "TOP - {0:06d}".format(self.best_score), (288, 528))

            colored_big_font.render(game_screen, colored_text, (120 + title.get_width() - colored_big_font.width(colored_text), 336))

            
            screen.fill((0, 0, 0))
            if fullscreen:
                screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
            else:
                screen.blit(game_screen, (0, 0))


            small_coin.play(dt)

            ### EVENT ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        if select_num == 0:
                            running = False
                        else: pass
                
                if event.type == pygame.JOYHATMOTION:
                    if not event.value[1] == 0:
                        if event.value[1] == 1:
                            select_num -= 1 if not select_num == 0 else 0
                        else:
                            select_num += 1 if not select_num + 1 == len(pointer_y) else 0


                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(WINDOW_SIZE)
                    
                    if event.key == pygame.K_w:
                        select_num -= 1 if not select_num == 0 else 0
                    
                    if event.key == pygame.K_s:
                        select_num += 1 if not select_num + 1 == len(pointer_y) else 0

                    if event.key == pygame.K_RETURN:
                        if select_num == 0:
                            running = False
                        else: pass
            pygame.display.update()
        return

    def level_intro(self):
        global screen, fullscreen

        small_coin = load_img("data/images/small_coin/UnderGround/0.png")
        mario_img = load_img("data/images/title_mario.png")

        start_time = pygame.time.get_ticks()

        running = True
        while running:
            dt = clock.tick(10) # 괜히 여기서 뻑가지 않게 프레임 드랍
            game_screen.fill((0, 0, 0))

            big_font.render(game_screen, "MARIO", (72, 24))
            big_font.render(game_screen, "{0:06}".format(self.score), (72, 48))

            game_screen.blit(small_coin, (264, 48))
            big_font.render(game_screen, "x{0:02}".format(self.coin), (288, 48))
            
            big_font.render(game_screen, "WORLD", (432, 24))
            big_font.render(game_screen, self.level, (456, 48))
            
            big_font.render(game_screen, "TIME", (600, 24))

            big_font.render(game_screen, "WORLD", (264, 216))
            big_font.render(game_screen, self.level, (408, 216))

            game_screen.blit(mario_img, (288, 291))
            big_font.render(game_screen, "x {}".format(str(self.life).rjust(2, " ")), (360, 315))



            end_time = pygame.time.get_ticks()
            if end_time - start_time >= 2000:
                running = False
            

            
            screen.fill((0, 0, 0))
            if fullscreen:
                screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
            else:
                screen.blit(game_screen, (0, 0))

            ### EVENT ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(WINDOW_SIZE)
                
            pygame.display.update()
        return

    def time_up(self):
        global screen, fullscreen

        small_coin = load_img("data/images/small_coin/UnderGround/0.png")

        start_time = pygame.time.get_ticks()

        running = True
        while running:
            dt = clock.tick(10) # 괜히 여기서 뻑가지 않게 프레임 드랍
            game_screen.fill((0, 0, 0))

            big_font.render(game_screen, "MARIO", (72, 24))
            big_font.render(game_screen, "{0:06}".format(self.score), (72, 48))

            game_screen.blit(small_coin, (264, 48))
            big_font.render(game_screen, "x{0:02}".format(self.coin), (288, 48))
            
            big_font.render(game_screen, "WORLD", (432, 24))
            big_font.render(game_screen, self.level, (456, 48))
            
            big_font.render(game_screen, "TIME", (600, 24))

            big_font.render(game_screen, "TIME UP", (288, 360))


            end_time = pygame.time.get_ticks()
            if end_time - start_time >= 2000:
                running = False
            

            
            screen.fill((0, 0, 0))
            if fullscreen:
                screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
            else:
                screen.blit(game_screen, (0, 0))

            ### EVENT ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(WINDOW_SIZE)
                
            pygame.display.update()
        return

    def game_over(self):
        global screen, fullscreen

        small_coin = load_img("data/images/small_coin/UnderGround/0.png")

        start_time = pygame.time.get_ticks()

        running = True
        while running:
            dt = clock.tick(10) # 괜히 여기서 뻑가지 않게 프레임 드랍
            game_screen.fill((0, 0, 0))

            big_font.render(game_screen, "MARIO", (72, 24))
            big_font.render(game_screen, "{0:06}".format(self.score), (72, 48))

            game_screen.blit(small_coin, (264, 48))
            big_font.render(game_screen, "x{0:02}".format(self.coin), (288, 48))
            
            big_font.render(game_screen, "WORLD", (432, 24))
            big_font.render(game_screen, self.level, (456, 48))
            
            big_font.render(game_screen, "TIME", (600, 24))

            big_font.render(game_screen, "MARIO", (312, 312))
            big_font.render(game_screen, "GAME OVER", (264, 360))


            end_time = pygame.time.get_ticks()
            if end_time - start_time >= 2000:
                running = False
            

            
            screen.fill((0, 0, 0))
            if fullscreen:
                screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
            else:
                screen.blit(game_screen, (0, 0))

            ### EVENT ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(WINDOW_SIZE)
                
            pygame.display.update()
        return

    def show_credits(self):
        global screen, fullscreen

        start_time = pygame.time.get_ticks()


        credits_text = [
            [("ORIGINAL GAME", 0), ("cNINTENDO   SUPER MARIO BROS.", 3), ("THIS GAME IS A REMAKE VERSION", 12), ("OF SUPER MARIO BROS. 1", 13)], # 원작, 리메이크
            [("MAKER", 0), ("SEOUN          a SNGYN_P", 3), ("SHINBANPO    PARKHYUNWOO", 5)], # 제작
            [("RESORCE", 0), ("WEBSITE  SPRITERS-RESORCE.COM", 3), ("REFERENCE", 11), ("YOUTUBE  NENRIKIGAMINGCHANNEL", 14), ("YOUTUBE        DAFLUFFYPOTATO", 16)],
            [("REMAKE WITH PYTHON PYGAME", 7)]  # REMAKE WITH PYTHON
        ]
        credits_n = 0

        running = True
        while running:
            dt = clock.tick(50) # 괜히 여기서 뻑가지 않게 프레임 드랍
            game_screen.fill((0, 0, 0))

            for (text, line) in credits_text[credits_n]:
                big_font.render(game_screen, text, ((WINDOW_SIZE[0] / 2) - (big_font.width(text) / 2), 150 + line * 24))

            
            screen.fill((0, 0, 0))
            if fullscreen:
                screen.blit(game_screen, ((monitor_size[0] / 2) - (WINDOW_SIZE[0] / 2), (monitor_size[1] / 2) - (WINDOW_SIZE[1] / 2)))
            else:
                screen.blit(game_screen, (0, 0))

            end_time = pygame.time.get_ticks()
            if end_time - start_time >= 4000:
                credits_n += 1
                start_time = end_time
            
            if credits_n >= len(credits_text):
                running = False


            ### EVENT ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(WINDOW_SIZE)
                
            pygame.display.update()
        return


    def main(self):
        self.life = 1

        # title screen
        self.title_screen()

        running = True
        while running:
            # level intro
            self.time = 300
            self.level_intro()
            # game start
            game_clear = self.run_level()
            if game_clear:
                self.show_credits()
                running = False
            else:
                self.life -= 1

                if self.time <= 0: # time up
                    self.time_up()

                if self.life <= 0: # game over
                    self.level_intro()
                    self.game_over()
                    running = False

                
        return self.main()


if __name__=="__main__":
    game = Game()
    game.main()