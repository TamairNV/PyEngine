import pygame

import PyEngine
from PyEngine import *





class Bird(PyEngine.ActionObj):
    def __init__(self):
        super().__init__()
        self.addComponent(Sprite("bird.png"))
        self.addComponent(Physics.Rigidbody())
        self.addComponent(Physics.Collider(pygame.Rect(0, 0, 100, 100)))
        self.transform.scale = dataS.Vector2(0.1, 0.1)


    def update(self):
        if Game.Input.getKeyDown("escape"):
            self.getComponent(Physics.Rigidbody).useGravity = True
        if Game.Input.getKeyDown("space"):
            self.getComponent(Physics.Rigidbody).addForce(dataS.Vector2(0, -1000))


        #Game.GameLoop.screen.position += dataS.Vector2(70,0) * Game.Time.deltaTime

class Pipe(PyEngine.ActionObj):

    def __init__(self):
        super().__init__()
        self.addComponent(Sprite("pipe.png"))
        self.transform.scale = dataS.Vector2(0.3, 0.2)
        self.transform.rotation = 180

    def update(self):

        self.transform.position += dataS.Vector2(-100,0) * Game.Time.deltaTime
        if self.transform.position.x < -100:
            self.transform.position = dataS.Vector2(800, 0)

if __name__ == "__main__":
    game = Game.GameLoop(frameRateCap=60)
    Game.GameLoop.screen = Game.Screen(800, 600, "test")


    bird = Bird()
    bird.addComponent(Sprite("bird.png"))
    bird.transform.position = dataS.Vector2(200, 300)


    floor = ActionObj()
    floor.addComponent(Sprite("floor-sprite.png"))
    floor.addComponent(Physics.Collider(pygame.Rect(0, 0, 800, 100)))
    floor.transform.position = dataS.Vector2(0, 800)
    floor.transform.scale = dataS.Vector2(5, 0.9)
    floor.addComponent(Physics.Rigidbody())

    roof = ActionObj()
    roof.addComponent(Sprite("floor-sprite.png"))
    roof.addComponent(Physics.Collider(pygame.Rect(0, 0, 800, 100)))
    roof.transform.position = dataS.Vector2(0, -200)
    roof.transform.scale = dataS.Vector2(5, 0.9)
    roof.addComponent(Physics.Rigidbody())

    p = Pipe()

    game.run()