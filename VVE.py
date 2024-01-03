import pygame
from typing import TypeVar, Generic
import random
import copy


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        return Vector3(other.x * self.x, other.y * self.y, other.z * self.z)

    def __add__(self, other):
        return Vector3(other.x + self.x, other.y + self.y, other.z + self.z)

    def __sub__(self, other):
        return Vector3( self.x - other.x,  self.y - other.y, self.z - other.z)

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return Vector2(other.x * self.x, other.y * self.y)

    def __add__(self, other):
        return Vector2(other.x + self.x, other.y + self.y)

    def __sub__(self, other):
        return Vector2( self.x - other.x,  self.y - other.y)

    def __str__(self):
        # Define the string representation of the object
        return f" {self.x} {self.y}"


class Colour:
    def __init__(self, r=0, g=0, b=0, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a



class Transform:
    def __init__(self):
        self.position = Vector2()
        self.rotation = 0
        self.scale = Vector2(0.5, 0.5)
        self.velocity = Vector2()



class Time:

    clock = pygame.time.Clock()
    deltaTime = 0

    @staticmethod
    def tick(frameRateCap):
        Time.deltaTime = Time.clock.tick(frameRateCap) / 1000.0  # Convert milliseconds to seconds


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





    def run(self):
        p = False
        tickIndex = 0
        while True:
            Time.tick(self.frameRateCap)
            GameLoop.screen.events = pygame.event.get()
            Input.keysPressed = pygame.key.get_pressed()
            if Input.getKeyDown("a"):
                p = True
            self.render()
            # Your game logic update function
            if p:
                self.physics()

            self.update()
            GameLoop.screen.screen.fill((0, 0, 0))
            # Your rendering function



            tickIndex +=1
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

    def physics(self):
        Collider.runUpdates()
        Collider.runLateUpdates()




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
    numOfSprites = 0
    def __init__(self, img):
        self.name = Sprite.numOfSprites
        Sprite.numOfSprites += 1
        self.imageOriginal = pygame.image.load(img)
        self.rectOriginal = self.imageOriginal.get_rect()
        self.rect = self.rectOriginal
        self.originalSize = Vector2(self.rectOriginal.width, self.rectOriginal.height)
        Sprite.sprites.append(self)
        self.obj = None
        self.transform = None
        self.layer = 0


    @staticmethod
    def runRenderUpdates():
        Sprite.sprites.sort( key=lambda a:a.layer)
        for sprite in Sprite.sprites:

            sprite.render()

    def render(self):

        rotatedImage = pygame.transform.rotate(self.imageOriginal, -self.transform.rotation)
        scaledRotatedImage = pygame.transform.scale(rotatedImage,
                                                      (int(self.originalSize.x * self.transform.scale.x),
                                                       int(self.originalSize.y * self.transform.scale.y)))

        rect = scaledRotatedImage.get_rect(center=(self.transform.position.x, self.transform.position.y))
        self.rect = rect


        GameLoop.screen.screen.blit(scaledRotatedImage, rect)
class Collider():
    colliders = []
    def __init__(self,layer = 0):
        Collider.colliders.append(self)
        self.obj = None
        self.transform = None
        self.rect = None
        self.obj = None
        self.collidingLayer = layer
        self.isTrigger = False
        self.colliders = []
        self.prevColliders = []
        self.prevTransform = copy.copy(self.transform)

    @staticmethod
    def runUpdates():
        for collider in Collider.colliders:
            collider.update()
    @staticmethod
    def runLateUpdates():
        for collider in Collider.colliders:
            collider.lateUpdate()


    def update(self):
        self.rect = self.obj.getComponent(Sprite).rect
        self.prevColliders = self.colliders
        self.isColliding()

    def lateUpdate(self):
        obj.lateTransform = copy.copy(obj.transform.position)

    def isColliding(self):
        self.colliders = []
        for collider in Collider.colliders:
            collider.rect = collider.obj.getComponent(Sprite).rect
            if collider != self and self.collidingLayer == collider.collidingLayer and self.rect.colliderect(collider.rect):
                obj.colliderStay()
                self.colliders.append(collider)
                self.resolveCollision(collider)


        for collider in Collider.colliders:
            if collider not in self.colliders and collider in self.prevColliders:
                obj.colliderExit()
            if collider  in self.colliders and collider not in self.prevColliders:
                obj.colliderEnter()
        self.prevTransform = copy.copy(self.transform)

    def resolveCollision(self, other_collider):
        # Get the rect attributes of the colliders
        other_rect = self.obj.getComponent(Sprite).rect
        self_rect = other_collider.obj.getComponent(Sprite).rect

        # Check for collision
        if other_rect.colliderect(self_rect):
            overlap_x = other_rect.width / 2 + self_rect.width / 2 - abs(
                other_collider.transform.position.x - self.transform.position.x)
            overlap_y = other_rect.height / 2 + self_rect.height / 2 - abs(
                other_collider.transform.position.y - self.transform.position.y)

            sign_x = 1 if other_collider.transform.position.x < self.transform.position.x else -1
            sign_y = 1 if other_collider.transform.position.y < self.transform.position.y else -1

            # Resolve collision based on the direction of overlap
            if overlap_x < overlap_y:
                other_collider.transform.position.x -= sign_x * overlap_x
            else:
                other_collider.transform.position.y -= sign_y * overlap_y


class ActionObj:
    actionObjs = []

    def __init__(self):
        ActionObj.actionObjs.append(self)
        self.transform = Transform()
        self.components = []
        self.awake()
        self.start()
        self.tag = "default"

        self.lateTransform = copy.copy(self.transform.position)

    def addComponent(self, component):
        self.components.append(component)
        component.obj = self
        component.transform =  self.transform

    def getComponent(self,component):
        for item in self.components:
            if type(item) == component:
                return item

    @staticmethod
    def runUpdates():
        for obj in ActionObj.actionObjs:
            obj.update()


    @staticmethod
    def runLateUpdates():
        for obj in ActionObj.actionObjs:
            obj.lateUpdate()
            obj.transform.velocity = obj.transform.position - obj.lateTransform


    def awake(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def lateUpdate(self):
        pass

    def colliderEnter(self):
        print("enter")

    def colliderExit(self):
        print("exit")

    def colliderStay(self):
       print("stay")



class Player(ActionObj):

    def __init__(self):
        super().__init__()

        self.health = 100

    def start(self):
        print("start")

    def awake(self):
        print("awake")
    def update(self):
        if Input.isKeyPressed("w"):
            self.transform.position.y -= 500 *Time.deltaTime
        if Input.isKeyPressed("a"):
            self.transform.position.x -= 500 * Time.deltaTime
            pass
        if Input.isKeyPressed("s"):
            self.transform.position.y += 500 * Time.deltaTime
            pass
        if Input.isKeyPressed("d"):
            self.transform.position.x += 500 * Time.deltaTime
            pass




if __name__ == "__main__":
    game = GameLoop(frameRateCap=30)
    GameLoop.screen = Screen(800, 600, "test")

    obj2 = ActionObj()
    obj2.addComponent(Sprite("Mario.png"))
    obj2.addComponent(Collider())
    obj2.transform.scale = Vector2(0.1, 0.1)
    obj2.transform.position = Vector2(400,300)
    obj2.getComponent(Sprite).layer = 10
    obj2.transform.rotation = 45

    obj = Player()
    obj.addComponent(Sprite("Mario.png"))
    obj.addComponent(Collider())
    obj.transform.position = Vector2(0,0)
    obj.transform.scale = Vector2(0.1,0.1)
    obj.getComponent(Sprite).layer = 4

    game.run()






