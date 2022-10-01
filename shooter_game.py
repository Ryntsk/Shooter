from pygame import *
from random import*

window = display.set_mode((700,500))
display.set_caption("Supe Mega Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700,500))

game=True
finish=False
FPS=60
clock=time.Clock()

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire=mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y, size_x, size_y,player_speed):
        super().__init__()
        self.direction="right"
        self.image=transform.scale(image.load(player_image), (65,65))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def Update(self):
        keys= key.get_pressed()
        if keys[K_RIGHT] and self.rect.x<630:
            self.rect.x+=self.speed
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 0.75, 1, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>510:
            self.rect.y=0
            self.rect.x=randint(80,620)
            lost+=1
class Bullet(GameSprite):
    def update(self):
            self.rect.y+=self.speed
            if self.rect.y<0:
                self.kill()

font.init()
font=font.SysFont('Arial',36)
lost=0
count=0

text_count=font.render('Счёт:'+ str(count),1,(255,255,255))
win=font.render('Победа!',1,(255,0,0))
lose=font.render('Проигрышь',1,(255,0,0))
bullets=sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy("ufo.png", randint(80, 700 - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

Rocket=Player('rocket.png',475,400,80,100,10)



while game:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            game = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                Rocket.fire()
    #сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
    #производим движения спрайтов
        Rocket.Update()
        monsters.update()
        bullets.update()

        #обновляем их в новом местоположении при каждой итерации цикла
        Rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            count = count + 1
            monster = Enemy("ufo.png", randint(80, 500 - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(Rocket, monsters, False) or lost >= 10:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose , (300, 200))

        #проверка выигрыша: сколько очков набрали?
        if count >= 10:
            finish = True
            window.blit(win, (300, 200))

        #пишем текст на экране
        text = font.render("Счет: " + str(count), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()

    time.delay(50)