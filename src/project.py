import random
import pygame
import sys
from pygame.math import Vector2

#FOX FUNCTIONS
class FOX:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('images/fox_UP.png').convert_alpha()
        self.head_down = pygame.image.load('images/fox_DOWN.png').convert_alpha()
        self.head_right = pygame.image.load('images/fox_RIGHT.png').convert_alpha()
        self.head_left = pygame.image.load('images/fox_LEFT.png').convert_alpha()

        self.tail_up = pygame.image.load('images/tail_UP.png').convert_alpha()
        self.tail_down = pygame.image.load('images/tail_DOWN.png').convert_alpha()
        self.tail_right = pygame.image.load('images/tail_RIGHT.png').convert_alpha()
        self.tail_left = pygame.image.load('images/tail_LEFT.png').convert_alpha()

        self.body_vertical = pygame.image.load('images/body_UPDOWN.png').convert_alpha()
        self.body_horizontal = pygame.image.load('images/body_LEFTRIGHT.png').convert_alpha()

        self.body_tr = pygame.image.load('images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('images/body_bl.png').convert_alpha()

    def draw_fox(self):
        self.update_head_direction()
        self.update_tail_direction()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_direction(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_direction(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(0,1): self.tail = self.tail_down
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_up

    def move_fox(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

#CHKN FUNCTIONS
class CHKN:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        chkn_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(chicken, chkn_rect)
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x=random.randint(0,cell_number - 1)
        self.y=random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

#NAME OF THE GAME
class MAIN:
    def __init__(self):
        self.fox = FOX()
        self.chkn = CHKN()

    def update(self):
        self.fox.move_fox()
        self.check_collision()
        self.check_fail()

    def draw_elemtents(self):
        self.chkn.draw_fruit()
        self.fox.draw_fox()

    def check_collision(self):
        if self.chkn.pos == self.fox.body[0]:
            self.chkn.randomize()
            self.fox.add_block()
    
    def check_fail(self):
        if not 0 <= self.fox.body[0].x < cell_number or  not 0 <= self.fox.body[0].y < cell_number:
            self.game_over()

        for block in self.fox.body[1:]:
            if block == self.fox.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

#BACKGROUND
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
chicken = pygame.image.load('images/chkn3.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

#CONTROLS
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.fox.direction.y != 1:
                    main_game.fox.direction = Vector2(0,-1)
            if event.key == pygame.K_LEFT:
                if main_game.fox.direction.x != 1:
                    main_game.fox.direction = Vector2(-1,0)
            if event.key == pygame.K_DOWN:
                if main_game.fox.direction.y != -1:   
                    main_game.fox.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.fox.direction.x != -1:
                    main_game.fox.direction = Vector2(1,0)

    screen.fill((175,215,70))
    main_game.draw_elemtents()
    pygame.display.update()
    clock.tick(60)