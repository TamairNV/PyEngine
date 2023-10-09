import pygame
from typing import TypeVar, Generic


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def multiplyVectors(self, vector3):
        return Vector3(vector3.x * self.x, vector3.y * self.y, vector3.z * self.z)


class Colour:
    def __init__(self, r=0, g=0, b=0, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def multiplyVectors(self, vector3):
        return Vector2(vector3.x * self.x, vector3.y * self.y)


class Transform:
    def __init__(self):
        self.position = Vector2()
        self.rotation = 0
        self.scale = Vector2(0.5, 0.5)



class Time:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.deltaTime = 0

    def tick(self, frameRateCap):
        self.deltaTime = self.clock.tick(frameRateCap) / 1000.0  # Convert milliseconds to seconds


class Screen:

    def __init__(self, height, width, name):
        self.height = height
        self.width = width
        self.name = name
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.events = pygame.event.get()
        Input.startListening()





class GameLoop:

    screen = None
    def __init__(self, frameRateCap=60):
        pygame.init()
        self.frameRateCap = frameRateCap
        self.time = Time()




    def run(self):
        while True:
            self.time.tick(self.frameRateCap)
            GameLoop.screen.events = pygame.event.get()
            Input.keysPressed = pygame.key.get_pressed()




            # Your game logic update function
            self.update()

            # Your rendering function
            self.render()

            Input.keysPressedLastFrame = pygame.key.get_pressed()
            for event in GameLoop.screen.events:
                if event.type == pygame.QUIT:
                    pygame.quit()

    def update(self):
        ActionObj.runUpdates()
        ActionObj.runLateUpdates()
        pass

    def render(self):
        Sprite.runRenderUpdates()
        pygame.display.flip()


class BoxCollider:
    def __init__(self, height, width):
        self.height = height
        self.width = width

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

class Sprite:
    sprites = []

    def __init__(self, img):
        self.imageOriginal = pygame.image.load(img)
        self.rectOriginal = self.imageOriginal.get_rect()
        self.transform = obj.transform
        self.originalSize = Vector2(self.rectOriginal.width, self.rectOriginal.height)
        Sprite.sprites.append(self)
        self.obj = None

    @staticmethod
    def runRenderUpdates():
        for sprite in Sprite.sprites:
            sprite.render()

    def render(self):

        rotatedImage = pygame.transform.rotate(self.imageOriginal, -self.transform.rotation)
        scaledRotatedImage = pygame.transform.scale(rotatedImage,
                                                      (int(self.originalSize.x * self.transform.scale.x),
                                                       int(self.originalSize.y * self.transform.scale.y)))

        rect = scaledRotatedImage.get_rect(center=(self.transform.position.x, self.transform.position.y))

        GameLoop.screen.screen.blit(scaledRotatedImage, rect)


class ActionObj:
    actionObjs = []

    def __init__(self):
        ActionObj.actionObjs.append(self)
        self.transform = Transform()
        self.components = []
        self.awake()
        self.start()

    def addComponent(self, component):
        self.components.append(component)
        component.obj = self

    @staticmethod
    def runUpdates():
        for obj in ActionObj.actionObjs:
            obj.update()

    @staticmethod
    def runLateUpdates():
        for obj in ActionObj.actionObjs:
            obj.lateUpdate()

    def awake(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def lateUpdate(self):
        pass


class Player(ActionObj):

    def __init__(self):
        super().__init__()

        self.health = 100

    def start(self):
        print("start")

    def awake(self):
        print("awake")
    def update(self):
        if Input.getKeyUp("a"):
            print("up")

        if Input.getKeyDown("a"):
            print("DOWN")


if __name__ == "__main__":
    game = GameLoop(frameRateCap=60)
    GameLoop.screen = Screen(800, 600, "test")
    obj = Player()
    obj.addComponent(Sprite("Mario.png"))
    obj.transform.rotation = 90
    obj.transform.position = Vector2(400,300)


    game.run()

