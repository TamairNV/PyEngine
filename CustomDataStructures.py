class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Vector3(other * self.x, other * self.y, other * self.z)
        if type(other) == Vector2:
            return Vector3(other.x * self.x, other.y * self.y,  self.z)
        return Vector3(other.x * self.x, other.y * self.y, other.z * self.z)

    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return Vector3(other + self.x, other + self.y, other + self.z)
        if type(other) == Vector2:
            return Vector3(other.x + self.x, other.y + self.y,  self.z)

        return Vector3(other.x + self.x, other.y + self.y, other.z + self.z)

    def __sub__(self, other):
        if type(other) == float or type(other) == int:
            return Vector3(self.x - other, self.y - other, self.z - other)
        if type(other) == Vector2:
            return Vector3(other.x - self.x, other.y - self.y, self.z)
        return Vector3( self.x - other.x,  self.y - other.y, self.z - other.z)

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Vector2(other * self.x, other * self.y)
        if type(other) == Vector3:
            return Vector2(other.x * self.x, other.y * self.y)
        return Vector2(other.x * self.x, other.y * self.y)

    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(other + self.x, other + self.y)

        if type(other) == Vector3:
            return Vector2(other.x + self.x, other.y + self.y)
        return Vector2(other.x + self.x, other.y + self.y)

    def __sub__(self, other):
        return Vector3( self.x - other.x,  self.y - other.y)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

class Colour:
    def __init__(self, r=0, g=0, b=0, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class HashMap:
    def __init__(self):
        pass


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def Add(self,data):
        node = Node()
        node.data = data
        if self.head == None:
            self.head = node
            self.tail = node
            self.length += 1
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
            self.length += 1

    def Remove(self,data):
        if self.head == None:
            return
        if self.head.data == data:
            self.head = self.head.next
            self.length -= 1
            return
        current = self.head
        while current.next != None:
            if current.next.data == data:
                current.next = current.next.next
                self.length -= 1
                return
            current = current.next
    def RemoveAt(self,index):
        if index >= self.length:
            return
        if index == 0:
            self.head = self.head.next
            self.length -= 1
            return
        current = self.head
        for i in range(index):
            current = current.next
        current.next = current.next.next
        self.length -= 1

    def Get(self,index):
        if index >= self.length:
            return
        current = self.head
        for i in range(index):
            current = current.next
        return current.data



class Node:
    def __init__(self):
        self.data = None
        self.next = None
        self.prev = None