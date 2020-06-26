import math
import time
import win32api
import win32con
from GDI import GDIDraw
from VEC import Vec2


def predict(delta_t):
    x0, y0 = win32api.GetCursorPos()
    time.sleep(0.1)
    x1, y1 = win32api.GetCursorPos()
    dx, dy = x1 - x0, y1 - y0
    speed = math.hypot(dx, dy) / 0.1
    vec0 = Vec2(dx, dy)
    vec1 = vec0.unite(speed*delta_t)
    return int(x1+vec1.x), int(y1+vec1.y)


if __name__ == "__main__":

    draw = GDIDraw()

    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        position = predict(0.2)
        draw.line(win32api.GetCursorPos(), position, 2, (0,255,0))
        draw.circle(position, 15, 1, (255, 0, 0))
        




