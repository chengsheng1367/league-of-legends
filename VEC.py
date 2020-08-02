import math


class Vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = math.hypot(x, y)

    @property
    def values(self):
        return self.x, self.y

    @property
    def unite(self):
        if self.h == 0:
            return Vec2(0, 0)
        return Vec2(
            self.x/self.h,
            self.y/self.h
        )

    def dot(self, n):
        return Vec2(self.x*n, self.y*n)

    def __add__(self, v):
        return Vec2(self.x+v.x, self.y+v.y)

    def __sub__(self, v):
        return Vec2(self.x-v.x, self.y-v.y)

    def __mul__(self, v):
        return Vec2(self.x*v.x, self.y*v.y)

    def __str__(self):
        return '[{0}->{1}]'.format(self.x, self.y)
