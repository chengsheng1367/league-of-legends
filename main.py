import cv2
import time
import math
import win32api
import win32gui
import win32con
import numpy as np
from PIL import ImageGrab, Image
from pynput.mouse import Controller
from GDI import GDIDraw
from VEC import Vec2

mouse = Controller()

def nothing(x):
    pass

def pil_2_cv(pil_img):
    img = np.array(pil_img)
    img = img[:,:,::-1].copy()
    return img

def get_screen():
    pil_img = ImageGrab.grab().convert('RGB')
    return pil_2_cv(pil_img)

def find_elements_on_screen(screen, lower, upper):
    kernel0 = np.ones((7,7), np.uint8)
    kernel1 = np.ones((20,20), np.uint8)
    mask = cv2.inRange(screen, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel0)
    mask = cv2.dilate(mask, kernel1, iterations = 1)
    ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = ret[0] if len(ret) == 2 else ret[1]
    return contours    

def find_local_player(screen):
    player = None
    lower = np.array([35, 25, 0])
    upper = np.array([49, 35, 4])
    life = np.array([41, 146, 66])
    contours = find_elements_on_screen(screen, lower, upper)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if 8 <= approx.size <= 12:
            x, y, w, h = cv2.boundingRect(approx)
            _x, _y = (
                x + w,
                y + h
            )
            if np.array_equal(screen[_y-22][_x-2], life):
                player = (_x + 38, _y + 79)
                break
    return player

def find_enemies(screen):
    enemies = []
    lower = np.array([0, 2, 47])
    upper = np.array([0, 11, 97])
    contours = find_elements_on_screen(screen, lower, upper)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if 8 <= approx.size <= 12:
            x, y, w, h = cv2.boundingRect(approx)
            _x, _y = (
                x + w + 49,
                y + h + 57
            )
            enemies.append((_x,_y))
    return enemies

def calculate_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x1-x2, y1-y2)

def lock_enemy(enemies):
    min_dist = 999
    min_enemy = None
    for enemy in enemies:
        dist = calculate_distance(mouse.position, enemy)
        if dist < min_dist:
            min_dist = dist
            min_enemy = enemy
    if not min_enemy is None:
        mouse.position = min_enemy

def create_player_range(player, r_alpha, r_beta):
    x,y = player
    focus_distance = math.sqrt(r_alpha**2 - r_beta**2)
    f1 = (x + focus_distance, y)
    f2 = (x - focus_distance, y)
    return r_alpha, f1, f2

def check_range(r_alpha, f1, f2, point):
    d1 = calculate_distance(point, f1)
    d2 = calculate_distance(point, f2)
    if d1 + d2 <= r_alpha*2:
        return True
    return False

def predict_player(img, delta_t):
    player0 = find_local_player(img)
    time.sleep(0.1)
    player1 = find_local_player(img)
    dx, dy = x1 - x0, y1 - y0
    speed = math.hypot(dx, dy) / 0.1
    vec0 = Vec2(dx, dy)
    vec1 = vec0.unite(speed*delta_t)
    return int(x1+vec1.x), int(y1+vec1.y)

def hitbox(player, screen, t1, t2):
    
    
    
    

    return


if __name__ == "__main__":

    cv2.namedWindow("track")
    cv2.createTrackbar("th1", "track", 0, 300, nothing)
    cv2.createTrackbar("th2", "track", 0, 300, nothing)

    img = cv2.imread("teste.png")
    
    while True:
        player = find_local_player(img)

        t1 = cv2.getTrackbarPos("th1", "track")
        t2 = cv2.getTrackbarPos("th2", "track")

        if not player is None:
            x,y = player
        
            H, W = 50, 50

            img = img[y - H: y + H, x - W: x + W]
        
            img_blur = cv2.GaussianBlur(img, (7, 7), 1)
            img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

        #img = hitbox(player, img, t1, t2)

        cv2.imshow("wnd", img_gray)

        cv2.waitKey(1)


    
