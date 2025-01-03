import pygame

from setting import *

from startView import StartView
from chooseStageView import ChooseStageView
from changeWearView import ChangeWearView
from shopView import ShopView
from stageView import StageView
from victoryView import VictoryView
from defeatView import DefeatView
from storyView import StoryView


class Game:
    def __init__(self):
        """遊戲初始化"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("衣服保衛戰!!!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.view = "start"

        """初始化界面"""
        self.startView = StartView()
        self.chooseStageView = ChooseStageView()
        self.changeWearView = ChangeWearView()
        self.shopView = ShopView()
        self.stageView = None
        self.victoryView = VictoryView()
        self.defeatView = DefeatView()
        self.storyView = StoryView()

        """載入玩家設定與資料"""
        self.setting = load_settings()

    def update(self, events):

        """startView"""
        if self.view == "start":
            if self.startView.startGame:
                if self.setting["stage"] == 1:
                    self.view = "story"
                    self.storyView.loadStory("start")
                else:
                    self.view = "chooseStage"
                    self.chooseStageView.reset()
            elif self.startView.quitGame:
                self.running = False
            else:
                self.startView.update()

        """storyView"""
        if self.view == "story":
            if self.storyView.end:
                self.view = "chooseStage"
                self.chooseStageView.reset()
            else:
                self.storyView.update()

        """chooseStageView"""
        if self.view == "chooseStage":
            if self.chooseStageView.stage_confirm:
                self.view = "stage"
                self.stageView = StageView(self.chooseStageView.chooseStage)
            elif self.chooseStageView.openShop:
                self.view = "shop"
                self.shopView.reset()
            elif self.chooseStageView.changeWear:
                self.view = "changeWear"
                self.changeWearView.reset()
            elif self.chooseStageView.quit:
                self.running = False
            else:
                self.chooseStageView.update()

        """stageView"""
        if self.view == "stage":
            if self.stageView.gameStatus == "victory":
                self.view = "victory"
                self.victoryView.reset()
                self.setting = update_settings("money", self.setting["money"] + self.stageView.reward)
                if self.setting["stage"] == self.stageView.stage:
                    self.setting = update_settings("stage", self.setting["stage"] + 1)
                    self.setting = update_settings("lockWear", False)
                    self.victoryView.unlockClothes(self.stageView.cloth)

            elif self.stageView.gameStatus == "defeat":
                self.view = "defeat"
                self.defeatView.reset()
                if self.setting["stage"] == self.stageView.stage:
                    self.setting = update_settings("wear", self.stageView.end_cloth)
                    self.setting = update_settings("lockWear", True)
                    self.defeatView.lockCloth(self.stageView.end_cloth)
            elif self.stageView.gameStatus == "quit":
                self.view = "chooseStage"
                self.stageView = None
                self.chooseStageView.reset()
            else:
                self.stageView.update(events)

        """victoryView"""
        if self.view == "victory":
            if self.victoryView.continue_clicked:
                self.view = "chooseStage"
                self.stageView = None
                self.victoryView.firstWin = False
                self.chooseStageView.reset()
            else:
                self.victoryView.update()

        """defeatView"""
        if self.view == "defeat":
            if self.defeatView.continue_clicked:
                self.view = "chooseStage"
                self.stageView = None
                self.defeatView.firstLose = False
                self.chooseStageView.reset()
            else:
                self.defeatView.update()

        """shopView"""
        if self.view == "shop":
            if self.shopView.back:
                self.view = "chooseStage"
                self.chooseStageView.reset()
            else:
                self.shopView.update()

        """changeWearView"""
        if self.view == "changeWear":
            if self.changeWearView.back:
                self.view = "chooseStage"
                self.chooseStageView.reset()
            else:
                self.changeWearView.update()

    def draw(self, surface):
        """startView"""
        if self.view == "start":
            self.startView.draw(surface)

        """storyView"""
        if self.view == "story":
            self.storyView.draw(surface)

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

        """shopView"""
        if self.view == "shop":
            self.shopView.draw(surface)

        """changeWearView"""
        if self.view == "changeWear":
            self.changeWearView.draw(surface)

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
