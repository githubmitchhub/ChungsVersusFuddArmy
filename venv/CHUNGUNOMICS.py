import pygame
import math
import random
from pygame import mixer

pygame.init()

mixer.music.load('Tribal Ritual.wav')
mixer.music.play(-1)
pygame.mixer.music.set_volume(.3)

screen = pygame.display.set_mode((1024, 768))

background = pygame.image.load('forest.jpg')
gameIcon = pygame.image.load('chung.png')
pygame.display.set_icon(gameIcon)


def main():
    sup = mixer.Sound('whatsup.wav')
    sup.set_volume(.1)

    fudd_Sound = mixer.Sound('elmer07.wav')
    fudd_Sound.set_volume(.2)
    fudd_Sound.play()

    global game_over
    game_over = False
    global bullet_state
    global bullet_Sound
    bullet_Sound = mixer.Sound('poo.wav')
    bullet_Sound.set_volume(.12)

    pygame.display.set_caption("CHUNGUS VS FUDD ARMY")

    playerImg = pygame.image.load('chung.png')
    playerX = 512
    playerY = 620
    playerX_change = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 30
    score_value = 0

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('pngbarn.png'))
        enemyX.append(random.randint(0, 960))
        enemyY.append(random.randint(20, 25))
        enemyX_change.append(random.randint(3, 9))
        enemyY_change.append(25)

    bulletImg = pygame.image.load('imageedit_3_4617970527.png')
    bulletX = 0
    bulletY = 600
    bulletX_change = 0
    global bulletY_change
    bulletY_change = 12
    bullet_state = "ready"

    global font
    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 10
    textY = 10

    over_font = pygame.font.Font('freesansbold.ttf', 100)
    over2 = pygame.font.Font('freesansbold.ttf', 100)

    def show_score(x, y):
        score = font.render("Fudds Eliminated = " + str(score_value), True, (255, 0, 0))
        screen.blit(score, (x, y))

    def game_over_text(x, y):
        over_text = over_font.render("F1 TO RETRY", True, (255, 0, 0))
        screen.blit(over_text, (x, y))

    def game_over_text2(x, y):
        over_2 = over2.render("C=BATTLECRY", True, (255, 0, 0))
        screen.blit(over_2, (x, y))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 19, y + 15))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + math.pow(enemyY - bulletY, 2))
        if distance < 30:
            return True
        else:
            return False

    if num_of_enemies == 0:
        mixer.music.load('cartoon-birds-2_daniel-simion.wav')
        mixer.music.play(-1)

    running = True

    while running:

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.time.set_timer(running, 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    sup.play()
                if event.key == pygame.K_LEFT:
                    playerX_change = -15
                if event.key == pygame.K_RIGHT:
                    playerX_change = 15
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_Sound.play()
                        bulletX = playerX
                        bulletY -= bulletY_change
                    fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_F1 and num_of_enemies == 0:
                    main()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 0:
            playerX = 920
        elif playerX >= 920:
            playerX = 0

        if num_of_enemies == 0:
            game_over_text(200, 300)
            game_over_text2(180, 400)
            game_over = True

            playerImg = pygame.image.load('imageedit_2_7490140388.png')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        for i in range(num_of_enemies):

            if enemyY[i] >= 550:
                num_of_enemies = 0

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = random.randint(8, 9)
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 960:
                enemyX_change[i] = random.randint(8, 9) * -1
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 600
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 960)
                enemyY[i] = random.randint(0, 50)
                fudd2_Sound = mixer.Sound('bomb.ogg')
                fudd2_Sound.set_volume(.5)
                fudd2_Sound.play()
                if score_value > 250:
                    enemyImg.append(pygame.image.load('imageedit_2_7490140388.png'))

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 600
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        if score_value > 250:
            for i in range(num_of_enemies):
                if enemyX[i] <= 0:
                    enemyX_change[i] = random.randint(9, 11)
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 960:
                    enemyX_change[i] = random.randint(9, 11) * -1
                    enemyY[i] += enemyY_change[i]

        if score_value > 50:
            bulletY_change = 18
        if score_value > 100:
            bulletY_change = 26
        if score_value > 250:
            bulletY_change = 50

        # global fastbulletfont

        if score_value > 50 and score_value <= 52:
            scream = mixer.Sound('2scream.wav')
            scream.set_volume(.05)
            scream.play(1)
            fastbulletfont = pygame.font.Font('freesansbold.ttf', 32)
            fastbullet = fastbulletfont.render("FASTER BULLETS UNLOCKED!", True, (255, 0, 0))
            screen.blit(fastbullet, (300, 400))

        if score_value > 100 and score_value <= 102:
            fastbullet = fastbulletfont.render("FASTER BULLETS UNLOCKED!", True, (255, 0, 0))
            screen.blit(fastbullet, (300, 400))
            sup.play(1)

        if score_value > 250 and score_value <= 252:
            truck = mixer.Sound('fire-truck-air-horn_daniel-simion.wav')
            truck.set_volume(.1)
            truck.play(1)
            fastbulletfont = pygame.font.Font('freesansbold.ttf', 40)
            fastbullet = fastbulletfont.render("       PAIN     TRAIN", True, (255, 0, 0))
            screen.blit(fastbullet, (300, 400))
        if score_value > 250:
            if enemyX[i] <= 0:
                enemyX_change[i] = random.randint(11, 13)
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 960:
                enemyX_change[i] = random.randint(11, 13) * -1
                enemyY[i] += enemyY_change[i]

        if score_value == 400:
            num_of_enemies = 0
            fastbulletfont = pygame.font.Font('freesansbold.ttf', 24)
            fastbullet = fastbulletfont.render("FUDD ARMY DEFEATED! CHUNGRATS!", True, (255, 0, 0))
            screen.blit(fastbullet, (220, 250))

        player(playerX, playerY)
        show_score(textX, textY)

        pygame.display.update()


main()
