
import pygame
import CustomDataStructures as dataS
import PyEngine
import Game

class Screen:

    def __init__(self, height, width, name):

        self.height = height
        self.width = width
        self.name = name
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        dataS.Transform.camera = self
        self.events = pygame.event.get()
        Game.Input.startListening()
        self.position = dataS.Vector2(0, 0)

    def getPosition(self):
        return self.position - dataS.Vector2(GameLoop.screen.width / 2, GameLoop.screen.height / 2)

    def setPosition(self, position):
        self.position = position - dataS.Vector2(GameLoop.screen.width / 2, GameLoop.screen.height / 2)
class GameLoop:

    screen = None
    def __init__(self, frameRateCap=60):
        pygame.init()
        self.frameRateCap = frameRateCap







    def run(self):
        while True:
            Time.tick(self.frameRateCap)
            GameLoop.screen.events = pygame.event.get()
            Input.keysPressed = pygame.key.get_pressed()

            # Your game logic update function
            self.update()
            GameLoop.screen.screen.fill((0,0,0))
            # Your rendering function
            self.render()

            Input.keysPressedLastFrame = pygame.key.get_pressed()
            for event in GameLoop.screen.events:
                if event.type == pygame.QUIT:
                    pygame.quit()

    def update(self):
        PyEngine.ActionObj.runUpdates()
        PyEngine.ActionObj.runLateUpdates()

        pass

    def render(self):
        PyEngine.Sprite.runRenderUpdates()
        pygame.display.flip()
class Time:

    clock = pygame.time.Clock()
    deltaTime = 0

    @staticmethod
    def tick(frameRateCap):
        Time.deltaTime = Time.clock.tick(frameRateCap) / 1000.0  # Convert milliseconds to seconds
class Input:


    keys = {}
    numberOfKeys = 0
    keysPressed = []
    keysPressedLastFrame = []

    @staticmethod
    def startListening():
        Input.numberOfKeys = len(pygame.key.get_pressed())
        Input.keysPressed = pygame.key.get_pressed()
        Input.keysPressedLastFrame = pygame.key.get_pressed()
        for key in range(Input.numberOfKeys - 1):
            Input.keys[pygame.key.name(key)] = key

    @staticmethod
    def isKeyPressed(key,pressed = None):
        if pressed == None:
            return pygame.key.get_pressed()[Input.keys[key]]
        return pressed[Input.keys[key]]

    @staticmethod
    def getKeyDown(key):
        for event in GameLoop.screen.events:
            if event.type == pygame.KEYDOWN and Input.isKeyPressed(key):
                return True
        return False

    @staticmethod
    def getKeyUp(key):
        for event in GameLoop.screen.events:
            if event.type == pygame.KEYUP and Input.isKeyPressed(key,Input.keysPressedLastFrame):
                return True
        return False