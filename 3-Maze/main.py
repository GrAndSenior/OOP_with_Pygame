
from pygame import *
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, 
                 player_x, player_y, 
                 size_x, size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image),
                        (size_x, size_y))

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def __init__(self, player_image, 
                 player_x, player_y, 
                 size_x, size_y, 
                 player_x_speed, player_y_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.side = 'right'

    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали, потом по вертикали
        #self.rect.x += self.x_speed
        #self.rect.y += self.y_speed
        
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if self.rect.x <= win_width-40 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0: # идём направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                # если коснулись сразу нескольких, то правый край - минимальный из возможных
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                # если коснулись нескольких стен, то левый край - максимальный
                self.rect.left = max(self.rect.left, p.rect.right) 
        # потом движение по вертикали
        if self.rect.y <= win_height-40 and self.y_speed >0 or self.rect.y >=0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.y_speed > 0: # идем вниз
            for p in platforms_touched:
                # Проверяем, какая из платформ снизу самая высокая, 
                # выравниваемся по ней, запоминаем её как свою опору:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: # идём вверх
            for p in platforms_touched:
                # выравниваем верхний край по нижним краям стенок, на которые наехали
                self.rect.top = max(self.rect.top, p.rect.bottom) 
    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        if self.x_speed > 0:
            bullet_x = self.rect.right
        elif self.x_speed < 0:
            bullet_x = self.rect.x
        else:
            bullet_x = -1
        if bullet_x != -1:    
            bullet = Bullet('source/image/bullet.png', bullet_x, self.rect.centery, 15, 5, self.x_speed*3)
            bullets.add(bullet)
            fire_sound.play()


#класс спрайта-врага   
class Enemy(GameSprite):
    side = "left"
    def __init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y, enemy_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, enemy_image, enemy_x, enemy_y, size_x, size_y)
        self.speed = enemy_speed

    #движение врага
    def update(self):
        if self.rect.x <= 10: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.right >= 790:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# класс спрайта-пули  
class Bullet(GameSprite):
    def __init__(self, bullet_image, bullet_x, bullet_y, size_x, size_y, bullet_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, bullet_image, bullet_x, bullet_y, size_x, size_y)
        self.speed = bullet_speed
    
    # движение пули
    def update(self):
        self.rect.x += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.x > win_width + 10 or self.rect.x < -10:
            self.kill()

#Создаем окошко
win_width = 800
win_height = 600
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#задаем цвет согласно цветовой схеме RGB
#background = transform.scale(image.load("source/image/background.jpg"), (win_width, win_height))

frag_speed = 20
#создаём группу для стен
walls = sprite.Group()

#создаем стены картинки
w1 = GameSprite('source/image/wall.png', 0, 90, 700, 20)
w2 = GameSprite('source/image/wall.png', 100, 190, 700, 20)
w3 = GameSprite('source/image/wall.png', 0, 290, 700, 20)
w4 = GameSprite('source/image/wall.png', 100, 390, 700, 20)
w5 = GameSprite('source/image/wall.png', 0, 490, 700, 20)

#добавляем стены в группу
walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)

#создаем спрайты врагов
frag1 = Enemy('source/image/frag.png', 740, 130, 40, 40, frag_speed)
frag2 = Enemy('source/image/frag.png', 20, 230, 40, 40, frag_speed)
frag3 = Enemy('source/image/frag.png', 740, 330, 40, 40, frag_speed)
frag4 = Enemy('source/image/frag.png', 20, 430, 40, 40, frag_speed)

#добавляем врагов в группу 
frags = sprite.Group()
frags.add(frag1)
frags.add(frag2)
frags.add(frag3)
frags.add(frag4)

hero = Player('source/image/hero.png', 5, 5, 50, 50, 0, 0)
target = GameSprite('source/image/target.png', 10, 510, 100, 100)

#создаем группу для пуль
bullets = sprite.Group()

#музыка
mixer.init()
mixer.music.load('source/sound/space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('source/sound/fire.ogg')
#win_sound = mixer.Sound('source/sound/win.ogg')
#lose_sound = mixer.Sound('source/sound/lose.ogg')

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 255, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))



#игровой цикл
game = True
finish = False

while game:
    window.fill(back)#закрашиваем окно цветом
    #window.blit(background,(0, 0))#закрашиваем окно фоновым изображением  
   
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                hero.x_speed = -5
            elif e.key == K_RIGHT:
                hero.x_speed = 5
            elif e.key == K_UP:
                hero.y_speed = -5
            elif e.key == K_DOWN:
                hero.y_speed = 5
            elif e.key == K_SPACE:
                hero.fire()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                hero.x_speed = 0
            elif e.key == K_RIGHT:
                hero.x_speed = 0
            elif e.key == K_UP:
                hero.y_speed = 0
            elif e.key == K_DOWN:
                hero.y_speed = 0
    
    if not finish:
        window.fill(back)#закрашиваем окно цветом

        #запускаем движения спрайтов
        hero.update()
        bullets.update()

        #обновляем их в новом местоположении при каждой итерации цикла
        hero.reset()
        target.reset()

        bullets.draw(window)
        walls.draw(window)

        sprite.groupcollide(frags, bullets, True, True)
        frags.update()
        frags.draw(window)
        sprite.groupcollide(bullets, walls, True, False)

        #Проверка столкновения героя с врагами и стенами
        frags_touched = sprite.spritecollide(hero, frags, False)
        if frags_touched:
            finish = True
            # #вычисляем отношение
            # img = image.load('source/image/game-over.png')
            # d = img.get_width() // img.get_height()
            # window.fill((255, 255, 255))
            # window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
            window.blit(lose, (200, 200))
            #lose_sound.play()

        if sprite.collide_rect(hero, target):
            finish = True
            # img = image.load('source/image/win.jpg')
            # window.fill((255, 255, 255))
            # window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            window.blit(win, (200, 200))
            #win_sound.play()
            time.delay(3000)
            break

#!!!! bonus - 
    else:
        finish = False

        for b in bullets:
            b.kill()
        for f in frags:
            f.kill()

        time.delay(3000)
        
        hero = Player('source/image/hero.png', 5, 5, 40, 40, 0, 0)

        frag1 = Enemy('source/image/frag.png', 740, 130, 40, 40, frag_speed)
        frag2 = Enemy('source/image/frag.png', 20, 230, 40, 40, frag_speed)
        frag3 = Enemy('source/image/frag.png', 740, 330, 40, 40, frag_speed)
        frag4 = Enemy('source/image/frag.png', 20, 430, 40, 40, frag_speed)

        #добавляем врагов в группу 
        frags = sprite.Group()
        frags.add(frag1)
        frags.add(frag2)
        frags.add(frag3)
        frags.add(frag4)
    
    display.update()
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)
