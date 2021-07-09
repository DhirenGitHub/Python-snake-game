import pygame
import random
import sys

screenSize = 500

pygame.init()

screen = pygame.display.set_mode((screenSize, screenSize))
clock = pygame.time.Clock()


while True:
    beanPos = []
    playerTailPos = []

    score = 0

    text = pygame.font.Font(None, 35)

    while True:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            break

        introText = text.render("Press the space bar", 1, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(introText, (screenSize / 2 - 120, screenSize / 2))
        pygame.display.update()
        pygame.display.flip()


    def beanPositions():
        for i in range(20):
            for q in range(20):
                beanPos.append([[i * 25], [q * 25]])


    class tail(pygame.sprite.Sprite):
        def __init__(self, number):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((25, 25))
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect()
            self.posNumber = number
            self.rect.center = playerTailPos[len(playerTailPos) - self.posNumber - 2]
        
        def update(self):
            self.rect.center = playerTailPos[len(playerTailPos) - self.posNumber - 2]

    class player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((25, 25))
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = screenSize / 2
            self.rect.y = screenSize / 2
            self.direction = "right"
            self.side = "side"
            self.vel = 25
            self.delayMovement = 30

        def update(self):

            if self.rect.x <= -self.rect.width:
                self.rect.x = screenSize + self.rect.width

            elif self.rect.x >= screenSize + self.rect.width:
                self.rect.x = -self.rect.width
        
            if self.rect.y <= -self.rect.height:
                self.rect.y = screenSize + self.rect.height

            elif self.rect.y >= screenSize + self.rect.height:
                self.rect.y = -self.rect.height

            key = pygame.key.get_pressed()

            if self.side == "side":
                if key[pygame.K_UP]:
                    self.direction = "up"
                if key[pygame.K_DOWN]:
                    self.direction = "down"
            else:
                if key[pygame.K_LEFT]:
                    self.direction = "left"
                if key[pygame.K_RIGHT]:
                    self.direction = "right"

            if self.delayMovement == 0:
                if self.direction == "left":
                    self.rect.x -= self.vel
                    playerTailPos.append(self.rect.center)
                    self.side = "side"

                elif self.direction == "right":
                    self.rect.x += self.vel
                    playerTailPos.append(self.rect.center)
                    self.side = "side"

                elif self.direction == "up":
                    self.rect.y -= self.vel
                    playerTailPos.append(self.rect.center)
                    self.side = "straight"

                elif self.direction == "down":
                    self.rect.y += self.vel
                    playerTailPos.append(self.rect.center)
                    self.side = "straight"

                self.delayMovement = 30

            else:
                self.delayMovement -= 1


    class bean(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((25, 25))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.pos = random.choice(beanPos)
            self.rect.y = self.pos[1][0]
            self.rect.x = self.pos[0][0]
        
        def update(self):
            global score

            for i in range(score):
                if self.rect.center == playerTailPos[len(playerTailPos) - i - 2]:
                    self.pos = random.choice(beanPos)
                    self.rect.y = self.pos[1][0]
                    self.rect.x = self.pos[0][0] 


    beanPositions()
    food = bean()
    gamePlayer = player()

    all_sprites = pygame.sprite.Group()
    foods = pygame.sprite.Group()
    tailGroup = pygame.sprite.Group()

    foods.add(food)
    all_sprites.add(gamePlayer, food)

    run = True
    while run:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        hit = pygame.sprite.spritecollide(gamePlayer, foods, False)
        gameover = pygame.sprite.spritecollide(gamePlayer, tailGroup, False)

        if gameover:
            print("You ate yourself!")
            run = False

        if hit:
            food.kill()
            food = bean()
            score += 1

            chain = tail(score - 1)
            
            all_sprites.add(food)
            all_sprites.add(chain)
            tailGroup.add(chain)
            foods.add(food)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()

        scoreText = text.render(str(score), 1, (255, 255, 255))
        screen.blit(scoreText, (screenSize / 2 - 12.5, 2))

        pygame.display.update()
        pygame.display.flip()
