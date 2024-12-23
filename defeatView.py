import pygame

from setting import *
from button import Button
from role import Role
from draw_text import draw_text


class DefeatView:
    def __init__(self, cloth):
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(WHITE)
        self.background.set_alpha(128)

        self.cloth = cloth

        self.btn_continue = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 100, 200, 100, "繼續", 50)
        self.continue_clicked = False

        self.role = Role(675, 50, 300, 450)

    def update(self):
        """取得滑鼠事件"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        """繼續按鈕"""
        self.btn_continue.check_hover(mouse_pos)

        if self.btn_continue.is_clicked(mouse_pos, mouse_pressed):
            self.continue_clicked = True

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        draw_text(surface, "Defeat!", 60, BLACK, SCREEN_WIDTH/2, 50)
        draw_text(surface, "你沒能保護你的衣服", 40, BLACK, SCREEN_WIDTH / 2, 130)
        draw_text(surface, f"你已被迫穿上{self.cloth}", 40, BLACK, SCREEN_WIDTH / 2, 200)
        draw_text(surface, f"你得通過此關卡才可脫下此衣服", 30, (142, 142, 142), SCREEN_WIDTH/2, 280)

        """繼續按鈕"""
        self.btn_continue.draw(surface)

        """繪製角色"""
        self.role.draw(surface)
