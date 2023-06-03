from pygame import *

from random import randint
from pygame.locals import *


width, height = 640, 480
screen = display.set_mode((width, height))

x, y = 100, 100

jump_speed = 10

gravity = 0.5
is_jumping = False

font.init()
font1 = font.Font(None, 80)
lose = font1.render("YOU'RE KILLED!", True, (180, 0, 0))
font2 = font.Font(None, 36)

img_back = "sky1.png" #фон 
img_mario = "mario.png" #герой
img_enemy = "brik.png" #кирпичи(враги)

score = 0 
lost = 0 


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, jump_power):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.jump_power = jump_power
        self.is_jumping = False
        self.jump_count = 10
 
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
        if keys[K_SPACE] and not self.is_jumping:
            self.is_jumping = True
 
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10
 
    

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



win_width = 700
win_height = 500
display.set_caption("Mario")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
human = Player(img_mario, 5, win_height - 100, 80, 100, 10, 10)
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

finish = False
run = True 
while run:
    for i in event.get():
        if i.type == QUIT:
            run = False
            
        if i.type == KEYDOWN:
            if i.key == K_SPACE and not is_jumping:
                is_jumping = True

    if is_jumping:
        y -= jump_speed 
        jump_speed -= gravity
        
        if jump_speed < -10:
            is_jumping = False
            jump_speed = 10       
   
    if not finish:
        window.blit(background,(0,0))

        human.update()
        monsters.update()
        
        human.reset()
        monsters.draw(window)

        collides = sprite.spritecollide(human, monsters, False)
        # screen.fill((0, 0, 0))
        # draw.rect(screen, (255,255, 235),(x, y, 50, 50))
        # display.flip()   

        # for c in collides:
        #     score = score + 1
        #     monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        #     monsters.add(monster)
        
        if sprite.spritecollide(human, monsters, False):
            finish = True
            #run = False
            window.blit(lose, (200, 200))

        text_lose = font2.render("Избегнуто кирпичей: " + str(lost), 1, (20, 46, 250))
        window.blit(text_lose, (10, 50))
        

    else:
        finish = False
        score = 0
        lost = 0
        for m in monsters:
            m.kill()


        time.delay(2000)
        for i in range(1, 5):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    display.update()    
    time.delay(50)
