import pygame

from draw_text import draw_text
from setting import IMG_TOOLS

BTN_WIDTH = 90
BTN_HEIGHT = 120


class Btn_tools:
    def __init__(self, x, y, tool, cost, bg_color=(200, 200, 200), hover_color=(170, 170, 170), border_color=(0, 0, 0), border_width=1):
        """
        初始化按鈕
        :param x: 按鈕的左上角 x 坐標
        :param y: 按鈕的左上角 y 坐標
        :param tool: 工具名稱
        :param cost: 工具價格
        :param bg_color: 按鈕的背景顏色
        :param hover_color: 滑鼠懸停時的按鈕顏色
        :param border_color: 按鈕邊框顏色
        :param border_width: 按鈕邊框寬度
        """

        self.rect = pygame.Rect(x, y, BTN_WIDTH, BTN_HEIGHT)
        self.x = x
        self.y = y
        self.tool = tool
        self.cost = cost
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.current_color = bg_color
        self.mouseInBtn = False
        self.selected = False
        self.enabled = True

        self.img_tool = pygame.image.load(f"{IMG_TOOLS}/{self.tool}.png").convert_alpha()
        self.img_tool = pygame.transform.scale(self.img_tool, (70, 70))

        self.img_coin = pygame.image.load("image/coin.png").convert_alpha()
        self.img_coin = pygame.transform.scale(self.img_coin, (30, 30))

    def draw(self, surface):
        # 繪製按鈕背景
        pygame.draw.rect(surface, self.border_color, self.rect)  # 繪製邊框
        inner_rect = self.rect.inflate(-self.border_width * 2, -self.border_width * 2)  # 計算內部矩形
        pygame.draw.rect(surface, self.current_color, inner_rect)  # 繪製內部背景

        # 加入圖片
        surface.blit(self.img_tool, (self.rect.x + 10, self.rect.y + 5))
        surface.blit(self.img_coin, (self.rect.x + 3, self.rect.y + 80))

        # 繪製價格
        draw_text(surface, str(self.cost), 30, (0, 0, 0), self.rect.x + 37, self.rect.y + 81, side="left")

    def check_hover(self, mouse_pos):
        if not self.selected:
            if self.rect.collidepoint(mouse_pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.bg_color

    def is_clicked(self, mouse_pos, mouse_pressed, money):
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
            if money >= self.cost:
                return True
            else:
                print("金錢不夠")
                return False
