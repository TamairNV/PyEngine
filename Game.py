
import pygame
import CustomDataStructures as dataS
import PyEngine
import Time
class Screen:

    def __init__(self, height, width, name):

        self.height = height
        self.width = width
        self.name = name
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        dataS.Transform.camera = self
        self.events = pygame.event.get()
        PyEngine.Input.startListening()
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
            Time.Time.tick(self.frameRateCap)
            GameLoop.screen.events = pygame.event.get()
            Time.Input.keysPressed = pygame.key.get_pressed()

            # Your game logic update function
            self.update()
            GameLoop.screen.screen.fill((0,0,0))
            # Your rendering function
            self.render()

            Time.Input.keysPressedLastFrame = pygame.key.get_pressed()
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