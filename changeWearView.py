import pygame

from setting import *

from button import Button
from role import Role


class ChangeWearView:
    def __init__(self):
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(WHITE)

        self.setting = load_settings()
        self.clothes = self.setting["clothes"]
        self.current_wear = self.setting["wear"]

        self.role = Role(SCREEN_WIDTH//2-160, 50, 320, 480)
        self.page = 1
        self.back = False

        """選擇衣服按鈕"""
        self.btn_clothes = []
        for i in range(len(self.clothes)):
            self.btn_clothes.append(Button(SCREEN_WIDTH - 220, 100 + (i % 5) * 70, 200, 60, f"{self.clothes[i]}", 30))

        """保存按鈕"""
        self.btn_save = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80, 100, 60, "保存", 30)

        """切頁按鈕"""
        self.btn_pageUp = Button(SCREEN_WIDTH - 240, 400, 100, 60, "上一頁", 30)
        self.btn_pageDown = Button(SCREEN_WIDTH - 120, 400, 100, 60, "下一頁", 30)

        """返回按鈕"""
        self.btn_back = Button(SCREEN_WIDTH - 120, 20, 100, 60, "返回", 30)

    def reset(self):
        self.setting = load_settings()
        self.clothes = self.setting["clothes"]
        self.current_wear = self.setting["wear"]

        """選擇衣服按鈕"""
        self.btn_clothes = []
        for i in range(len(self.clothes)):
            self.btn_clothes.append(Button(SCREEN_WIDTH - 220, 100 + (i % 5) * 70, 200, 60, f"{self.clothes[i]}", 30))

        self.page = 1
        self.back = False

    def update(self):
        """取得滑鼠事件"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        """選擇衣服按鈕"""
        for btn in self.btn_clothes:
            # 確認按鈕是否在該頁數
            if not self.btn_clothes.index(btn) // 5 == self.page - 1:
                continue

            btn.check_hover(mouse_pos)

            if btn.is_clicked(mouse_pos, mouse_pressed):
                self.current_wear = btn.text

            if self.current_wear == btn.text:
                btn.is_selected(True)
            else:
                btn.is_selected(False)

        self.role.changeWear(self.current_wear)

        """保存按鈕"""
        self.btn_save.check_hover(mouse_pos)

        if self.btn_save.is_clicked(mouse_pos, mouse_pressed):
            self.role.save_wear(self.current_wear)
            self.back = True

        """切頁按鈕"""
        self.btn_pageUp.check_hover(mouse_pos)
        self.btn_pageDown.check_hover(mouse_pos)

        if self.btn_pageUp.is_clicked(mouse_pos, mouse_pressed) and self.page != 1:
            self.page -= 1

        if self.btn_pageDown.is_clicked(mouse_pos, mouse_pressed) and self.page != ((len(self.btn_clothes) - 1) // 5) + 1:
            self.page += 1

        """返回按鈕"""
        self.btn_back.check_hover(mouse_pos)

        if self.btn_back.is_clicked(mouse_pos, mouse_pressed):
            self.back = True

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        self.role.draw(surface)

        """按鈕"""
        for btn in self.btn_clothes:
            # 確認按鈕是否在該頁數
            if not self.btn_clothes.index(btn) // 5 == self.page - 1:
                continue

            btn.draw(surface)

        self.btn_save.draw(surface)
        self.btn_pageUp.draw(surface)
        self.btn_pageDown.draw(surface)
        self.btn_back.draw(surface)
