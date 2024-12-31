import json

import pygame
import os

from setting import *
from draw_text import draw_text

from button import Button
from btn_shopTool import Btn_shopTools


class ShopView:
    def __init__(self):
        """Background"""
        self.background = pygame.image.load("image/background_shop.jpeg").convert_alpha()
        self.background.set_alpha(180)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.setting = load_settings()

        """初始化工具列表"""
        self.tools = []
        for f in os.listdir("tools"):
            if f.replace(".json", "") not in self.setting["tools"]:
                with open(f"tools/{f}", "r") as file:
                    self.tools.append(json.load(file))

        self.btn_tools = []
        for i in range(len(self.tools)):
            self.btn_tools.append(Btn_shopTools(100 + (i % 4) * 210, 200, self.tools[i]["name"], self.tools[i]["price"]))

        """當前狀態"""
        self.page = 1
        self.chooseTool = None
        self.price = 0
        self.back = False

        self.img_coin = pygame.image.load(f"image/coin.png")
        self.img_coin = pygame.transform.scale(self.img_coin, (50, 50))

        """購買按鈕"""
        self.btn_purchase = Button(SCREEN_WIDTH//2-50, SCREEN_HEIGHT-80, 100, 60, "購買", 30)
        self.sound_purchase = pygame.mixer.Sound("sound/purchase.mp3")

        """切頁按鈕"""
        self.btn_pageUp = Button(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT-80, 100, 60, "上一頁", 30)
        self.btn_pageDown = Button(SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT-80, 100, 60, "下一頁", 30)

        """返回按鈕"""
        self.btn_back = Button(SCREEN_WIDTH-120, 20, 100, 60, "返回", 30)

    def reset(self):
        self.setting = load_settings()

        """初始化工具列表"""
        self.tools = []
        for f in os.listdir("tools"):
            if f.replace(".json", "") not in self.setting["tools"]:
                with open(f"tools/{f}", "r") as file:
                    self.tools.append(json.load(file))

        self.btn_tools = []
        for i in range(len(self.tools)):
            self.btn_tools.append(Btn_shopTools(((i % 4) * 210) + 10, 200, self.tools[i]["name"], self.tools[i]["price"]))

        self.chooseTool = None
        self.price = 0
        self.back = False

    def update(self):
        """取得滑鼠事件"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        """商品按鈕"""
        for btn in self.btn_tools:
            # 確認按鈕是否在該頁數
            if not self.btn_tools.index(btn) // 4 == self.page - 1:
                continue

            btn.check_hover(mouse_pos)

            if btn.is_clicked(mouse_pos, mouse_pressed):
                self.chooseTool = btn.tool
                self.price = btn.price

            if btn.tool == self.chooseTool:
                btn.is_selected(True)
            else:
                btn.is_selected(False)

        """購買按鈕"""
        self.btn_purchase.check_hover(mouse_pos)

        if self.btn_purchase.is_clicked(mouse_pos, mouse_pressed):
            if self.setting["money"] >= self.price and self.chooseTool:
                self.setting["tools"].append(self.chooseTool)
                self.setting = update_settings("tools", self.setting["tools"])

                self.setting["money"] -= self.price
                self.setting = update_settings("money", self.setting["money"])

                self.sound_purchase.play()

                for btn in self.btn_tools:
                    if btn.tool == self.chooseTool:
                        self.btn_tools.remove(btn)
                        break

                self.reset()

        """切頁按鈕"""
        self.btn_pageUp.check_hover(mouse_pos)
        self.btn_pageDown.check_hover(mouse_pos)

        if self.btn_pageUp.is_clicked(mouse_pos, mouse_pressed) and self.page != 1:
            self.page -= 1

        if self.btn_pageDown.is_clicked(mouse_pos, mouse_pressed) and self.page != ((len(self.btn_tools) - 1) // 4) + 1:
            self.page += 1

        """返回按鈕"""
        self.btn_back.check_hover(mouse_pos)

        if self.btn_back.is_clicked(mouse_pos, mouse_pressed):
            self.back = True

    def draw(self, surface):
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(WHITE)
        surface.blit(background, (0, 0))
        surface.blit(self.background, (0, 0))
        surface.blit(self.img_coin, (5, 5))
        draw_text(surface, str(self.setting["money"]), 50, BLACK, 60, 5, side="left")

        """商品按鈕"""
        for btn in self.btn_tools:
            # 確認按鈕是否在該頁數
            if not self.btn_tools.index(btn) // 4 == self.page - 1:
                continue

            btn.draw(surface)

        """其他按鈕"""
        self.btn_purchase.draw(surface)
        self.btn_pageUp.draw(surface)
        self.btn_pageDown.draw(surface)
        self.btn_back.draw(surface)
