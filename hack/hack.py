import cv2
import time
import math
import threading
import numpy as np
from PIL import ImageGrab
from pynput.mouse import Controller


class ScreenCapture(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.screen = None
        self.on = True

    def run(self):
        while self.on:
            pil_img = ImageGrab.grab().convert('RGB')
            img = np.array(pil_img)
            self.screen = img[:,:,::-1].copy()

    def terminate(self):
        self.on = False


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
            return Vec2(0,0)
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



class LeagueOfLegends(object):
    def __init__(self):
        self.mouse = Controller()

        self.__kernel0 = np.ones((7,7), np.uint8)
        self.__kernel1 = np.ones((20,20), np.uint8)

        self.__enemy_color_id = {
            'lower': np.array([0, 2, 47]),
            'upper': np.array([0, 11, 97])
        }
        self.__player_color_id = {
            'lower': np.array([35, 25, 0]),
            'upper': np.array([49, 35, 4]),
            'life': np.array([41, 146, 66])
        }

        self.__screencap = ScreenCapture()
        self.__screencap.setDaemon(True)
        self.__screencap.start()
        
    def find_closest_enemy(self):
        min_dist = math.inf
        min_enemy = None
        for enemy in self.enemies_entities:
            dist = math.dist(mouse.position, enemy)
            if dist < min_dist:
                min_dist = dist
                min_enemy = enemy
        return min_enemy

    def __find_elements_on_screen(self, lower, upper):
        mask = cv2.inRange(self.__screencap.screen, lower, upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel0)
        mask = cv2.dilate(mask, self.kernel1, iterations = 1)
        ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = ret[0] if len(ret) == 2 else ret[1]
        return contours
    
    
    def __find_entities(self, entity_color_id):
        entities = []
        mask = cv2.inRange(
            self.__screencap.screen,
            entity_color_id['lower'], 
            entity_color_id['upper']
        )
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel0)
        mask = cv2.dilate(mask, self.kernel1, iterations=1)
        ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        possible_entities = ret[0] if len(ret) == 2 else ret[1]
        for i, ent in enumerate(possible_entities):
            approx = cv2.approxPolyDP(ent, 0.01*cv2.arcLength(ent, True), True)
            if 8 <= approx.size <= 12:
                x, y, w, h = cv2.boundingRect(approx)
                entities.append((x + w, y + h))
        return entities



    @property
    def enemies_entities(self):
        enemies = []
        # the contours maybe the possible enemies
        contours = self.__find_elements_on_screen(
            self.__enemy_color_id['lower'],
            self.__enemy_color_id['upper']
        )
        for i, cnt in enumerate(contours):
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if 8 <= approx.size <= 12:
                x, y, w, h = cv2.boundingRect(approx)
                _x, _y = (
                    x + w + 49,
                    y + h + 57
                )
                enemies.append((_x,_y))
        return enemies

    @property
    def local_player(self):
        player = None
        contours = self.__find_elements_on_screen(
            self.__player_color_id['lower'],
            self.__player_color_id['upper']
        )
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if 8 <= approx.size <= 12:
                x, y, w, h = cv2.boundingRect(approx)
                _x, _y = (
                    x + w,
                    y + h
                )
                if np.array_equal(self.__screencap.screen[_y-22][_x-2], self.__player_color_id['life']):
                    player = (_x + 38, _y + 79)
                    break
        return player
    
    def movement_predict(self, delta):
        v1 = Vec2(*self.find_closest_enemy())
        time.sleep(.1)
        v2 = Vec2(*self.find_closest_enemy())
        v3 = v2 - v1
        pred = v2 + v3.unite.dot((v3.h / .1)*delta)
        return pred.values
                



if __name__ == "__main__":
    lol = LeagueOfLegends()
    while True:
        print(lol.local_player)
    
