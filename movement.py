import time
import random
import win32api
import win32con
from GDI import GDIDraw
from VEC import Vec2

draw = GDIDraw()

#random.seed(91822371239719283731237)

w = win32api.GetSystemMetrics(0)
h = win32api.GetSystemMetrics(1)

x0 = random.randint(0, w)
y0 = random.randint(0, h)

print("Point ->", x0,y0)

directions = [(1,0), (-1,0), (0,-1), (0, 1), (1,1), (1,-1), (-1,1), (-1,-1)]

distance = 10

def predict(x0, y0, x1, y1, delta_t):
    vec0 = Vec2(x1 - x0, y1 - y0)
    vec1 = vec0.unite((distance/0.1)*delta_t)
    return int(x1+vec1.x), int(y1+vec1.y)

def change_direction():
    return random.choice(directions)

def move(x, y, dx, dy):
    return x + dx*distance, y + dy*distance

dx, dy = change_direction()

while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
    if random.randint(0, 10) > 8:
        dx, dy = change_direction()

    draw.circle((x0,y0), 3, 2, (0,255,0))
    
    time.sleep(0.1)

    x1, y1 = move(x0,y0, dx, dy)

    p = predict(x0, y0, x1, y1, 0.3)

    draw.circle(p, 3, 2, (255,0,0))

    x0, y0 = x1, y1

    

