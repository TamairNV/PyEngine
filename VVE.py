import pygame
from typing import TypeVar, Generic
import CustomDataStructures as dataS

class Transform:
    camera = None
    def __init__(self):
        self.position = dataS.Vector2()
        self.rotation = 0
        self.scale = dataS.Vector2(0.5, 0.5)


    def update(self):
        pass
class Rigidbody:
    def __init__(self):
        self.velocity = dataS.Vector2()
        self.gravity = dataS.Vector2(0, 980*2)
        self.mass = 1
        self.drag = 0.1
        self.collider = None
        self.useGravity = False
        self.transform = None
        self.obj = None
        self.maxSpeed = dataS.Vector2(1000,1000)
        self.deceleration = 5

    def addForce(self, force):
        self.velocity += force / self.mass

    def update(self):

        if self.collider == None:
            self.collider = self.obj.getComponent(Collider)
        self.velocity -= self.velocity * self.drag * Time.deltaTime
        if self.useGravity:
            self.velocity += self.gravity * Time.deltaTime
        self.velocity.x = max(min(self.velocity.x, self.maxSpeed.x), -self.maxSpeed.x)
        self.velocity.y = max(min(self.velocity.y, self.maxSpeed.y), -self.maxSpeed.y)
        self.velocity.x -= self.velocity.x * self.deceleration * Time.deltaTime
        self.velocity.y -= self.velocity.y * self.deceleration * Time.deltaTime
        self.transform.position += self.velocity * Time.deltaTime
        if self.collider != None:
            self.collider.rect.x = self.transform.position.x
            self.collider.rect.y = self.transform.position.y
            self.collider.rect.width = self.obj.getComponent(Sprite).originalSize.x * self.transform.scale.x
            self.collider.rect.height = self.obj.getComponent(Sprite).originalSize.y * self.transform.scale.y
            self.collider.checkForCollisionsAndMoveBack()


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
        Transform.camera = self
        self.events = pygame.event.get()
        Input.startListening()
        self.position = dataS.Vector2(0, 0)







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
        self.originalSize = dataS.Vector2(self.rectOriginal.width, self.rectOriginal.height)
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

        rect = scaledRotatedImage.get_rect(center=(self.transform.position.x,self.transform.position.y))

        rect.x -= GameLoop.screen.position.x
        rect.y -= GameLoop.screen.position.y
        GameLoop.screen.screen.blit(scaledRotatedImage, rect)

class Collider():
    dictColliders = {}
    def __init__(self,rect):
        self.obj = None
        self.transform = None
        self.rect = rect
        Collider.dictColliders[self] = self.rect

    def checkForCollisions(self):
        for key in Collider.dictColliders:
            if key != self:
                if self.rect.colliderect(key.rect):
                    return True
        return False

    def checkForCollisionsAndMoveBack(self):
        for key in Collider.dictColliders:
            if key != self:
                if self.rect.colliderect(key.rect):
                    self.transform.position = self.transform.position - self.obj.getComponent(Rigidbody).velocity * Time.deltaTime
                    return True
        return False


class ActionObj:
    actionObjs = []

    def __init__(self):
        ActionObj.actionObjs.append(self)
        self.transform = Transform()
        self.components = []
        self.awake()
        self.start()
        self.tag = "default"

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
            obj.transform.update()
            for com in obj.components:
                if type(com) == Rigidbody:
                    com.update()
                    if com.collider != None:
                        if com.collider.checkForCollisionsAndMoveBack():
                            com.velocity = dataS.Vector2(0,0)
                else:
                    try:

                        com.update()
                    except:
                        pass

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
    def update(self): # add movement use the rigidbody and the input class with wasd
        if Input.isKeyPressed("w"):
            self.getComponent(Rigidbody).addForce(dataS.Vector2(0,-100))
        if Input.isKeyPressed("s"):
            self.getComponent(Rigidbody).addForce(dataS.Vector2(0,100))
        if Input.isKeyPressed("a"):
            self.getComponent(Rigidbody).addForce(dataS.Vector2(-100,0))
        if Input.isKeyPressed("d"):
            self.getComponent(Rigidbody).addForce(dataS.Vector2(100,0))
        if Input.getKeyDown("space"):
            self.getComponent(Rigidbody).addForce(dataS.Vector2(0,-1000))
        if Input.getKeyDown("escape"):
            self.getComponent(Rigidbody).useGravity = True
        pos = (self.transform.position - GameLoop.screen.position)
        GameLoop.screen.position += dataS.Vector2(pos.x,pos.y) - dataS.Vector2(GameLoop.screen.width/2,GameLoop.screen.height/2)

if __name__ == "__main__":
    game = GameLoop(frameRateCap=60)
    GameLoop.screen = Screen(800, 600, "test")

    obj2 = ActionObj()
    obj2.addComponent(Sprite("Mario.png"))
    #obj2.addComponent(Collider(obj2.getComponent(Sprite).rectOriginal))
    #obj2.addComponent(Rigidbody())
    obj2.transform.scale = dataS.Vector2(10, 10)
    obj2.transform.position = dataS.Vector2(400,300)
    obj2.getComponent(Sprite).layer = 1
    #obj2.getComponent(Rigidbody).drag = 10

    obj = Player()
    obj.addComponent(Sprite("Mario.png"))
    obj.addComponent(Collider(obj.getComponent(Sprite).rectOriginal))
    obj.addComponent(Rigidbody())
    obj.transform.position = dataS.Vector2(400,100)
    obj.transform.scale = dataS.Vector2(0.1,0.1)
    obj.getComponent(Sprite).layer = 4




    game.run()

