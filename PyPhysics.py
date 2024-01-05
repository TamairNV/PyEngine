import CustomDataStructures as dataS
import Game
import PyEngine
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
            self.obj.getComponent(PyEngine.Sprite).rectOriginal = self.collider.rect
        self.velocity -= self.velocity * self.drag * Game.Time.deltaTime
        if self.useGravity:
            self.velocity += self.gravity * Game.Time.deltaTime
        self.velocity.x = max(min(self.velocity.x, self.maxSpeed.x), -self.maxSpeed.x)
        self.velocity.y = max(min(self.velocity.y, self.maxSpeed.y), -self.maxSpeed.y)
        self.velocity.x -= self.velocity.x * self.deceleration * Game.Time.deltaTime
        self.velocity.y -= self.velocity.y * self.deceleration * Game.Time.deltaTime
        self.transform.position += self.velocity * Game.Time.deltaTime
        if self.collider != None:
            self.collider.rect.x = self.transform.position.x
            self.collider.rect.y = self.transform.position.y
            #self.collider.rect.width = self.obj.getComponent(PyEngine.Sprite).originalSize.x * self.transform.scale.x
            #self.collider.rect.height = self.obj.getComponent(PyEngine.Sprite).originalSize.y * self.transform.scale.y
            self.collider.checkForCollisionsAndMoveBack()
class Collider():
    dictColliders = {}
    def __init__(self,rect):
        self.obj = None
        self.transform = None
        self.rect = rect
        Collider.dictColliders[self] = self.rect

    def update(self):
        self.rect.x = self.transform.position.x
        self.rect.y = self.transform.position.y
        self.rect.width = self.obj.getComponent(PyEngine.Sprite).originalSize.x * self.transform.scale.x
        self.rect.height = self.obj.getComponent(PyEngine.Sprite).originalSize.y * self.transform.scale.y
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
                    self.transform.position = self.transform.position - self.obj.getComponent(Rigidbody).velocity * Game.Time.deltaTime
                    return True
        return False