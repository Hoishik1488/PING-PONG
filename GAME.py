from pygame import *
from random import *
import time as tm

lost1 = 0
lost2 = 0
seconds = 0

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 40)

win_w = 600
win_h = 500

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed = 5, width = 65, height = 65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys  = key.get_pressed()
        if keys [K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys [K_s] and self.rect.y < win_h - 80:
            self.rect.y += self.speed
    def update_l(self):
        keys  = key.get_pressed()
        if keys [K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys [K_DOWN] and self.rect.y < win_h - 80:
            self.rect.y += self.speed  

BLACK = (0, 0, 0)

class Ball(sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [randint(4, 8), randint(-8, 8)]
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.x = self.rect.x + self.velocity[0]
        self.rect.y = self.rect.y + self.velocity[1]
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)

game_state = "start_menu"

def draw_start_menu():
    screen_width = 750
    screen_height = 450
    window.fill((0, 0, 0))
    fontq = font.SysFont('arial', 40)
    title = font1.render('PING-PONG', True, (255, 255, 255))
    start_button = font1.render('Start', True, (255, 255, 255))
    window.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/2))
    window.blit(start_button, (screen_width/2 - start_button.get_width()/2, screen_height/2 + start_button.get_height()/2))
    display.update()

def draw_game_over_screen():
    screen_width = 750
    screen_height = 450
    window.fill((0, 0, 0))
    font2 = font.SysFont('arial', 40)
    title = font2.render('Game Over', True, (255, 255, 255))
    restart_button = font2.render('R - Restart', True, (255, 255, 255))
    quit_button = font2.render('Q - Quit', True, (255, 255, 255))
    window.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/3))
    window.blit(restart_button, (screen_width/2 - restart_button.get_width()/2, screen_height/1.9 + restart_button.get_height()))
    window.blit(quit_button, (screen_width/2 - quit_button.get_width()/2, screen_height/2 + quit_button.get_height()/2))
    display.update()

window = display.set_mode((win_w, win_h))
display.set_caption("PING PONG")
backgrounds = (0,0,0)

mixer.init()
game = True
finish = False
clock = time.Clock()
FPS = 60

speed_x = 3
speed_y = 3

player1 = Player('racket-removebg-preview.png', 30, 200,8,50,150)
player2 = Player('racket-removebg-preview.png', 520,200,8,50,150)
ball = GameSprite('ball.png', 200,200,4,45,45)

def save():
    global lost1, lost2, ball
    if ball.rect.x < 0:
        lost1 += 1
        mixer.music.load('fallingPipe.mp3')
        mixer.music.play()
        ball = GameSprite('ball.png', 200,200,4,45,45)
    if ball.rect.x > 550:
        lost2 += 1
        mixer.music.load('fallingPipe.mp3')
        mixer.music.play()
        ball = GameSprite('ball.png', 200,200,4,45,45)

def gg():
    global lost1, lost2
    if lost1 <= 10:
        lost1 = 0
        player1 = Player('racket-removebg-preview.png', 30, 200,8,50,150)
        player2 = Player('racket-removebg-preview.png', 520,200,8,50,150)
        ball = GameSprite('ball.png', 200,200,4,45,45)
    if lost2 <= 10:
        lost2 = 0
        player1 = Player('racket-removebg-preview.png', 30, 200,8,50,150)
        player2 = Player('racket-removebg-preview.png', 520,200,8,50,150)
        ball = GameSprite('ball.png', 200,200,4,45,45)

def timer():
    global seconds, game
    start_ticks=time.get_ticks()
    while game:
        seconds=(time.get_ticks()-start_ticks)/1000 
        for e in event.get():
            if e.type == QUIT:
                game = False
        if seconds>10: 
            break
        window.fill(backgrounds)
        window.blit(font2.render(str(seconds), 1, (255, 255, 255)), (300,300))
        display.update()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if game_state == "start_menu":
       draw_start_menu()
       keys = key.get_pressed()
       if keys[K_SPACE]:
           game_state = "game"
           game_over = False
           timer()
    elif game_state == "game_over":
       draw_game_over_screen()
       keys = key.get_pressed()
       if keys[K_r]:
           game_state = "start_menu"
       if keys[K_q]:
           quit()
    elif game_state == 'game':
        if finish != True:  
            player1.update_r()
            player2.update_l()
            ball.update()

            ball.rect.x += speed_x
            ball.rect.y += speed_y

            if sprite.collide_rect(player1, ball) or sprite.collide_rect(player2, ball):
                speed_x *= -1
                mixer.music.load('ballColliding.wav')
                mixer.music.play()
            if ball.rect.y > win_h - 50 or ball.rect.y < 0:
                speed_y *= -1

            save()    

            window.fill(backgrounds)
            ball.reset()
            player1.reset()
            player2.reset()
            window.blit(font1.render("Player 2: " + str(lost1), 1, (255, 255, 255)), (0,50))
            window.blit(font1.render("Player 1: " + str(lost2), 1, (255, 255, 255)), (0,0))
            if lost2 == 10:
                window.blit(font2.render("Player 1 win!", 1, (255, 255, 255)), (250,250))
                gg()
                game_over = True
                game_state = "game_over" 
            if lost1 == 10:
                window.blit(font2.render("Player 2 win!", 1, (255, 255, 255)), (250,250))
                gg()
                game_over = True
                game_state = 'game_over'
        if game_over:
            game_state = "game_over"
            game_over = False
    display.update()
    clock.tick(FPS)