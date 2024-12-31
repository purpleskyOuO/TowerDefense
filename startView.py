import pygame

from setting import *
from button import Button
from draw_text import draw_text


class StartView:
    def __init__(self):
        self.background = pygame.image.load("image/background_start.jpeg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        """按鈕事件"""
        self.startGame = False
        self.openSettings = False
        self.quitGame = False

        self.btn_startGame = Button(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2+10, 300, 80, "開始遊戲", 30)
        self.btn_quit = Button(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2+100, 300, 80, "離開遊戲", 30)

    def update(self):

        # 取得滑鼠事件
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # 更新按鈕狀態
        self.btn_startGame.check_hover(mouse_pos)
        self.btn_quit.check_hover(mouse_pos)

        if self.btn_startGame.is_clicked(mouse_pos, mouse_pressed):
            self.startGame = True

        if self.btn_quit.is_clicked(mouse_pos, mouse_pressed):
            self.quitGame = True

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        draw_text(surface, "衣服保衛戰", 80, PURPLE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100)

        """按鈕"""
        self.btn_startGame.draw(surface)
        self.btn_quit.draw(surface)

    def reset(self):
        self.startGame = False
        self.openSettings = False

