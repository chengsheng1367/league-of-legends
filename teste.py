import math
import time
import win32api
import win32con
from GDI import GDIDraw
from VEC import Vec2


def predict(delta_t):
    v0 = Vec2(*win32api.GetCursorPos())
    time.sleep(.1)
    v1 = Vec2(*win32api.GetCursorPos())
    v2 = v1 - v0
    v3 = v2.unite.dot((v2.h / .1)*delta_t)
    pred = v1 + v3
    return int(pred.x), int(pred.y)


if __name__ == "__main__":

    draw = GDIDraw()

    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        position = predict(0.21)
        draw.line(win32api.GetCursorPos(), position, 2, (0,255,0))
        draw.circle(position, 15, 1, (255, 0, 0))
        




