import pygame
import os

from setting import *
from draw_text import draw_text

from button import Button


class ShopView:
    def __init__(self):
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(WHITE)

        self.setting = load_settings()

        self.tools = [f.replace(".json", "") for f in os.listdir("tools") if f.replace(".json", "") not in self.setting["tools"]]


    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

