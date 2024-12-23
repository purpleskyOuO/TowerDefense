import pygame

from draw_text import draw_text


class Button:
    def __init__(self, x, y, width, height, text='', font_size=30, bg_color=(200, 200, 200), text_color=(0, 0, 0), hover_color=(170, 170, 170), border_color=(0, 0, 0), border_width=2):
        """
        初始化按鈕
        :param x: 按鈕的左上角 x 坐標
        :param y: 按鈕的左上角 y 坐標
        :param width: 按鈕的寬度
        :param height: 按鈕的高度
        :param text: 按鈕的文字
        :param font_size: 文字的字體大小
        :param bg_color: 按鈕的背景顏色
        :param text_color: 按鈕文字顏色
        :param hover_color: 滑鼠懸停時的按鈕顏色
        :param border_color: 按鈕邊框顏色
        :param border_width: 按鈕邊框寬度
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.current_color = bg_color
        self.mouseInBtn = False
        self.selected = False
        self.enabled = True

    def draw(self, surface):
        # 繪製按鈕背景
        pygame.draw.rect(surface, self.border_color, self.rect)  # 繪製邊框
        inner_rect = self.rect.inflate(-self.border_width * 2, -self.border_width * 2)  # 計算內部矩形
        pygame.draw.rect(surface, self.current_color, inner_rect)  # 繪製內部背景

        # 繪製文字
        if self.text:
            draw_text(surface, self.text, self.font_size, self.text_color, self.rect)

    def check_hover(self, mouse_pos):
        if not self.selected:
            if self.rect.collidepoint(mouse_pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.bg_color

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
            return True

    def is_selected(self, selected: bool):
        self.selected = selected
        if self.selected:
            self.current_color = self.hover_color


# 測試 Button 類的範例程式
if __name__ == "__main__":
    pygame.init()

    # 視窗初始化
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Button Example")
    clock = pygame.time.Clock()

    # 創建按鈕
    button = Button(300, 250, 200, 100, text="Click Me", font_size=40, border_color=(0, 0, 0), border_width=4)

    running = True
    while running:
        screen.fill((255, 255, 255))

        # 事件處理
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新按鈕狀態
        button.check_hover(mouse_pos)

        if button.is_clicked(mouse_pos, mouse_pressed):
            print("Button clicked!")
            print(str([(x, y) for x in range(15) for y in range(15)]))

        # 繪製按鈕
        button.draw(screen)

        # 更新畫面
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()