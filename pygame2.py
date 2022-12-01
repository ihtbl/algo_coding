from pygame import *
from random import randint

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

mixer.init()
mixer.music.load('C:/Users/annah/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/pygame/space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('C:/Users/annah/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/pygame/fire.ogg')

width = 700
height  = 500
fps = 60

img_back = "C:/Users/annah/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/pygame/galaxy.jpg"
img_bullet = "C:/Users/annah/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/pygame/bullet.png"
img_hero = "C:/Users/annah/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/pygame/rocket.png"
img_enemy = "C:/Users/annah/AppData/Local/Programs/Algoritmika/vscode/data/extensions/algoritmika.algopython-20220124.142703.0/temp/pygame/ufo.png"
score = 0
goal = 10
lost = 0
max_lost = 3

window = display.set_mode((width,height))
display.set_caption("shooting game")
clock = time.Clock()

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
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0
            lost = lost + 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

background = transform.scale(image.load(img_back), (width, height))
rocket = Player(img_hero, 5, height -100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    if not finish:
        window.blit(background, (0,0))

        rocket.update()
        monsters.update()
        bullets.update()

        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(rocket, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        
        text = font2.render("Score:" +str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed:" +str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

    time.delay(50)





