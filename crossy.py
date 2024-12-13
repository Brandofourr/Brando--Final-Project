
import pygame as p
import time

#Chicken Class
class Chicken(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = HEIGHT / 2
        self.vel = 4
        self.width = 100
        self.height = 50


        self.chicken1 = p.image.load('Chicken1.png')
        self.chicken2 = p.image.load('Chicken2.png')
        self.chicken3 = p.image.load('Chicken3.png')
        self.chicken4 = p.image.load('Chicken4.png')
        self.chicken1 = p.transform.scale(self.chicken1, (self.width, self.height))
        self.chicken2 = p.transform.scale(self.chicken2, (self.width, self.height))
        self.chicken3 = p.transform.scale(self.chicken3, (self.width, self.height))
        self.chicken4 = p.transform.scale(self.chicken4, (self.width, self.height))
        self.image = self.chicken1
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.movement()
        self.correction()
        self.getCollision()
        self.rect.center = (self.x, self.y)
    
    def movement(self):
        keys = p.key.get_pressed()
        if keys[p.K_RIGHT]:
            self.x += self.vel
            self.image = self.chicken1

        elif keys[p.K_LEFT]:
            self.x -= self.vel
            self.image = self.chicken2

        if keys[p.K_UP]:
            self.y -= self.vel
            self.image = self.chicken3
            
        elif keys[p.K_DOWN]:
            self.y += self.vel
            self.image = self.chicken4
            
    def correction(self):
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2

        elif self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2

    def getCollision(self):
        carCheck = p.sprite.spritecollide(self, carGroup, False, p.sprite.collide_mask)
        if carCheck:
            Explosion.explode(self.x, self.y)

#Car Class
class Car(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        if number == 1:
            self.x = 190
            self.image = p.image.load('SlowCar.png')
            self.vel = -4

        else:
            self.x = 460
            self.image = p.image.load('FastCar.png')
            self.vel = 5

        self.y = HEIGHT / 2
        self.width = 100
        self.height = 150
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.movement()
        self.rect.center = (self.x, self.y)

    def movement(self):
        self.y += self.vel

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
            self.vel *= -1

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2
            self.vel *= -1

#Screen Class
class Screen(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.im1 = p.image.load('Scene.png')
        self.im2 = p.image.load('Winner.png')
        self.im3 = p.image.load('Loser.png')

        self.im1 = p.transform.scale(self.im1, (WIDTH, HEIGHT))
        self.im2 = p.transform.scale(self.im2, (WIDTH, HEIGHT))
        self.im3 = p.transform.scale(self.im3, (WIDTH, HEIGHT))

        self.image = self.im1
        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)

#Food Class
class Food(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number

        if self.number == 1:
            self.image = p.image.load('Cornmeal2.png')
            self.visible = False
            self.x = 50

        else:
            self.image = p.image.load('Cornmeal1.png')
            self.visible = True
            self.x = 580

        self.y = HEIGHT / 2
        self.image = p.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        if self.visible:
            self.collision()
            self.rect.center = (self.x, self.y)

    def collision(self):
        global SCORE, cat

        gotFood = p.sprite.spritecollide(self, chickenGroup, False, p.sprite.collide_mask)
        if gotFood:
            self.visible = False

            if self.number == 1:
                Cornmeal1.visible = True
                if SCORE < 5:
                    SwitchLevel()

                else:
                    chickenGroup.empty()
                    DeleteOtherItems()

                    EndScreen(1)

            else:
                Cornmeal2.visible = True

#Explosion Class
class Explosion(object):
    def __init__(self):
        self.costume = 1
        self.width = 140
        self.height = 140
        self.image = p.image.load('Explosion' + str(self.costume) + '.png')
        self.image = p.transform.scale(self.image, (self.width, self.height))

    def explode(self, x, y):
        x = x - self.width / 2
        y = y - self.height / 2
        DeleteCat()

        while self.costume < 6:
            self.image = p.image.load('Explosion' + str(self.costume) + '.png')
            self.image = p.transform.scale(self.image, (self.width, self.height))
            win.blit(self.image, (x, y))
            p.display.update()

            self.costume += 1
            time.sleep(0.1)

        DeleteOtherItems()
        EndScreen(0)

#Game Functions
def scoreDisplay():
    global gameOn
    global score_font
    if gameOn:
        score_font = p.font.Font(None, 36)
        score_text = score_font.render(str(SCORE) + ' / 5', True, (0, 0, 0))
        win.blit(score_text, (255, 10))


def getFood():
    Food = []
    for f in Food:
        if not f.visible:
            f.kill()

        else:
            if not f.alive():
                foodGroup.add(f)


def SwitchLevel():
    global SCORE

    if slowCar.vel < 0:
        slowCar.vel -= 1

    else:
        slowCar.vel += 1

    if fastCar.vel < 0:
        fastCar.vel -= 1

    else:
        fastCar.vel += 1

    SCORE += 1


def DeleteChicken():
    global chicken

    chicken.kill()
    screenGroup.draw(win)
    carGroup.draw(win)
    foodGroup.draw(win)

    screenGroup.update()
    carGroup.update()
    flagGroup.update()

    p.display.update()


def DeleteOtherItems():
    carGroup.empty()
    foodGroup.empty()
    foods.clear()


def EndScreen(n):
    global gameOn

    gameOn = False

    if n == 0:
        bg.image = bg.im3

    elif n == 1:
        bg.image = bg.im2

#Global Game Methods
WIDTH = 640
HEIGHT = 480

p.init()

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('Crossy Road')
clock = p.time.Clock()

SCORE = 0
scoreFont = p.font.SysFont('Arial', 80, True)

s = Screen()
screenGroup = p.sprite.Group()
screenGroup.add(s)

chicken = Chicken()
chickenGroup = p.sprite.Group()
chickenGroup.add(chicken)

slowCar = Car(1)
fastCar = Car(2)
carGroup = p.sprite.Group()
carGroup.add(slowCar, fastCar)

Cornmeal2 = Food(1)
Cornmeal1 = Food(2)
foodGroup = p.sprite.Group()
foodGroup.add(Cornmeal2, Cornmeal1)
foods = [Cornmeal2, Cornmeal1]

explode = Explosion()

gameOn = True
run = True
while run:
    clock.tick(60)
    for e in p.event.get():
        if e.type == p.QUIT:
            run = False

    screenGroup.draw(win)

    scoreDisplay()
    getFood()

    carGroup.draw(win)
    chickenGroup.draw(win)
    foodGroup.draw(win)

    carGroup.update()
    chickenGroup.update()
    foodGroup.update()

    screenGroup.update()

    p.display.update()

p.quit()



