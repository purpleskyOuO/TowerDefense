import pygame
import math
import random

# 初始化 Pygame
pygame.init()

# 遊戲視窗設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("簡單塔防遊戲")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 遊戲時鐘
clock = pygame.time.Clock()

# 設定
TILE_SIZE = 40
ENEMY_SPEED = 2
TOWER_ATTACK_RADIUS = 100
TOWER_ATTACK_DAMAGE = 5

# 地圖路徑
PATH = [
    (0, 300), (200, 300), (200, 200), (400, 200),
    (400, 400), (600, 400), (600, 100), (800, 100)
]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.path = path
        self.current_point = 0
        self.rect.topleft = self.path[self.current_point]
        self.health = 100

    def update(self):
        if self.current_point < len(self.path) - 1:
            # 移動到下一個點
            target_x, target_y = self.path[self.current_point + 1]
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < ENEMY_SPEED:
                self.current_point += 1
            else:
                self.rect.x += ENEMY_SPEED * dx / distance
                self.rect.y += ENEMY_SPEED * dy / distance



class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.attack_radius = TOWER_ATTACK_RADIUS
        self.damage = TOWER_ATTACK_DAMAGE

    def attack(self, enemies):
        for enemy in enemies:
            distance = math.sqrt(
                (enemy.rect.centerx - self.rect.centerx) ** 2 +
                (enemy.rect.centery - self.rect.centery) ** 2
            )
            if distance <= self.attack_radius:
                enemy.health -= self.damage
                if enemy.health <= 0:
                    enemy.kill()


# 遊戲初始化
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()

# 建立一個塔
tower = Tower(400, 300)
towers.add(tower)

# 遊戲主迴圈
running = True
spawn_timer = 0

while running:
    screen.fill(WHITE)

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 產生敵人
    spawn_timer += 1
    if spawn_timer > 100:  # 每 100 幀產生一個敵人
        enemy = Enemy(PATH)
        enemies.add(enemy)
        spawn_timer = 0

    # 更新敵人
    enemies.update()

    # 塔攻擊敵人
    for tower in towers:
        tower.attack(enemies.sprites())

    # 繪製路徑
    for i in range(len(PATH) - 1):
        pygame.draw.line(screen, BLACK, PATH[i], PATH[i + 1], 5)

    # 繪製塔與敵人
    towers.draw(screen)
    enemies.draw(screen)

    # 繪製敵人生命條
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy.rect.x, enemy.rect.y - 10, 30, 5))
        pygame.draw.rect(screen, GREEN, (enemy.rect.x, enemy.rect.y - 10, 30 * (enemy.health / 100), 5))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
