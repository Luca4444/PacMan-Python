import pygame
import numpy as np
import sys, pygame
import random

import math

pygame.init()
pygame.display.set_caption('Luca Snake')
size = width, height = 1000, 800
black = 0, 0, 0

screen = pygame.display.set_mode(size)
red = (255, 0, 0)
green = (244, 173, 167)


def scoreText(score, x, y, txt):
    white = (255, 255, 255)

    font = pygame.font.Font('Minecraft.ttf', 28)
    text = font.render(txt + str(score), True, white)
    textRect = text.get_rect()
    textRect.center = (x, y)
    textRect.left = x
    return [text, textRect]


class Game:
    def __init__(self):

        self.screen = screen
        self.pac = Pac()
        self.ghost1 = Ghost("Red")
        self.ghost2 = Ghost("Orange")
        self.ghost3 = Ghost("Pink")
        self.ghost4 = Ghost("LightBlue")
        self.score = 1
        self.board = Board()
        self.foodRectList = []

        for col in range(1, 24):
            for row in range(1, 19):
                rect = pygame.rect.Rect(((col + 0.5) * 40, (row + 0.5) * 40, 10, 10))
                rect.centerx = (col + 0.5) * 40
                rect.centery = (row + 0.5) * 40
                self.foodRectList.append(rect)

    def main(self):
        clock = pygame.time.Clock()
        frametime = clock.tick()
        self.score = 1

        run = True
        while run == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

            self.drawObjects()
            # if len(self.snake.snakeList[1:]) > 1 and self.snake.snakeList[0][0].collidelist(
            #         list(np.concatenate(self.snake.snakeList[1:]).flat)[::2]) != -1:
            #     run = False
            #     sys.exit()
            #
            # if self.snake.snakeList[0][0].x == -24 or self.snake.snakeList[0][0].x == 1008:
            #     run = False
            #     sys.exit()
            #
            # if self.snake.snakeList[0][0].y == -24 or self.snake.snakeList[0][0].y == 816:
            #     run = False
            #     sys.exit()

            clock.tick(8)

    def drawObjects(self):
        scoreFunc = scoreText(self.score * 100, 20, 20, "")

        self.screen.fill((0, 0, 0))

        for foodRect in self.foodRectList:
            pygame.draw.rect(screen, green, foodRect)

        self.board.setBoard()

        self.ghost1.move(self.board, self.pac, [self.ghost2.ghostRect, self.ghost3.ghostRect, self.ghost4.ghostRect])
        self.ghost2.move(self.board, self.pac, [self.ghost1.ghostRect, self.ghost3.ghostRect, self.ghost4.ghostRect])
        self.ghost3.move(self.board, self.pac, [self.ghost1.ghostRect, self.ghost2.ghostRect, self.ghost4.ghostRect])
        self.ghost4.move(self.board, self.pac, [self.ghost1.ghostRect, self.ghost2.ghostRect, self.ghost3.ghostRect])

        self.pac.move(self.board)

        self.ghost1.drawGhost(self.screen)
        self.ghost2.drawGhost(self.screen)
        self.ghost3.drawGhost(self.screen)
        self.ghost4.drawGhost(self.screen)

        self.pac.drawPac(self.screen)

        # if self.pac.pacRect.collidelist([self.ghost1.ghostRect, self.ghost2.ghostRect, self.ghost3.ghostRect, self.ghost4.ghostRect]) != -1:
        #     self.ghost1.eatMode = 40
        #     self.ghost2.eatMode = 40
        #     self.ghost3.eatMode = 40
        #     self.ghost4.eatMode = 40

        if self.ghost1.eatMode != 0 and self.ghost2.eatMode != 0 and self.ghost3.eatMode != 0 and self.ghost4.eatMode != 0:
            collision = self.pac.pacRect.collidelist([self.ghost1.ghostRect, self.ghost2.ghostRect, self.ghost3.ghostRect, self.ghost4.ghostRect])
            if collision !=1:
                [self.ghost1, self.ghost2, self.ghost3, self.ghost4][collision].eaten = True


        if self.pac.pacRect.collidelist(self.board.eatBallRects) != -1:
            self.board.eatBallRects.pop(self.pac.pacRect.collidelist(self.board.eatBallRects))
            self.ghost1.eatMode = 40
            self.ghost2.eatMode = 40
            self.ghost3.eatMode = 40
            self.ghost4.eatMode = 40

        if self.pac.pacRect.collidelist(self.foodRectList) != -1:
            self.score += 1
            self.foodRectList.pop(self.pac.pacRect.collidelist(self.foodRectList))

        self.screen.blit(scoreFunc[0], scoreFunc[1])
        pygame.display.update()


class Pac:
    def __init__(self):
        self.speed = 20
        self.moveDir = [self.speed, 0]
        self.pacRect = pygame.rect.Rect((10 * 40, 13 * 40, 40, 40))
        self.canMove = 1
        self.spriteSheet = pygame.image.load('pacManNew.png').convert_alpha()
        rect = pygame.Rect((0, 0, 40, 40))
        self.pacOpenImage = pygame.Surface(rect.size).convert_alpha()
        self.pacOpenImage.blit(self.spriteSheet, (0, 0), rect)
        rect = pygame.Rect((0, 40, 40, 40))
        self.pacClosedImage = pygame.Surface(rect.size).convert_alpha()
        self.pacClosedImage.blit(self.spriteSheet, (0, 0), rect)
        self.image = self.pacClosedImage
        self.checkDoor = 0

    def move(self, board):

        if self.checkDoor > 0:
            self.checkDoor -= 1

        self.canMove = self.canMove * -1

        if self.canMove == -1:
            self.image = self.pacOpenImage
        else:
            self.image = self.pacClosedImage

        keys = pygame.key.get_pressed()

        allowMove = [True, True, True, True]

        rectUp = pygame.rect.Rect((self.pacRect.x, self.pacRect.y - self.speed, 40, 40))
        rectDown = pygame.rect.Rect((self.pacRect.x, self.pacRect.y + self.speed, 40, 40))
        rectLeft = pygame.rect.Rect((self.pacRect.x - self.speed, self.pacRect.y, 40, 40))
        rectRight = pygame.rect.Rect((self.pacRect.x + self.speed, self.pacRect.y, 40, 40))

        if rectUp.collidelist(board.piecesRect) != -1:
            allowMove[2] = False

        if rectDown.collidelist(board.piecesRect) != -1:
            allowMove[3] = False

        if rectLeft.collidelist(board.piecesRect) != -1:
            allowMove[0] = False

        if rectRight.collidelist(board.piecesRect) != -1:
            allowMove[1] = False

        if keys[pygame.K_LEFT] and allowMove[0] and self.canMove == 1:  # Check boundaries
            self.moveDir = [-self.speed, 0]

        if keys[pygame.K_RIGHT] and allowMove[1] and self.canMove == 1:
            self.moveDir = [self.speed, 0]

        if keys[pygame.K_UP] and allowMove[2] and self.canMove == 1:
            self.moveDir = [0, -self.speed]

        if keys[pygame.K_DOWN] and allowMove[3] and self.canMove == 1:
            self.moveDir = [0, self.speed]

        if self.moveDir == [-self.speed, 0] and allowMove[0]:
            self.pacRect.move_ip(self.moveDir)

        if self.moveDir == [self.speed, 0] and allowMove[1]:
            self.pacRect.move_ip(self.moveDir)

        if self.moveDir == [0, -self.speed] and allowMove[2]:
            self.pacRect.move_ip(self.moveDir)

        if self.moveDir == [0, self.speed] and allowMove[3]:
            self.pacRect.move_ip(self.moveDir)

        for doors in board.doorsRectList:
            if self.pacRect.colliderect(doors[0]) and self.checkDoor == 0:
                self.pacRect.x = doors[1].x
                self.pacRect.y = doors[1].y
                self.checkDoor = 2
            elif self.pacRect.colliderect(doors[1]) and self.checkDoor == 0:
                self.pacRect.x = doors[0].x
                self.pacRect.y = doors[0].y
                self.checkDoor = 2

    def drawPac(self, screen):
        if self.moveDir == [-self.speed, 0]:
            self.image = pygame.transform.rotate(self.image, 180)

        if self.moveDir == [0, -self.speed]:
            self.image = pygame.transform.rotate(self.image, 90)

        if self.moveDir == [0, self.speed]:
            self.image = pygame.transform.rotate(self.image, 270)

        screen.blit(self.image, self.pacRect)


class Board:
    def __init__(self):
        self.sheetPos = [[0, 0], [10, 0], [0, 10], [10, 10]]
        self.boardList = []

        self.spriteSheet = pygame.image.load('pacBlueMap.png').convert_alpha()
        self.eatBallSpriteSheet = pygame.image.load('eatBall.png').convert_alpha()
        self.piecesRect = []
        self.piecesImages = []
        self.pieceTypes = []
        self.pieceTypesList = []
        self.doorsRectList = []
        self.eatBallPositions = []
        self.eatBallRects = []

        self.upDownPath = None
        self.leftRigthPath = None
        self.upFinalPath = None
        self.downFinalPath = None
        self.leftFinalPath = None
        self.rigthFinalPath = None
        self.downRightTurnPath = None
        self.downLeftTurnPath = None
        self.upLeftTurnPath = None
        self.upRightTurnPath = None
        self.ballPath = None

        self.setPieces()
        self.eatBallTimer = 4

    def setBoard(self):
        self.eatBallTimer -= 1
        if self.eatBallTimer == 0:
            self.eatBallTimer += 4

        self.boardList = np.array([
            [[1, 2], [1, 3], [1, 7], [1, 8], [1, 9], [1, 10], [1, 11], [1, 12], [1, 13], [1, 14],
             [1, 15], [1, 16], [1, 17],
             [3, 6], [3, 7], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14],
             [3, 15],
             [5, 8], [5, 9], [5, 15],
             [7, 6], [7, 7], [7, 8], [7, 9], [7, 13],
             [9, 9], [9, 10], [9, 11],
             [14, 15],
             [16, 9], [16, 10], [16, 11], [16, 15],
             [18, 4], [18, 5], [18, 6],
             [19, 10], [19, 11], [19, 12], [19, 13],
             [21, 4], [21, 5], [21, 6], [21, 10], [21, 14], [21, 15],
             [23, 2], [23, 3], [23, 4], [23, 8], [23, 9], [23, 10], [23, 11], [23, 12],
             [23, 13], [23, 14], [23, 15], [23, 16], [23, 17]
             ],
            [[2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1],
             [14, 1],
             [18, 1], [19, 1], [20, 1], [21, 1], [22, 1],
             [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [12, 3], [13, 3], [14, 3], [15, 3],
             [6, 5], [12, 5], [13, 5], [14, 5], [15, 5],
             [10, 8], [15, 8],
             [6, 12], [10, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12],
             [8, 14], [9, 14], [10, 14], [11, 14],
             [8, 16], [9, 16], [10, 16], [11, 16], [19, 16], [20, 16],
             [2, 18], [3, 18], [7, 18], [8, 18], [9, 18], [10, 18], [11, 18], [12, 18], [13, 18],
             [14, 18], [15, 18], [16, 18], [17, 18], [18, 18], [19, 18], [20, 18], [21, 18], [22, 18]
             ],
            [[1, 6], [3, 5], [5, 7], [5, 14], [9, 5], [14, 14], [16, 14], [18, 3], [19, 9], [21, 9], [21, 13],
             [23, 7]],
            [[1, 4], [3, 16], [5, 10], [5, 16], [7, 10], [9, 6], [11, 6], [14, 16], [16, 16], [18, 7], [21, 11],
             [23, 5]],
            [[3, 3], [5, 5], [11, 3], [17, 1], [20, 3], [14, 8], [20, 7], [5, 12],
             [18, 14], [7, 16], [18, 16], [6, 18]
             ],
            [[15, 1], [9, 3], [16, 3], [16, 5], [12, 14], [12, 16], [4, 18], [11, 8]],
            [[1, 1], [11, 5], [9, 8]],
            [[23, 1], [21, 3], [7, 5], [16, 8], [7, 12], ],
            [[21, 7], [16, 12], [19, 14], [21, 16], [23, 18]],
            [[9, 12], [7, 14], [1, 18]],
            [],
        ])



        rotate = [0, 90, 0, 180, 90, 270, 0, 270, 180, 90, 0]

        for index, row in enumerate(self.boardList):
            self.boardList[index] = np.array(row) * 40

        typesList = ["upDownPath",
                     "leftRigthPath",
                     "upFinalPath",
                     "downFinalPath",
                     "leftFinalPath",
                     "rigthFinalPath",
                     "downRightTurnPath",
                     "downLeftTurnPath",
                     "upLeftTurnPath",
                     "upRightTurnPath",
                     "ballPath"]

        for index, positions in enumerate(self.boardList):
            for pos in positions:
                rect = pygame.rect.Rect((pos[0], pos[1], 40, 40))
                self.piecesRect.append(rect)
                self.pieceTypesList.append(typesList[index])
                screen.blit(
                    pygame.transform.rotate(
                        pygame.transform.scale(
                            self.pieceTypes[index], (40, 40)), rotate[index])
                    , rect)

        for rect in self.eatBallRects:
            if self.eatBallTimer > 2:
                screen.blit(pygame.transform.scale(self.eatBallSpriteSheet, (40, 40)), rect)
            elif self.eatBallTimer <= 2:
                screen.blit(pygame.transform.scale(pygame.surface.Surface((40,40)), (40, 40)), rect)


        door1Rect = pygame.rect.Rect((5 * 40, 19 * 40, 40, 40))
        door2Rect = pygame.rect.Rect((16 * 40, 0 * 40, 40, 40))
        door3Rect = pygame.rect.Rect((0 * 40, 5 * 40, 40, 40))
        door4Rect = pygame.rect.Rect((24 * 40, 6 * 40, 40, 40))
        self.doorsRectList = [[door1Rect, door2Rect], [door3Rect, door4Rect]]

    def setPieces(self):
        rect = pygame.Rect((self.sheetPos[0][0], self.sheetPos[0][1], 10, 10))
        self.upDownPath = pygame.Surface(rect.size).convert_alpha()
        self.upDownPath.blit(self.spriteSheet, (0, 0), rect)

        self.leftRigthPath = pygame.transform.rotate(self.upDownPath, 90)
        self.leftRigthPath.blit(self.spriteSheet, (0, 0), rect)

        rect = pygame.Rect((self.sheetPos[1][0], self.sheetPos[1][1], 10, 10))
        self.upFinalPath = pygame.Surface(rect.size).convert_alpha()
        self.upFinalPath.blit(self.spriteSheet, (0, 0), rect)

        self.downFinalPath = pygame.transform.rotate(self.upFinalPath, 180)
        self.downFinalPath.blit(self.spriteSheet, (0, 0), rect)

        self.leftFinalPath = pygame.transform.rotate(self.upFinalPath, 270)
        self.leftFinalPath.blit(self.spriteSheet, (0, 0), rect)

        self.rigthFinalPath = pygame.transform.rotate(self.upFinalPath, 90)
        self.rigthFinalPath.blit(self.spriteSheet, (0, 0), rect)

        rect = pygame.Rect((self.sheetPos[2][0], self.sheetPos[2][1], 10, 10))
        self.downRightTurnPath = pygame.Surface(rect.size).convert_alpha()
        self.downRightTurnPath.blit(self.spriteSheet, (0, 0), rect)

        self.downLeftTurnPath = pygame.transform.rotate(self.downRightTurnPath, 90)
        self.downLeftTurnPath.blit(self.spriteSheet, (0, 0), rect)

        self.upLeftTurnPath = pygame.transform.rotate(self.downRightTurnPath, 180)
        self.upLeftTurnPath.blit(self.spriteSheet, (0, 0), rect)

        self.upRightTurnPath = pygame.transform.rotate(self.downRightTurnPath, 270)
        self.upRightTurnPath.blit(self.spriteSheet, (0, 0), rect)

        rect = pygame.Rect((self.sheetPos[3][0], self.sheetPos[3][1], 10, 10))
        self.ballPath = pygame.Surface(rect.size).convert_alpha()
        self.ballPath.blit(self.spriteSheet, (0, 0), rect)

        self.pieceTypes = [
            self.upDownPath,
            self.leftRigthPath,
            self.upFinalPath,
            self.downFinalPath,
            self.leftFinalPath,
            self.rigthFinalPath,
            self.downRightTurnPath,
            self.downLeftTurnPath,
            self.upLeftTurnPath,
            self.upRightTurnPath,
            self.ballPath
        ]

        self.eatBallPositions = [
            [2 * 40, 2 * 40],
            [6 * 40, 11 * 40],
            [4 * 40, 17 * 40],
            [15 * 40, 4 * 40],
            [15 * 40, 15 * 40],
            [20 * 40, 5 * 40],
            [22 * 40, 17 * 40]
        ]

        for eatBallPos in self.eatBallPositions:
            rect = pygame.rect.Rect((eatBallPos[0], eatBallPos[1], 40, 40))
            self.eatBallRects.append(rect)


class Ghost:
    def __init__(self, color):
        self.speed = 20
        self.moveDir = [self.speed, 0]
        x = 10
        y = 10
        if color == 'LightBlue':
            x = 10
            y = 9
        elif color == 'Red':
            x = 15
            y = 9
        elif color == 'Orange':
            x = 10
            y = 11
        elif color == 'Pink':
            x = 15
            y = 11

        self.ghostRect = pygame.rect.Rect((x * 40, y * 40, 40, 40))
        self.canMove = 1
        self.img = 'ghostBody' + color + '.png'
        self.spriteSheet = pygame.image.load(self.img).convert_alpha()
        rect = pygame.Rect((0, 0, 40, 40))
        self.ghost1Image = pygame.Surface(rect.size).convert_alpha()
        self.ghost1Image.blit(self.spriteSheet, (0, 0), rect)
        rect = pygame.Rect((0, 40, 40, 40))
        self.ghost2Image = pygame.Surface(rect.size).convert_alpha()
        self.ghost2Image.blit(self.spriteSheet, (0, 0), rect)
        rect = pygame.Rect((40, 0, 40, 40))
        self.ghost3Image = pygame.Surface(rect.size).convert_alpha()
        self.ghost3Image.blit(self.spriteSheet, (0, 0), rect)
        self.image = self.ghost3Image
        self.checkDoor = 0
        self.changeDircTimer = 0
        self.imageCounter = 2
        self.ghostEyesSpriteSheet = pygame.image.load('ghostEyes.png').convert_alpha()
        self.ghostEyesEatSpriteSheet = pygame.image.load('ghostEyesEat.png').convert_alpha()
        self.eatMode = 0
        self.eatModeFinalTime = 12
        self.eaten = False

    def move(self, board, pac, ghostRects):

        if self.eatMode > self.eatModeFinalTime:
            self.eatMode -= 1
            self.spriteSheet = pygame.image.load('ghostBodyBlue.png').convert_alpha()
        elif 0 != self.eatMode <= self.eatModeFinalTime:
            self.eatMode -= 1
            if self.eatMode % 2 == 0:
                self.spriteSheet = pygame.image.load('ghostBodyWhite.png').convert_alpha()
            else:
                self.spriteSheet = pygame.image.load('ghostBodyBlue.png').convert_alpha()
        else:
            self.spriteSheet = pygame.image.load(self.img).convert_alpha()

        rect = pygame.Rect((0, 0, 40, 40))
        self.ghost1Image = pygame.Surface(rect.size).convert_alpha()
        self.ghost1Image.blit(self.spriteSheet, (0, 0), rect)
        rect = pygame.Rect((0, 40, 40, 40))
        self.ghost2Image = pygame.Surface(rect.size).convert_alpha()
        self.ghost2Image.blit(self.spriteSheet, (0, 0), rect)
        rect = pygame.Rect((40, 0, 40, 40))
        self.ghost3Image = pygame.Surface(rect.size).convert_alpha()
        self.ghost3Image.blit(self.spriteSheet, (0, 0), rect)

        if self.changeDircTimer > 0:
            self.changeDircTimer -= 1

        self.canMove = self.canMove * -1

        if self.imageCounter == 2:
            self.image = self.ghost1Image

        elif self.imageCounter == 1:
            self.image = self.ghost2Image
        else:
            self.image = self.ghost3Image
            self.imageCounter = 3

        self.imageCounter -= 1

        keys = pygame.key.get_pressed()

        allowMove = [True, True, True, True]

        rectUp = pygame.rect.Rect((self.ghostRect.x, self.ghostRect.y - self.speed, 40, 40))
        rectDown = pygame.rect.Rect((self.ghostRect.x, self.ghostRect.y + self.speed, 40, 40))
        rectLeft = pygame.rect.Rect((self.ghostRect.x - self.speed, self.ghostRect.y, 40, 40))
        rectRight = pygame.rect.Rect((self.ghostRect.x + self.speed, self.ghostRect.y, 40, 40))

        if rectUp.collidelist(board.piecesRect + ghostRects) != -1:
            allowMove[2] = False

        if rectDown.collidelist(board.piecesRect + ghostRects) != -1:
            allowMove[3] = False

        if rectLeft.collidelist(board.piecesRect + ghostRects) != -1:
            allowMove[0] = False

        if rectRight.collidelist(board.piecesRect + ghostRects) != -1:
            allowMove[1] = False

        if math.sqrt((pac.pacRect.x - self.ghostRect.x) ** 2 + (
                pac.pacRect.y - self.ghostRect.y) ** 2) > 200 and self.changeDircTimer == 0 and self.eaten == False:
            options = [[-self.speed, 0], [self.speed, 0], [0, -self.speed], [0, self.speed]]

            self.changeDircTimer = 5
            allowMoveCopy = allowMove.copy()

            for index, allow in enumerate(allowMoveCopy):
                if allow is False:
                    allowMoveCopy.pop(index)
                    options.pop(index)

            self.moveDir = random.choice(options)
        elif self.changeDircTimer == 0:
            if self.eatMode is 0:
                if pac.pacRect.x < self.ghostRect.x and allowMove[0] and self.canMove == 1:
                    self.moveDir = [-self.speed, 0]

                if pac.pacRect.x > self.ghostRect.x and allowMove[1] and self.canMove == 1:
                    self.moveDir = [self.speed, 0]

                if pac.pacRect.y < self.ghostRect.y and allowMove[2] and self.canMove == 1:
                    self.moveDir = [0, -self.speed]

                if pac.pacRect.y > self.ghostRect.y and allowMove[3] and self.canMove == 1:
                    self.moveDir = [0, self.speed]
            elif self.eaten is True:
                if pac.pacRect.x < 11*40 and allowMove[0] and self.canMove == 1:
                    self.moveDir = [-self.speed, 0]

                if pac.pacRect.x > 11*40 and allowMove[1] and self.canMove == 1:
                    self.moveDir = [self.speed, 0]

                if pac.pacRect.y < 9*40 and allowMove[2] and self.canMove == 1:
                    self.moveDir = [0, -self.speed]

                if pac.pacRect.y > 9*40 and allowMove[3] and self.canMove == 1:
                    self.moveDir = [0, self.speed]
            else:
                if pac.pacRect.x > self.ghostRect.x and allowMove[0] and self.canMove == 1:
                    self.moveDir = [-self.speed, 0]

                if pac.pacRect.x < self.ghostRect.x and allowMove[1] and self.canMove == 1:
                    self.moveDir = [self.speed, 0]

                if pac.pacRect.y > self.ghostRect.y and allowMove[2] and self.canMove == 1:
                    self.moveDir = [0, -self.speed]

                if pac.pacRect.y < self.ghostRect.y and allowMove[3] and self.canMove == 1:
                    self.moveDir = [0, self.speed]

        if self.moveDir == [-self.speed, 0] and allowMove[0]:
            self.ghostRect.move_ip(self.moveDir)

        if self.moveDir == [self.speed, 0] and allowMove[1]:
            self.ghostRect.move_ip(self.moveDir)

        if self.moveDir == [0, -self.speed] and allowMove[2]:
            self.ghostRect.move_ip(self.moveDir)

        if self.moveDir == [0, self.speed] and allowMove[3]:
            self.ghostRect.move_ip(self.moveDir)

        for doors in board.doorsRectList:
            if self.ghostRect.colliderect(doors[0]) and self.checkDoor == 0:
                self.ghostRect.x = doors[1].x
                self.ghostRect.y = doors[1].y
                self.checkDoor = 2
            elif self.ghostRect.colliderect(doors[1]) and self.checkDoor == 0:
                self.ghostRect.x = doors[0].x
                self.ghostRect.y = doors[0].y
                self.checkDoor = 2

    def drawGhost(self, screen):
        if self.eatMode > self.eatModeFinalTime:
            rect = pygame.Rect((0, 0, 40, 40))
            self.image.blit(self.ghostEyesEatSpriteSheet, (0, 0), rect)
        elif 0 != self.eatMode <= self.eatModeFinalTime:
            if self.eatMode % 2 == 0:
                rect = pygame.Rect((0, 40, 40, 40))
                self.image.blit(self.ghostEyesEatSpriteSheet, (0, 0), rect)
            else:
                rect = pygame.Rect((0, 0, 40, 40))
                self.image.blit(self.ghostEyesEatSpriteSheet, (0, 0), rect)
        else:
            if self.moveDir == [-self.speed, 0]:
                rect = pygame.Rect((0, 40, 40, 40))
                self.image.blit(self.ghostEyesSpriteSheet, (0, 0), rect)

            if self.moveDir == [self.speed, 0]:
                rect = pygame.Rect((40, 0, 40, 40))
                self.image.blit(self.ghostEyesSpriteSheet, (0, 0), rect)

            if self.moveDir == [0, -self.speed]:
                rect = pygame.Rect((40, 40, 40, 40))
                self.image.blit(self.ghostEyesSpriteSheet, (0, 0), rect)

            if self.moveDir == [0, self.speed]:
                rect = pygame.Rect((0, 0, 40, 40))
                self.image.blit(self.ghostEyesSpriteSheet, (0, 0), rect)

        screen.blit(self.image, self.ghostRect)


game1 = Game()

game1.main()
