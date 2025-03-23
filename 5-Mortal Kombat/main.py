import pygame
import player
from menu import MainMenu
from constants import WIDTH, HEIGHT, FPS, DARK_RED, BLACK, WHITE


class Game:
    def __init__(self):
        pygame.init()
        # Fonts
        self.font_bg = pygame.font.SysFont('Arial', 45, bold=True)
        self.font = pygame.font.SysFont('Arial', 40, bold=True)
        self.font_timer = pygame.font.SysFont("Arial", 25)
        self.font_go = pygame.font.SysFont("Arial", 75)
        # Images
        self.background_img = pygame.image.load("assets/images/bg2.png")
        self.bg = pygame.image.load('assets/images/bg3.png')
        # Init
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('FIGHTER')
        # Players
        self.player = player.Player(
            120, 85, 'player', 'scorpion_red_sprites', hb_x=20, hb_text_x=40, flip=False)
        self.enemy = player.Player(
            500, 85, 'enemy', 'scorpion_sprites', hb_x=430, hb_text_x=700, flip=True)
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.all_sprite_list.add(self.enemy)
        self.timer = player.Timer(378, 10, 1200)
        self.player.enemy = self.enemy
        self.enemy.enemy = self.player

        self.main_menu = MainMenu(300, 200)
        self.state = "START"

    def state_update(self):
        if (self.player.hb.hp == 0 or self.enemy.hb.hp == 0 or self.timer.indx/10 <= 0) and self.state != 'FINISH':
            self.state = 'FINISH'
            self.timer.stop = True

    def draw_states(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background_img, [0, 0])
        if self.state == "START":
            self.main_menu.draw(self.screen)

        elif self.state == "GAME":
            self.screen.blit(self.bg, (0, 0))
            self.all_sprite_list.draw(self.screen)
            self.enemy.hb.draw(self.screen, self.font)
            self.player.hb.draw(self.screen, self.font)
            self.timer.draw(self.screen, self.font_timer)

        elif self.state == "PAUSE":
            self.platform_list.draw(self.screen)
            self.main_menu.draw(self.screen)

        elif self.state == "FINISH":
            self.screen.blit(self.bg, (0, 0))
            self.all_sprite_list.draw(self.screen)
            self.enemy.hb.draw(self.screen, self.font)
            self.player.hb.draw(self.screen, self.font)
            self.timer.draw(self.screen, self.font_timer)
            text = self.font.render('GAME  OVER', True, DARK_RED)
            self.screen.blit(text, (300, 60))

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                active_button = self.main_menu.handle_mouse_event(event)
                if event.type == pygame.QUIT:
                    done = True
                if active_button:
                    active_button.state = 'normal'

                    if active_button.name == 'START':
                        self.state = 'GAME'

                    elif active_button.name == 'CONTINUE':
                        self.state = 'GAME'

                    elif active_button.name == 'QUIT':
                        done = True

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.player.go_left()
                    if event.key == pygame.K_RIGHT:
                        self.player.go_right()
                    if event.key == pygame.K_SPACE:
                        self.player.attack = True

                    # 2 Player
                    if event.key == pygame.K_a:
                        self.enemy.go_left()
                    if event.key == pygame.K_d:
                        self.enemy.go_right()
                    if event.key == pygame.K_q:
                        self.enemy.attack = True

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.player.stop()
                    if event.key in [pygame.K_a, pygame.K_d]:
                        self.enemy.stop()
            
            self.main_menu.update()
            self.state_update()
            self.draw_states()
            self.timer.update()
            self.all_sprite_list.update()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


game = Game()
game.run()
