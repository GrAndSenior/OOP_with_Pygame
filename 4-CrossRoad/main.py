import pygame
import pgzrun
from video import Video
from random import randint, choice
from game import Game

TITLE = 'CROSS THE ROAD'
WIDTH = 800
HEIGHT = 700

pygame.mixer.init()

gm = Game(Actor)
gm.init_lvl(1)
video = Video('video/chicken_screem.mp4', 'sounds/chicken_screem.mp3')
# Загрузка изображений

explosion = Actor('explosion/0', (-100, -100))
explosion.time = 0

state = 'game'

video.play_audio(pygame.mixer)


def draw():
    ended = video.play_video(screen)
    if not ended:
        return

    for grass in gm.grasses:
        grass.draw()
    for road in gm.roads:
        road.draw()
    for car in gm.cars:
        car.draw()
    for enemy in gm.enemies:
        enemy.draw()
    for water in gm.water_sprites:
        water.draw()
    for log in gm.logs:
        log.draw()
    gm.finish.draw()
    gm.chicken.draw()

    if state == 'pause':
        screen.draw.text('PAUSE', fontsize=60,
                         center=(WIDTH//2, HEIGHT//2),
                         color='red')

    if state == 'win':
        screen.draw.text('WIN! PRESS SPACE', fontsize=60,
                         center=(WIDTH//2, HEIGHT//2),
                         color='green')
    if state == 'loose':
        screen.draw.text('GAME OVER!', fontsize=60,
                         center=(WIDTH//2, HEIGHT//2),
                         color='red')
        explosion.draw()


def update(dt):
    global tracks, state
    gm.finish.time += dt
    if gm.finish.time > 0.1:
        gm.finish.time = 0
        number = int(gm.finish.image.split('/')[-1])
        gm.finish.image = f'flag/{(number + 1) % 10}'
    if state == 'game':
        gm.update_enemies()
        gm.chicken_move_y(keyboard, HEIGHT)
        for car in gm.cars:
            car.y -= car.speed
            if car.bottom < 0:
                gm.tracks.append(car.track)
                car.track = choice(gm.tracks)
                gm.tracks.remove(car.track)
                car.x = 43+car.track
                car.top = 700
                car.image = choice(gm.car_names)
        if gm.chicken.colliderect(gm.finish):
            state = 'win'
            pygame.mixer.music.load('sounds/win.mp3')
            pygame.mixer.music.play()
        if gm.chicken.collidelist(gm.cars) != -1 or gm.chicken.collidelist(gm.enemies) != -1:
            state = 'loose'
            pygame.mixer.music.load('sounds/car-crash-sound-effect.mp3')
            pygame.mixer.music.play()
            animate(gm.chicken, y=gm.chicken.y-60,
                    tween='bounce_start_end', duration=1)

    if state == 'loose':
        explosion.time += dt
        if explosion.time > 0.2:
            explosion.time = 0
            index = int(explosion.image.split('/')[-1])
            if index == 0:
                explosion.pos = gm.chicken.pos  # (x, y)
                explosion.image = f'explosion/{index + 1}'
            elif index == 7:
                #                 x      y
                explosion.pos = (-100, -100)
            else:
                explosion.image = f'explosion/{index + 1}'


def on_key_down(key):
    global state
    if state == 'game':
        gm.chicken_move_x(key, keys, WIDTH)
        if key == keys.SPACE:
            state = 'pause'
            return
    if state == 'pause':
        if key == keys.SPACE:
            state = 'game'
    if state == 'win':
        if key == keys.SPACE:
            gm.init_lvl(2)
            state = 'game'


pgzrun.go()
