import pygame
from pygame.locals import *
import random
import button
import textButton

pygame.init()

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Frosty Dash')

# Load images
game_bg = pygame.image.load('images/bg.png')

# define game variables
game_started = False
menu_state = "main"
rows = 1  # single "row" of fire
cols = 6  # 4 "colums" of fire
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0  # 0 means no game over, -1 means player lost
difficulty = "normal"
clicked = False
# define fonts
font30 = pygame.font.SysFont('Roboto', 34)
font40 = pygame.font.SysFont('Roboto', 50)
fontMain = pygame.font.SysFont('arialblack', 40)
# define colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# load button images
play_img = pygame.image.load("images/PlayButton.png").convert_alpha()
options_img = pygame.image.load("images/OptionsButton.png").convert_alpha()
controls_img = pygame.image.load("images/ControlsButton.png").convert_alpha()
quit_img = pygame.image.load("images/QuitButton.png").convert_alpha()
back_img = pygame.image.load("images/BackButton.png").convert_alpha()
revert_img = pygame.image.load("images/RevertButton.png").convert_alpha()

# create button instances
play_button = button.Button(300, 125, play_img, 0.5)
options_button = button.Button(297, 250, options_img, 0.5)
controls_button = button.Button(297, 375, controls_img, 0.5)
quit_button = button.Button(300, 500, quit_img, 0.5)
back_button = button.Button(300, 625, back_img, 0.5)
revert_button = button.Button(200, 625, revert_img, 0.5)


# define function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health

    def update(self):
        # set movement speed
        speed = 8
        game_over = 0
        # get keys pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT] and self.rect.left > -2:
            self.rect.x -= speed
        elif key[pygame.K_d] or key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH + 1:
            self.rect.x += speed

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            self.kill()
            game_over = -1
        return game_over


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/fire.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # set movement
        if difficulty == 'normal':
            speed = 3
        elif difficulty == 'easy':
            speed = 2
        elif difficulty == 'hard':
            speed = 5
        self.rect.y += speed
        # reset location after hitting bottom of screen
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-800, -100)
            self.rect.x = random.randint(5, SCREEN_WIDTH)
        # collisions - reset position after collision
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.rect.y = random.randint(-800, -100)
            player.health_remaining -= 1
        # print(self.rect.y)


# create sprite groups
player_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()


# create fire
def create_fire():
    # generate fire
    for row in range(rows):
        for item in range(cols):
            fire = Fire(random.randint(10, 700) + item * 100, random.randint(-250, -50) + row * 70)
            fire_group.add(fire)


create_fire()

# create player
player = Player(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, 3)

# add to groups
player_group.add(player)

clock = pygame.time.Clock()
run = True

while run:
    # check the game has started
    if game_started is False:
        screen.fill((52, 78, 91))
        # check the menu state
        if menu_state == "main":
            # draw menu buttons
            if play_button.draw(screen):
                game_started = True
            if options_button.draw(screen):
                menu_state = "options"
            if controls_button.draw(screen):
                menu_state = "controls"
            if quit_button.draw(screen):
                run = False
            draw_text('Use the options menu to change game difficulty.', font30, white, 100,680)
            draw_text('Use the controls menu to learn the game basics.', font30, white, 100,710)
        if menu_state == "options":
            # draw back button
            if back_button.draw(screen):
                menu_state = "main"
            # draw difficulty buttons
            old_difficulty = difficulty
            EASY_MOUSE_POS = pygame.mouse.get_pos()
            NORMAL_MOUSE_POS = pygame.mouse.get_pos()
            HARD_MOUSE_POS = pygame.mouse.get_pos()
            DIFFICULTY_TEXT = draw_text('Select Difficulty:', font30, white, 200, 260)
            draw_text('Easy difficulty will slow tthe fire balls, while hard speeds them up', font30, white, 100, 500)
            draw_text('Use the counter clockwise arrow to revert changes', font30, white, 100, 540)
            draw_text('Note: Changes will be saved after clicking Back', font30, white, 100, 580)

            #EASY_TEXT = draw_text('EASY', font30, white, 400, 260)
            #NORMAL_TEXT = draw_text('NORMAL', font30, white, 480, 260)
            #HARD_TEXT = draw_text('HARD', font30, white, 600, 260)
            #EASY_RECT = EASY_TEXT.get_rect(center=(640, 260))
            #screen.blit(EASY_TEXT, EASY_RECT)
            EASY_SELECT = textButton.TextButton(image=None, pos=(430, 273), text_input="EASY", font=font30, base_color="White", hovering_color="Green")
            NORMAL_SELECT = textButton.TextButton(image=None, pos=(530, 273), text_input="NORMAL", font=font30, base_color="White", hovering_color="Green")
            HARD_SELECT = textButton.TextButton(image=None, pos=(630, 273), text_input="HARD", font=font30, base_color="White", hovering_color="Green")

            EASY_SELECT.changeColor(EASY_MOUSE_POS)
            EASY_SELECT.update(screen)
            NORMAL_SELECT.changeColor(EASY_MOUSE_POS)
            NORMAL_SELECT.update(screen)
            HARD_SELECT.changeColor(EASY_MOUSE_POS)
            HARD_SELECT.update(screen)
            if pygame.mouse.get_pressed():
                clicked = True
                if EASY_SELECT.checkForInput(EASY_MOUSE_POS):
                    difficulty = 'easy'
                if NORMAL_SELECT.checkForInput(NORMAL_MOUSE_POS):
                    difficulty = 'normal'
                if HARD_SELECT.checkForInput(HARD_MOUSE_POS):
                    difficulty = 'hard'
            if clicked:
                if revert_button.draw(screen):
                    difficulty = old_difficulty
            if NORMAL_SELECT.checkForInput(NORMAL_MOUSE_POS):
                difficulty = 'normal'
            if HARD_SELECT.checkForInput(HARD_MOUSE_POS):
                difficulty = 'hard'
            #print(difficulty)
        if menu_state == "controls":
            draw_text('Welcome to Frosty Dash!', font40, white, int(SCREEN_WIDTH / 2 - 200), int(SCREEN_HEIGHT / 2 - 250))
            draw_text('The objective of the game is to dodge the falling fire balls.', font30, white, int(SCREEN_WIDTH / 2 - 400), int(SCREEN_HEIGHT / 2 - 200))
            draw_text('To move, use the left and right arrow keys or use the A key to move.', font30, white, int(SCREEN_WIDTH / 2 - 400), int(SCREEN_HEIGHT / 2 - 140))
            draw_text('left and the D key to move right.', font30, white, int(SCREEN_WIDTH / 2 - 400), int(SCREEN_HEIGHT / 2 - 110))
            if back_button.draw(screen):
                menu_state = "main"

    else:
        screen.blit(game_bg, (0, 0))

        if countdown == 0:

            if game_over == 0:
                # update player
                game_over = player.update()

                # update sprite groups
                fire_group.update()
            elif game_over == -1:
                draw_text('GAME OVER!', font40, white, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 - 110))
                draw_text('Press 1 to play again or 2 to go to main menu.', font30, white, int(SCREEN_WIDTH / 2 - 140), int(SCREEN_HEIGHT / 2 - 50))
                key = pygame.key.get_pressed()
                if key[pygame.K_1]:
                    player = Player(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, 3)
                    player_group.add(player)
                    for item in fire_group:
                        item.kill()
                    create_fire()
                    game_over = 0
                if key[pygame.K_2]:
                    menu_state = 'main'
                    game_started = False
                    player = Player(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, 3)
                    player_group.add(player)
                    for item in fire_group:
                        item.kill()
                    create_fire()
                    game_over = 0

            # draw sprite groups
            player_group.draw(screen)
            fire_group.draw(screen)

        if countdown > 0:
            draw_text('GET READY!', font40, white, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 - 110))
            draw_text(str(countdown), font30, white, int(SCREEN_WIDTH / 2 - 10), int(SCREEN_HEIGHT / 2 - 50))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick()
    print(clock.get_fps())

pygame.quit()
