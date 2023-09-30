from pygame import *
from random import *
from time import time as timer


rel_time = False

num_fire = 0


font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN' , True, (0, 180, 0))
lose = font1.render('YOU LOSE' , True, (180, 0, 0))

score = 0
goal = 10
lost = 0

max_lost = 3

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Space Shooter')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

font2 = font.SysFont('Arial', 36)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

a = 50
b = 600

bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (45,    45))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png ', self.rect.centerx   , self.rect.top, -15) 
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

game = True
finish = False

player = Player('rocket.png', randint(a, b), 400, 15)
clock = time.Clock()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1, 5))
    monsters.add(monster)

while game :
    for e in event.get():
        if e.type == QUIT:
            game = False  
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True                  
    
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        player.reset()

        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text , (10,20))
        
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(3, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        monsters.update()
        bullets.update()
        
        monsters.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

    display.update()
   
    

    time.delay(50)
