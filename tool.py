import math
import pygame

from setting import *


class Tool(pygame.sprite.Sprite):
    def __init__(self, center, name):
        super().__init__()

        """載入道具圖片"""
        self.image = pygame.image.load(f"{IMG_TOOLS}/{name}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = center

        """載入道具資料"""
        if os.path.exists(f"tools/{name}.json"):
            with open(f"tools/{name}.json", "r") as file:
                self.tool = json.load(file)

        self.sound = pygame.mixer.Sound(f"sound/{name}.mp3")

        self.name = name
        self.cost = self.tool["cost"]
        self.damage = self.tool["damage"]
        self.cooldown = self.tool["cooldown"]
        self.radius = self.tool["radius"]
        self.AOE = self.tool["AOE"]
        self.atk_time = 0

    def update(self, enemies):
        now = pygame.time.get_ticks()

        if now - self.atk_time >= self.cooldown:
            sound_atk = False
            for enemy in enemies:
                distance = math.sqrt(
                    (enemy.rect.centerx - self.rect.centerx) ** 2 +
                    (enemy.rect.centery - self.rect.centery) ** 2
                )
                if distance <= self.radius:
                    enemy.health -= self.damage

                    sound_atk = True
                    self.atk_time = pygame.time.get_ticks()

                    if not self.AOE:
                        break

            if sound_atk:
                self.sound.play()
