import json
import pygame
from random import randint
from utils import SpriteSheet
from constants import GREEN, RED, WHITE

# Анимация
# Условие конца
# state отрисовки конца

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, entity, 
                srite_file, hb_x=20, hb_text_x=40, flip=False):
        super().__init__()

        self.change_x = 0
        self.change_y = 0
        self.flip = flip
        data = self.read_json(entity)
        ss = SpriteSheet(f'assets/images/{srite_file}.png')

        self.standing = []
        for row in data['standing']:
            self.standing += self.append_img(ss.get_image(*row), flip=flip)

        self.appercot = []
        for row in data['appercot']:
            self.appercot += self.append_img(ss.get_image(*row), flip=flip)

        self.death = []
        for row in data['death']:
            self.death += self.append_img(ss.get_image(*row), flip=flip)

        self.attack = False
        self.image = self.standing[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.stand_indx = 1
        self.appercot_indx = 0
        self.death_indx = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_cooldown = 0
        self.enemy = None
        self.hb = HealthBar(100, hb_x, 10, 350, 30, hb_text_x, 1)

    def read_json(self, charachter):
        with open('animation.json', 'r') as f:
            data = json.load(f)
        data = data[charachter]
        return data

    def append_img(self, img, flip=False):
        lst = []
        img = pygame.transform.scale2x(img)
        if flip:
            img = pygame.transform.flip(img, True, False)
        for _ in range(3):
            lst.append(img)
        return lst

    def update(self):
        if self.hb.hp == 0:
            self.image = self.death[self.death_indx % len(self.death)]
            self.death_indx += 1
        elif not self.attack:
            self.image = self.standing[self.stand_indx % len(self.standing)]
            self.stand_indx += 1
        else:
            self.image = self.appercot[self.appercot_indx % len(self.appercot)]
            self.appercot_indx += 1
            if self.appercot_indx >= len(self.appercot):
                self.attack = False
                self.appercot_indx = 0

        if self.hb.hp > 0:
            if self.flip:
                if randint(0, 100) > 95:
                    self.attack = True
                self.rect.x += randint(-6, 6)        
            else:
                self.rect.x += self.change_x
            self.mask = pygame.mask.from_surface(self.image)
            hit_list = pygame.sprite.collide_mask(self, self.enemy)
            if hit_list:
                if self.enemy.attack and not self.hit_cooldown:
                    self.hit_cooldown = 21
                    self.hb.hp -= 10
                self.stop()
        
        if self.hit_cooldown:
            self.hit_cooldown -= 1
        self.hb.update()

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

class HealthBar:
    def __init__(self, hp, x, y, w, h, text_x, text_y):
        self.hp = hp
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.text_x = text_x
        self.text_y = text_y
        self.max_w = w

    def update(self):
        if self.hp < 0:
            self.hp = 0
            return
        self.w = self.hp*3.5

    def draw(self, screen, font):
        square_r = pygame.Rect(self.x, self.y, self.max_w, self.h)
        square_g = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, RED, square_r)
        pygame.draw.rect(screen, GREEN, square_g)
        text = font.render(str(self.hp), True, WHITE)
        screen.blit(text,  (self.text_x, self.text_y))


class Timer:
    def __init__(self, x, y, indx):
        self.x = x
        self.y = y
        self.indx = indx
        self.stop = False

    def update(self):
        if not self.stop:
            self.indx -= 0.3

    def draw(self, screen, font2):
        text = font2.render(str(round(self.indx/10)), True, RED)
        screen.blit(text, (self.x, self.y))

