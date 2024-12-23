import pygame
import os

from setting import *
from draw_text import draw_text
from setting import IMG_TOOLS

BTN_WIDTH = 200
BTN_HEIGHT = 280


class Btn_shopTools:
    def __init__(self, x, y, tool, price, bg_color=(200, 200, 200), hover_color=(170, 170, 170), border_color=(0, 0, 0), border_width=1):
        """
        初始化按鈕
        :param x: 按鈕的左上角 x 坐標
        :param y: 按鈕的左上角 y 坐標
        :param tool: 工具名稱
        :param price: 工具價格
        :param bg_color: 按鈕的背景顏色
        :param hover_color: 滑鼠懸停時的按鈕顏色
        :param border_color: 按鈕邊框顏色
        :param border_width: 按鈕邊框寬度
        """

        self.rect = pygame.Rect(x, y, BTN_WIDTH, BTN_HEIGHT)
        self.x = x
        self.y = y
        self.tool = tool
        self.price = price
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.current_color = bg_color
        self.mouseInBtn = False
        self.selected = False
        self.enabled = True
        self.mouse_pos = None
        self.showInfo = False

        self.img_tool = pygame.image.load(f"{IMG_TOOLS}/{self.tool}.png").convert_alpha()
        self.img_tool = pygame.transform.scale(self.img_tool, (180, 180))

        self.img_coin = pygame.image.load("image/coin.png").convert_alpha()
        self.img_coin = pygame.transform.scale(self.img_coin, (50, 50))

        """載入道具資料"""
        if os.path.exists(f"tools/{self.tool}.json"):
            with open(f"tools/{self.tool}.json", "r") as file:
                self.tool_info = json.load(file)

    def draw(self, surface):
        # 繪製按鈕背景
        pygame.draw.rect(surface, self.border_color, self.rect)  # 繪製邊框
        inner_rect = self.rect.inflate(-self.border_width * 2, -self.border_width * 2)  # 計算內部矩形
        pygame.draw.rect(surface, self.current_color, inner_rect)  # 繪製內部背景

        # 加入圖片
        surface.blit(self.img_tool, (self.rect.x + 10, self.rect.y + 10))
        surface.blit(self.img_coin, (self.rect.x + 5, self.rect.y + 200))

        # 繪製價格
        draw_text(surface, str(self.price), 50, BLACK, self.rect.x + 70, self.rect.y + 200, side="left")

        if self.showInfo:
            info_x = self.mouse_pos[0] + 10
            info_y = self.mouse_pos[1]
            info_rect = pygame.Rect(info_x, info_y, 100, 100)

            pygame.draw.rect(surface, BLACK, info_rect)  # 繪製邊框
            inner_rect = info_rect.inflate(-2, -2)  # 計算內部矩形
            pygame.draw.rect(surface, GRAY, inner_rect)  # 繪製內部背景

            draw_text(surface, f"花費: {self.tool_info['cost']}", 10, BLACK, info_x+5, info_y+5, side="left")
            draw_text(surface, f"傷害: {self.tool_info['damage']}", 10, BLACK, info_x+5, info_y+20, side="left")
            draw_text(surface, f"冷卻時間: {self.tool_info['cooldown']}", 10, BLACK, info_x+5, info_y+35, side="left")
            draw_text(surface, f"攻擊半徑: {self.tool_info['radius']}", 10, BLACK, info_x+5, info_y+50, side="left")
            if self.tool_info["AOE"]:
                draw_text(surface, "範圍攻擊", 10, BLACK, info_x+5, info_y+65, side="left")
            else:
                draw_text(surface, "單體攻擊", 10, BLACK, info_x+5, info_y+65, side="left")

    def check_hover(self, mouse_pos):
        if not self.selected:
            if self.rect.collidepoint(mouse_pos):
                self.current_color = self.hover_color
                self.showInfo = True
            else:
                self.current_color = self.bg_color
                self.showInfo = False

        self.mouse_pos = mouse_pos

    def is_clicked(self, mouse_pos, mouse_pressed):
        """
        檢查按鈕是否被點擊
        :return: 如果按鈕被點擊返回 True，否則返回 False
        """
        # 是否將按鈕關閉
        if not self.enabled:
            return False

        if self.rect.collidepoint(mouse_pos) and not mouse_pressed[0]:
            self.mouseInBtn = True
            return False
        elif self.rect.collidepoint(mouse_pos) and mouse_pressed[0] and self.mouseInBtn:
            self.mouseInBtn = False
            self.showInfo = False
            return True

    def is_selected(self, selected: bool):
        self.selected = selected
        if self.selected:
            self.current_color = self.hover_color
