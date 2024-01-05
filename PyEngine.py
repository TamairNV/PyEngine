import pygame
from typing import TypeVar, Generic
import CustomDataStructures as dataS
import PyPhysics as Physics
import Game




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
        rectOriginal = self.imageOriginal.get_rect()
        originalSize = dataS.Vector2(rectOriginal.width, rectOriginal.height)
        rotatedImage = pygame.transform.rotate(self.imageOriginal, -self.transform.rotation)
        scaledRotatedImage = pygame.transform.scale(rotatedImage,
                                                      (int(originalSize.x * self.transform.scale.x),
                                                       int(originalSize.y * self.transform.scale.y)))

        rect = scaledRotatedImage.get_rect(center=(self.transform.position.x,self.transform.position.y))

        rect.x -= Game.GameLoop.screen.position.x
        rect.y -= Game.GameLoop.screen.position.y
        Game.GameLoop.screen.screen.blit(scaledRotatedImage, rect)
class ActionObj:
    actionObjs = []

    def __init__(self):
        ActionObj.actionObjs.append(self)
        self.transform = dataS.Transform()
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
                if type(com) == Physics.Rigidbody:
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
        if Game.Input.isKeyPressed("w"):
            self.getComponent(Physics.Rigidbody).addForce(dataS.Vector2(0, -100))
        if Game.Input.isKeyPressed("s"):
            self.getComponent(Physics.Rigidbody).addForce(dataS.Vector2(0, 100))
        if Game.Input.isKeyPressed("a"):
            self.getComponent(Physics.Rigidbody).addForce(dataS.Vector2(-100, 0))
        if Game.Input.isKeyPressed("d"):
            self.getComponent(Physics.Rigidbody).addForce(dataS.Vector2(100, 0))
        if Game.Input.getKeyDown("space"):
            self.getComponent(Physics.Rigidbody).addForce(dataS.Vector2(0, -1000))
        if Game.Input.getKeyDown("escape"):
            self.getComponent(Physics.Rigidbody).useGravity = False

        Game.GameLoop.screen.setPosition(self.transform.position)

if __name__ == "__main__":
    game = Game.GameLoop(frameRateCap=60)
    Game.GameLoop.screen = Game.Screen(800, 600, "test")

    obj2 = ActionObj()
    obj2.addComponent(Sprite("Mario.png"))
    obj2.addComponent(Physics.Collider(obj2.getComponent(Sprite).rectOriginal))
    obj2.addComponent(Physics.Rigidbody())
    obj2.transform.scale = dataS.Vector2(0.1, 0.1)
    obj2.transform.position = dataS.Vector2(400,300)
    obj2.getComponent(Sprite).layer = 1
    obj2.getComponent(Physics.Rigidbody).drag = 10

    obj = Player()
    obj.addComponent(Sprite("Mario.png"))
    obj.addComponent(Physics.Collider(obj.getComponent(Sprite).rectOriginal))
    obj.addComponent(Physics.Rigidbody())
    obj.transform.position = dataS.Vector2(400,100)
    obj.transform.scale = dataS.Vector2(0.1,0.1)
    obj.getComponent(Sprite).layer = 4




    game.run()
