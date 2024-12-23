import pygame

from setting import MAGENTA


"""
地圖繪製僅會在畫面上方 768x384的空間
請繪製時注意不要超出範圍
否則道路將繪製不出來
但依舊會運作，可能造成遊戲BUG

請將768x384的空間切割為64x32的小格子，並以空間座標表示
左上角的格子為(0,0),右下角格子為(11,11)
往右數為x加1(即(0,0)右側的格子為(1,0))
往下數為y加1(即(0,0)下側的格子為(0,1))

types為欲使用的道路(請參考以下代號)
並以[type1, type2, ...] 傳入

pos為道路的座標
並以[(x1, y1), (x2, y2), ...]對應type傳入

使用的道路素材網址為https://opengameart.org/content/5000-isometric-pathway-tiles
"""


# 以下為路的代號
# 0: 十字路口 +
# 1: /
# 2: \
# 3: none
# 4: />
# 5: <\
# 6: \>
# 7: </
# 8: <
# 9: >
# 10: ^
# 11: ˇ

def draw_path(surface, texture, types, pos):

    # 載入道路材質
    tile_image = pygame.image.load(texture).convert()
    tile_image.set_colorkey(MAGENTA)

    # 切割圖片
    tile_width, tile_height = 128, 64  # 每塊 tile 的寬和高
    tiles = []
    image_width, image_height = tile_image.get_size()
    for y in range(0, image_height, tile_height):
        for x in range(0, image_width, tile_width):
            tile = tile_image.subsurface((x, y, tile_width, tile_height))
            tiles.append(tile)

    for i in range(len(types)):
        tile_type = types[i]
        x, y = pos[i]

        drawX = -32 + x * (tile_width // 2)  # 等軸投影的 x 偏移量
        drawY = -16 + y * (tile_height // 2)  # 等軸投影的 y 偏移量
        surface.blit(tiles[tile_type], (drawX, drawY))  # 繪製 tile

