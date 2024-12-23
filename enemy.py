import math
import pygame

from setting import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, path):
        super().__init__()

        """載入衣服圖片"""
        self.image = pygame.image.load(f"{IMG_CLOTHES}/{name}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

        """載入衣服資料"""
        if os.path.exists(f"clothes/{name}.json"):
            with open(f"clothes/{name}.json", "r") as file:
                self.cloth = json.load(file)

        self.name = name
        self.life = self.cloth["health"]
        self.health = self.cloth["health"]
        self.speed = self.cloth["speed"]
        self.drop = self.cloth["drop"]

        self.path = path
        self.current_point = 0
        self.rect.center = (self.path[self.current_point][0]*64, self.path[self.current_point][1]*32)

    def update(self):
        if self.current_point < len(self.path) - 1:
            # 移動到下一個點
            target_x = self.path[self.current_point + 1][0] * 64 + 32
            target_y = self.path[self.current_point + 1][1] * 32 + 16
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < self.speed:
                self.current_point += 1
            else:
                self.rect.centerx += self.speed * dx / distance
                self.rect.centery += self.speed * dy / distance
        else:
            self.rect.centerx += self.speed
