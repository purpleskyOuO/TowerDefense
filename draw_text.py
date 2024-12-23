import pygame

from setting import FONT


def draw_text(surface, text, size, color, *args, side: str = None):
    font = pygame.font.Font(FONT, size=size)
    text_surface = font.render(text, True, color)

    """預設顯示在所選目標中心"""
    if len(args) == 1 and isinstance(args[0], pygame.Rect):
        rect = args[0]
        text_rect = text_surface.get_rect(center=rect.center)

    # 顯示在所選座標
    elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
        x, y = args
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        raise ValueError("Invalid arguments: Pass a pygame.Rect or x, y coordinates.")

    if side:
        """顯示在所選目標左側"""
        if side == "left":
            if len(args) == 1 and isinstance(args[0], pygame.Rect):
                rect = args[0]
                text_rect = text_surface.get_rect(topleft=rect.topleft)

                # 顯示在所選座標
            elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
                x, y = args
                text_rect = text_surface.get_rect(topleft=(x, y))
            else:
                raise ValueError("Invalid arguments: Pass a pygame.Rect or x, y coordinates.")

    surface.blit(text_surface, text_rect)

