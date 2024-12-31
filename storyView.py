import pygame

from setting import *

from draw_text import draw_text


class StoryView:
    def __init__(self):
        """background"""
        self.background = pygame.image.load("image/background_storyView.jpeg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.lines = 0
        self.story = []
        self.clicked = False
        self.end = False

    def reset(self):
        self.lines = 0
        self.story = []
        self.clicked = False
        self.end = False

    def loadStory(self, story):
        self.reset()

        if os.path.exists(f"story/{story}.txt"):
            with open(f"story/{story}.txt", "r", encoding="utf-8") as file:
                storyLines = file.readlines()
                self.story = [line.strip() for line in storyLines]

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0]:
            self.clicked = True

        if self.clicked and not mouse_pressed[0]:
            self.lines += 1

            if self.story[self.lines] == "end":
                self.end = True

            elif self.story[self.lines] == "turn page":
                self.story = self.story[self.lines+1:]
                self.lines = 0

            self.clicked = False

    def draw(self, surface: pygame.Surface):
        """background"""
        surface.blit(self.background, (0, 0))

        if not self.end:
            for i in range(self.lines+1):
                draw_text(surface, self.story[i], 30, WHITE, SCREEN_WIDTH/2, 130+30*i)
