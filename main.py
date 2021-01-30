import random
import sys
import pygame
import function

pygame.init()
AI = 1
screen = pygame.display.set_mode((288, 512))  # 288 512
background = pygame.image.load("./assets/background.png")
pygame.display.set_caption("Flappy Bird")


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.birdSprites = [pygame.image.load("assets/0.png"), pygame.image.load("assets/1.png"),
                            pygame.image.load("assets/2.png")]  # 生成一个列表
        self.a = 0
        self.birdX = 10
        self.birdY = 100
        self.jumpSpeed = 4
        self.gravity = 0.25
        self.rect = self.birdSprites[self.a].get_rect()
        self.rect.center = (self.birdX, self.birdY)

    def birdUpdate(self):
        self.jumpSpeed -= self.gravity
        self.birdY -= self.jumpSpeed
        self.rect.center = (self.birdX, self.birdY)
        if self.jumpSpeed < 0:
            self.a = 1
        if self.jumpSpeed > 0:
            self.a = 2

    def birdCrush(self):
        global keep_going
        global Code
        global score
        global time
        global point
        global populations
        global epoch
        global environment
        resultU = self.rect.colliderect(newWall.wallUpRect)
        resultD = self.rect.colliderect(newWall.wallDownRect)

        if resultU or resultD or newBird.rect.bottom >= ground.rect.top or newBird.birdY < -400:
            score.append(time - (environment[0] ** 2 + environment[1] ** 2) ** 0.5 + point * 200)
            hit = pygame.mixer.Sound('sound/hit.WAV')
            channel_3 = pygame.mixer.Channel(2)
            channel_3.play(hit)
            print("第%s轮第%s号个体得分：" % (epoch, Code) + str(
                time - (environment[0] ** 2 + environment[1] ** 2) ** 0.5 + point * 200))
            Code += 1
            time = 0
            point = 0
            # 一轮Code只鸟
            if Code == 10:
                # 杂交，变异
                rank = sorted(list(zip(score, populations)))[::-1]
                print("该轮最高得分：" + str(rank[0][0]))
                father = rank[0:10]
                mother = rank[0:10]
                random.shuffle(mother)
                populations = []
                Code = 0
                score = []
                epoch += 1
                for i in range(5):
                    populations.append(function.Variation(function.Crossover(father[i][1], mother[i][1])))
                    populations.append(function.Variation(function.Crossover(father[i][1], mother[i][1])))

            keep_going = False


class Wall():
    def __init__(self):
        self.wallUp = pygame.image.load("assets/bottom.png")
        self.wallDown = pygame.image.load("assets/top.png")
        self.wallUpRect = self.wallUp.get_rect()
        self.wallDownRect = self.wallDown.get_rect()
        self.gap = 30  # 缝隙间隔
        self.wallx = 288
        self.offset = 0

        self.wallUpY = 360 + self.gap - self.offset
        self.wallDownY = 0 - self.gap - self.offset

        self.wallUpRect.center = (self.wallx, self.wallUpY)
        self.wallDownRect.center = (self.wallx, self.wallDownY)

    def wallUpdate(self):
        self.wallx -= 1

        self.wallUpRect.center = (self.wallx, self.wallUpY)
        self.wallDownRect.center = (self.wallx, self.wallDownY)

        if self.wallx < -20:
            self.wallx = 288
            self.offset = random.randint(-80, 80)
            self.wallUpY = 360 + self.gap - self.offset
            self.wallDownY = 0 - self.gap - self.offset


class Text():

    def __init__(self, content):
        red = (100, 50, 50)
        self.color = red
        self.font = pygame.font.SysFont(None, 52)

        contentStr = str(content)
        self.image = self.font.render(contentStr, True, self.color)

    def updateText(self, content):
        contentStr = str(content)
        self.image = self.font.render(contentStr, True, self.color)


class Ground():
    def __init__(self):
        self.image = pygame.image.load("assets/ground.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = 560
        self.rect.left = -30


epoch = 0  # 已经进行的轮数
time = 0  # 存活时间
point = 0  # 得分
coolText = Text(point)
newBird = Bird()
newWall = Wall()
keep_going = True
clock = pygame.time.Clock()
ground = Ground()
populations = []
score = []
for i in range(20):
    populations.append(function.Generate_chromosome())
Code = 0
while True:
    # 感知环境并作出决策
    environment = [newBird.birdX - newWall.wallx,
                   newBird.birdY - (newWall.wallUpY + newWall.wallDownY) / 2,
                   newBird.jumpSpeed * 20]
    possibilty = function.Predict(populations[Code], environment)
    if possibilty >= 0.5:
        action = 1
    else:
        action = 0

    if newBird.rect.top > ground.rect.top:
        newBird.rect.centery = ground.rect.top
    else:
        if newBird.rect.right == newWall.wallUpRect.right:
            point = point + 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and AI == 0:
            newBird.jumpSpeed = 3
            channel_2 = pygame.mixer.Channel(3)
            fly = pygame.mixer.Sound('sound/fly.WAV')
            channel_2.play(fly)
    screen.blit(background, (0, 0))
    screen.blit(newBird.birdSprites[newBird.a], newBird.rect)
    screen.blit(newWall.wallUp, newWall.wallUpRect)
    screen.blit(newWall.wallDown, newWall.wallDownRect)
    screen.blit(ground.image, ground.rect)
    screen.blit(coolText.image, (10, 10))
    newWall.wallUpdate()
    newBird.birdUpdate()
    if action == 0 and AI == 1:
        newBird.jumpSpeed = 4
        channel_2 = pygame.mixer.Channel(3)
        fly = pygame.mixer.Sound('sound/fly.WAV')
        channel_2.play(fly)
    if keep_going:
        newBird.birdCrush()
        coolText.updateText(point)
    else:
        newBird = Bird()
        newWall = Wall()
        keep_going = True
    pygame.display.update()
    if point >= 10 or AI != 1:
        clock.tick(60)
    else:
        clock.tick(300)
    time = time + 1
