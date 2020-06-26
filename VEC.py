import math

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.module = math.hypot(x, y)

    def unite(self, module):
        if module != 0 and self.module != 0: 
            return Vec2(module*(self.x/self.module), module*(self.y/self.module))
        return Vec2(0,0)
        
    def __str__(self):
        return "Vec2({}, {})".format(self.x, self.y)