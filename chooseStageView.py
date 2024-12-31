import pygame

from setting import *
from button import Button
from role import Role
from draw_text import draw_text


class ChooseStageView:
    def __init__(self):
        """Background"""
        self.background = pygame.image.load("image/background_chooseStage.jpeg").convert_alpha()
        self.background.set_alpha(180)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.chooseStage = 0  # 選擇的關卡
        self.stage_confirm = False
        self.page = 1  # 當前的頁數
        self.openShop = False
        self.changeWear = False
        self.quit = False

        """選擇關卡按鈕"""
        self.setting = load_settings()
        self.stages = self.setting["stage"]
        self.btn_stages = []
        for i in range(self.stages):
            self.btn_stages.append(Button(SCREEN_WIDTH / 2 - 200, (i % 5 + 1) * 70, 400, 60, f"第 {i + 1} 關", 30))

        self.btn_pageUp = Button(SCREEN_WIDTH / 2 - 200, 430, 100, 60, "上一頁", 30)
        self.btn_pageDown = Button(SCREEN_WIDTH / 2 + 100, 430, 100, 60, "下一頁", 30)

        """更衣按鈕"""
        self.btn_changeWear = Button(20, 320, 150, 60, "更衣", 30)

        """商店按鈕"""
        self.btn_shop = Button(20, 400, 150, 60, "工具商店", 30)

        """離開遊戲按鈕"""
        self.btn_quit = Button(20, 480, 150, 60, "離開遊戲", 30)

        """確認按鈕"""
        self.btn_confirm = Button(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 100, 300, 80, "確認", 30)

        """人物"""
        self.role = Role(675, 50, 300, 450)

    def update(self):

        """取得滑鼠事件"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        """關卡按鈕"""
        for btn in self.btn_stages:
            # 確認按鈕是否在該頁數
            if not self.btn_stages.index(btn) // 5 == self.page - 1:
                continue

            btn.check_hover(mouse_pos)

            if btn.is_clicked(mouse_pos, mouse_pressed):
                self.chooseStage = self.btn_stages.index(btn) + 1

            if self.btn_stages.index(btn) == self.chooseStage - 1:
                btn.is_selected(True)
            else:
                btn.is_selected(False)

        """頁數按鈕"""
        self.btn_pageUp.check_hover(mouse_pos)
        self.btn_pageDown.check_hover(mouse_pos)

        if self.btn_pageUp.is_clicked(mouse_pos, mouse_pressed) and self.page != 1:
            self.page -= 1

        if self.btn_pageDown.is_clicked(mouse_pos, mouse_pressed) and self.page != ((self.stages - 1) // 5) + 1:
            self.page += 1

        """更衣按紐"""
        self.btn_changeWear.check_hover(mouse_pos)

        if self.btn_changeWear.is_clicked(mouse_pos, mouse_pressed) and not self.setting["lockWear"]:
            self.changeWear = True

        """商店按鈕"""
        self.btn_shop.check_hover(mouse_pos)

        if self.btn_shop.is_clicked(mouse_pos, mouse_pressed):
            self.openShop = True

        """離開遊戲按鈕"""
        self.btn_quit.check_hover(mouse_pos)

        if self.btn_quit.is_clicked(mouse_pos, mouse_pressed):
            self.quit = True

        """確認按鈕"""
        self.btn_confirm.check_hover(mouse_pos)

        if self.btn_confirm.is_clicked(mouse_pos, mouse_pressed) and self.chooseStage != 0:
            if os.path.exists(f"stages/stage_{self.chooseStage}.json"):
                self.stage_confirm = True

    def draw(self, surface):
        """背景與標題"""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(WHITE)
        surface.blit(background, (0, 0))
        surface.blit(self.background, (0, 0))
        draw_text(surface, "選擇關卡", 40, (94, 38, 18), SCREEN_WIDTH / 2, 30)

        """關卡按鈕"""
        for btn in self.btn_stages:
            # 確認按鈕是否在該頁數
            if not self.btn_stages.index(btn) // 5 == self.page - 1:
                continue

            btn.draw(surface)

        """頁數"""
        draw_text(surface, f"第 {self.page}/{((self.stages - 1) // 5) + 1} 頁", 30, BLACK, SCREEN_WIDTH / 2, 460)
        self.btn_pageUp.draw(surface)
        self.btn_pageDown.draw(surface)

        """更衣按鈕"""
        self.btn_changeWear.draw(surface)

        """商店按鈕"""
        self.btn_shop.draw(surface)

        """離開遊戲按鈕"""
        self.btn_quit.draw(surface)

        """確認按鈕"""
        self.btn_confirm.draw(surface)

        """繪製人物"""
        self.role.draw(surface)

    def reset(self):
        self.chooseStage = 0  # 選擇的關卡
        self.stage_confirm = False
        self.openShop = False
        self.changeWear = False

        # 選擇關卡按鈕
        self.setting = load_settings()
        self.stages = self.setting["stage"]
        self.btn_stages = []
        for i in range(self.stages):
            self.btn_stages.append(Button(SCREEN_WIDTH / 2 - 200, (i % 5 + 1) * 70, 400, 60, f"第 {i + 1} 關", 30))

        self.role.reset()
