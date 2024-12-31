import json
import math
import pygame
import os

from setting import *
from draw_text import draw_text
from draw_path import draw_path

from button import Button
from btn_tools import Btn_tools
from tool import Tool
from enemy import Enemy
from role import Role


def draw_toolProgress(surface, tool):
    center = tool.rect.center
    radius = 30
    thickness = 5

    now = pygame.time.get_ticks()
    progress_angle = (now - tool.atk_time) / tool.cooldown * 360

    """draw"""
    pygame.draw.circle(surface, WHITE, center, radius)

    # 繪製進度部分的圓弧
    start_angle = -90  # 從頂部開始
    end_angle = start_angle + progress_angle
    rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
    pygame.draw.arc(surface, PROGRESS_COLOR, rect, math.radians(start_angle), math.radians(end_angle), thickness)


class StageView:
    def __init__(self, stage):
        try:
            """Background"""
            self.background = pygame.image.load("image/background_stage.jpeg").convert_alpha()
            self.background.set_alpha(128)
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

            self.bg_pause = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_pause.fill(GRAY)
            self.bg_pause.set_alpha(64)

            """載入關卡設定"""
            if os.path.exists(f"stages/stage_{stage}.json"):
                with open(f"stages/stage_{stage}.json", "r") as file:
                    self.stages = json.load(file)

            self.stage = stage
            self.path_texture = self.stages["path_texture"]
            self.path_type = self.stages["path_type"]
            self.path_pos = self.stages["path_pos"]
            self.cloth = self.stages["cloth"]
            self.waves_num = self.stages["waves_num"]
            self.waves = self.stages["waves"]
            self.reward = self.stages["reward"]

            """網格化地圖"""
            self.tiles = [[x, y] for x in range(12) for y in range(12)]
            self.tiles_rect = [pygame.Rect(tile[0] * 64, tile[1] * 32, 64, 32) for tile in self.tiles]

            """遊戲狀態"""
            self.gameStatus = "fight"
            self.currentWave = 1
            self.end_cloth = None

            """工具欄"""
            self.bg_toolbar = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 12 * 32))
            self.bg_toolbar.fill((255, 255, 153))
            self.toolbar_x = 0
            self.toolbar_y = 12 * 32
            self.img_coin = pygame.image.load("image/coin.png").convert_alpha()
            self.img_coin = pygame.transform.scale(self.img_coin, (30, 30))
            self.money = 100
            self.tool_group = pygame.sprite.Group()
            self.page = 1

            self.setting = load_settings()

            """暫停按鈕"""
            self.btn_gamePause = Button(20, 20, 50, 50, "||", 30)
            self.btn_continue = Button(SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 60, 100, 60, "繼續", 30)
            self.btn_back = Button(SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 - 60, 100, 60, "退出", 30)

            """工具按鈕"""
            self.tools = self.setting["tools"]

            self.btn_tools = []
            for i in range(len(self.tools)):
                with open(f"tools/{self.tools[i]}.json", "r") as file:
                    tool = json.load(file)

                btn_x = self.toolbar_x + 10 + i % 5 * 100
                btn_y = self.toolbar_y + 50
                self.btn_tools.append(Btn_tools(btn_x, btn_y, self.tools[i], tool["cost"]))

            """切換工具頁按鈕"""
            self.btn_pageUp = Button(self.toolbar_x + 850, self.toolbar_y + 50, 50, 50, "<", 30)
            self.btn_pageDown = Button(self.toolbar_x + 850, self.toolbar_y + 120, 50, 50, ">", 30)

            """工具選擇狀態"""
            self.selectedTool = None
            self.img_selectedTool = None
            self.rect_selectedTool = None

            """初始化敵人"""
            self.enemy_group = pygame.sprite.Group()
            self.enemy_generator_time = 0
            self.enemy_generator_delay = 1000
            self.enemy_summoned = 0  # 當前波數已生成敵人量
            self.waves_delay = self.enemy_generator_delay * 5
            self.nextWave_time = 0
            self.waitNextWave = False

            """載入角色"""
            self.role = Role(720, 10, 250, 375)

        except Exception as e:
            print(e)
            print("載入關卡失敗")

    def enemy_generator(self):
        now = pygame.time.get_ticks()

        if self.waitNextWave and now - self.nextWave_time >= self.waves_delay:
            self.waitNextWave = False

        if self.waves and not self.waitNextWave:
            if now - self.enemy_generator_time > self.enemy_generator_delay:
                self.enemy_group.add(Enemy(self.waves[0][0][0], self.path_pos))
                self.enemy_generator_time = pygame.time.get_ticks()
                self.enemy_summoned += 1
                if self.enemy_summoned >= self.waves[0][0][1]:
                    self.waves[0].pop(0)
                    self.enemy_summoned = 0

                    if not self.waves[0]:
                        self.waves.pop(0)
                        self.currentWave += 1
                        self.nextWave_time = pygame.time.get_ticks()
                        self.waitNextWave = True

    def check_enemyDeath(self):
        for enemy in self.enemy_group.sprites():
            if enemy.health <= 0:
                self.money += enemy.drop
                enemy.kill()

    def check_reachEnd(self):
        for enemy in self.enemy_group.sprites():
            if enemy.rect.left >= 64 * 12:
                self.gameStatus = "defeat"
                self.end_cloth = enemy.name

    def update(self, events):

        """取得滑鼠事件"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.gameStatus == "fight":

            """敵人更新"""
            self.enemy_group.update()
            self.enemy_generator()
            self.check_enemyDeath()
            self.check_reachEnd()

            """工具更新"""
            self.tool_group.update(self.enemy_group.sprites())

            """工具欄更新"""
            for btn_tool in self.btn_tools:
                # 確認按鈕是否在該頁數
                if not self.btn_tools.index(btn_tool) // 5 == self.page - 1:
                    continue

                btn_tool.check_hover(mouse_pos)

                if btn_tool.is_clicked(mouse_pos, mouse_pressed, self.money):
                    self.selectedTool = btn_tool.tool
                    self.img_selectedTool = pygame.image.load(f"{IMG_TOOLS}/{btn_tool.tool}.png").convert_alpha()
                    self.img_selectedTool = pygame.transform.scale(self.img_selectedTool, (50, 50))
                    self.rect_selectedTool = self.img_selectedTool.get_rect()

                if btn_tool.tool == self.selectedTool:
                    btn_tool.is_selected(True)
                else:
                    btn_tool.is_selected(False)

            """切頁按鈕"""
            self.btn_pageUp.check_hover(mouse_pos)
            self.btn_pageDown.check_hover(mouse_pos)

            if self.btn_pageUp.is_clicked(mouse_pos, mouse_pressed) and self.page != 1:
                self.page -= 1

            if self.btn_pageDown.is_clicked(mouse_pos, mouse_pressed) and self.page != (
                    (len(self.btn_tools) - 1) // 5) + 1:
                self.page += 1

            """放置工具"""
            if self.selectedTool:
                if not mouse_pressed[0]:
                    for tile_rect in self.tiles_rect:
                        if tile_rect.collidepoint(mouse_pos) and not \
                                self.tiles[self.tiles_rect.index(tile_rect)] in self.path_pos and \
                                tile_rect.center not in [tool.rect.center for tool in self.tool_group]:
                            newTool = Tool(tile_rect.center, self.selectedTool)
                            self.tool_group.add(newTool)
                            self.money -= newTool.cost

                    self.selectedTool = None

            """暫停按鈕"""
            self.btn_gamePause.check_hover(mouse_pos)

            if self.btn_gamePause.is_clicked(mouse_pos, mouse_pressed):
                self.gameStatus = "pause"

        else:
            self.btn_continue.check_hover(mouse_pos)

            if self.btn_continue.is_clicked(mouse_pos, mouse_pressed):
                self.gameStatus = "fight"

            self.btn_back.check_hover(mouse_pos)

            if self.btn_back.is_clicked(mouse_pos, mouse_pressed):
                self.gameStatus = "quit"

        """檢查遊戲勝利"""
        if not self.enemy_group.sprites() and not self.waves:
            self.gameStatus = "victory"

    def draw(self, surface: pygame.Surface):
        """背景與標題"""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(WHITE)
        surface.blit(background, (0, 0))
        surface.blit(self.background, (0, 0))
        draw_path(surface, self.path_texture, self.path_type, self.path_pos)

        # 繪製工具進度條
        for tool in self.tool_group:
            draw_toolProgress(surface, tool)

        self.enemy_group.draw(surface)
        self.tool_group.draw(surface)

        """繪製敵人生命條"""
        for enemy in self.enemy_group:
            pygame.draw.rect(surface, RED, (enemy.rect.x, enemy.rect.y - 10, 30, 5))
            pygame.draw.rect(surface, GREEN, (enemy.rect.x, enemy.rect.y - 10, 30 * (enemy.health / enemy.life), 5))

        """工具欄"""
        surface.blit(self.bg_toolbar, (self.toolbar_x, self.toolbar_y))
        surface.blit(self.img_coin, (self.toolbar_x + 5, self.toolbar_y + 5))
        draw_text(surface, str(self.money), 30, BLACK, self.toolbar_x + 40, self.toolbar_y + 6, side="left")

        """工具購買按鈕"""
        for btn_tool in self.btn_tools:
            # 確認按鈕是否在該頁數
            if not self.btn_tools.index(btn_tool) // 5 == self.page - 1:
                continue

            btn_tool.draw(surface)

        self.btn_pageUp.draw(surface)
        self.btn_pageDown.draw(surface)

        """放置工具"""
        if self.selectedTool and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.rect_selectedTool.center = mouse_pos
            surface.blit(self.img_selectedTool, self.rect_selectedTool)

        """繪製角色"""
        self.role.draw(surface)

        """暫停遊戲"""
        self.btn_gamePause.draw(surface)

        if self.gameStatus == "pause":
            surface.blit(self.bg_pause, (0, 0))
            self.btn_continue.draw(surface)
            self.btn_back.draw(surface)
