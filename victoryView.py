import pygame

from setting import *
from button import Button
from role import Role
from draw_text import draw_text


class VictoryView:
    def __init__(self):
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(WHITE)
        self.background.set_alpha(128)

        self.unlock_cloth = []
        self.firstWin = False
        self.setting = load_settings()

        self.btn_continue = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 100, 200, 100, "繼續", 50)
        self.continue_clicked = False

        self.role = Role(675, 50, 300, 450)

    def unlockClothes(self, clothes):
        self.firstWin = True
        self.setting = load_settings()
        print(str(self.setting))

        for cloth in clothes:
            if cloth not in self.setting["clothes"]:
                self.unlock_cloth.append(cloth)
                self.setting["clothes"].append(cloth)
                self.setting = update_settings(self.setting, "clothes", self.setting["clothes"])

    def reset(self):
        self.role.reset()

        self.setting = load_settings()
        self.continue_clicked = False
        self.unlock_cloth = []

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
        draw_text(surface, "Victory!", 60, BLACK, SCREEN_WIDTH/2, 50)
        draw_text(surface, "恭喜你", 40, BLACK, SCREEN_WIDTH / 2, 130)
        draw_text(surface, "成功捍衛住你的穿衣自由", 40, BLACK, SCREEN_WIDTH / 2, 200)

        """解鎖衣服"""
        if self.firstWin:
            for cloth in self.unlock_cloth:
                draw_text(surface, f"你已解鎖  {cloth}", 30, (142, 142, 142), SCREEN_WIDTH/2, 280 + 40 * self.unlock_cloth.index(cloth))

        """繼續按鈕"""
        self.btn_continue.draw(surface)

        """繪製角色"""
        self.role.draw(surface)
