import pygame

from setting import *


class Role:
    def __init__(self, x, y, w, h):
        """載入玩家資料"""

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.setting = load_settings()

        self.img_role = pygame.image.load(f"image/role/{self.setting['wear']}.png")
        self.img_role = pygame.transform.scale(self.img_role, (self.w, self.h))

        self.lockWear = self.setting["lockWear"]

    def changeWear(self, cloth):
        if not self.lockWear:
            self.img_role = pygame.image.load(f"image/role/{cloth}.png").convert_alpha()
            self.img_role = pygame.transform.scale(self.img_role, (self.w, self.h))

    def save_wear(self, cloth):
        self.setting = update_settings("wear", cloth)

    def reset(self):
        self.setting = load_settings()
        self.lockWear = self.setting["lockWear"]
        self.img_role = pygame.image.load(f"image/role/{self.setting['wear']}.png")
        self.img_role = pygame.transform.scale(self.img_role, (self.w, self.h))

    def lock(self):
        self.lockWear = True
        self.setting = update_settings("lockWear", self.lockWear)

    def unlock(self):
        self.lockWear = False
        self.setting = update_settings("lockWear", self.lockWear)

    def draw(self, surface):
        surface.blit(self.img_role, (self.x, self.y))
