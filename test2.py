import pygame
import sys

# 初始化 Pygame
pygame.init()

# 設定視窗大小與標題
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draw Path with Tiles")

# 加載地圖素材
tile_image = pygame.image.load("path/Path_Stones_01-128x64.png").convert()
tile_image.set_colorkey((255, 0, 255))

# 切割 tile 函數
def cut_tile(image, tile_width, tile_height):
    tiles = []
    image_width, image_height = image.get_size()
    for y in range(0, image_height, tile_height):
        for x in range(0, image_width, tile_width):
            tile = image.subsurface((x, y, tile_width, tile_height))
            tiles.append(tile)
    return tiles

# 切割圖片
tile_width, tile_height = 128, 64  # 每塊 tile 的寬和高
tiles = cut_tile(tile_image, tile_width, tile_height)

# 遊戲主迴圈
clock = pygame.time.Clock()
running = True

# 繪製地圖的坐標邏輯
def draw_path(surface, tiles, start_x, start_y, path_length):
    for i in range(path_length):
        x = start_x + i * (tile_width // 2)  # 等軸投影的 x 偏移量
        y = start_y + i * (tile_height // 2)  # 等軸投影的 y 偏移量
        surface.blit(tiles[2], (x, y))  # 繪製 tile

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景顏色
    screen.fill((100, 100, 255))  # 藍色背景

    # 繪製地圖 path
    draw_path(screen, tiles, start_x=-32, start_y=-16, path_length=10)

    # 更新畫面
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
