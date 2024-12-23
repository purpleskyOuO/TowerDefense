import pygame

from setting import *

from startView import StartView
from chooseStageView import ChooseStageView
from stageView import StageView
from victoryView import VictoryView
from defeatView import DefeatView


class Game:
    def __init__(self):
        """遊戲初始化"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("衣服保衛戰!!!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.view = "start"

        """初始化界面"""
        self.startView = StartView()
        self.chooseStageView = ChooseStageView()
        self.stageView = None
        self.victoryView = None
        self.defeatView = None

        """載入玩家設定與資料"""
        self.setting = load_settings()

    def update(self, events):

        """startView"""
        if self.view == "start":
            if self.startView.startGame:
                self.view = "chooseStage"
                self.chooseStageView.reset()
            elif self.startView.openSettings:
                pass
            elif self.startView.quitGame:
                self.running = False
            else:
                self.startView.update()

        """chooseStageView"""
        if self.view == "chooseStage":
            if self.chooseStageView.stage_confirm:
                self.view = "stage"
                self.stageView = StageView(self.chooseStageView.chooseStage)
            else:
                self.chooseStageView.update()

        """stageView"""
        if self.view == "stage":
            if self.stageView.gameStatus == "victory":
                self.view = "victory"
                if self.setting["stage"] == self.stageView.stage:
                    update_settings(self.setting, "stage", self.setting["stage"] + 1)
                    update_settings(self.setting, "lockWear", False)
                    self.victoryView.unlockClothes(self.stageView.cloth)
                self.victoryView = VictoryView()

            elif self.stageView.gameStatus == "defeat":
                self.view = "defeat"
                if self.setting["stage"] == self.stageView.stage:
                    update_settings(self.setting, "wear", self.stageView.end_cloth)
                    update_settings(self.setting, "lockWear", True)
                    self.defeatView = DefeatView(self.stageView.end_cloth)

            else:
                self.stageView.update(events)

        """victoryView"""
        if self.view == "victory":
            if self.victoryView.continue_clicked:
                self.view = "chooseStage"
                self.stageView = None
                self.victoryView = None
                self.chooseStageView.reset()
            else:
                self.victoryView.update()

        """defeatView"""
        if self.view == "defeat":
            if self.defeatView.continue_clicked:
                self.view = "chooseStage"
                self.stageView = None
                self.defeatView = None
                self.chooseStageView.reset()
            else:
                self.defeatView.update()

    def draw(self, surface):
        """startView"""
        if self.view == "start":
            self.startView.draw(surface)

        """chooseStageView"""
        if self.view == "chooseStage":
            self.chooseStageView.draw(surface)

        """stageView"""
        if self.view == "stage":
            self.stageView.draw(surface)

        """victoryView"""
        if self.view == "victory":
            self.victoryView.draw(surface)

        """defeatView"""
        if self.view == "defeat":
            self.defeatView.draw(surface)

    def game_run(self):
        while self.running:
            """ Checking for events"""
            # 離開遊戲
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

            self.update(events)
            self.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)
