import json
import os
import pygame

"""顏色"""
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 97, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (8, 46, 84)
PURPLE = (160, 32, 240)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

"""字型"""
FONT = "Font/NaikaiFont-Regular-Lite.ttf"

"""遊戲基本設定"""
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600
FPS = 60
IMG_TOOLS = "image/tools"
IMG_CLOTHES = "image/clothes"

"""預設遊戲玩家設定"""
DEFAULT_SETTINGS = {
    "stage": 1,
    "tools": ["scissor"],
    "clothes": ["default"],
    "wear": "default",
    "lockWear": False
}

SETTINGS_FILE = "settings.json"


def load_settings():
    """讀取設定檔，若不存在則生成預設檔案"""
    if os.path.exists(SETTINGS_FILE):
        # 如果設定檔存在，讀取內容
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    else:
        # 如果設定檔不存在，創建並寫入預設設定
        print(f"設定檔 {SETTINGS_FILE} 不存在，正在創建預設檔案...")
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS


def save_settings(settings):
    """將遊戲設定儲存到檔案"""
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)
    print(f"設定已儲存至 {SETTINGS_FILE}")


def update_settings(settings, key, value):
    """更新指定設定項目"""
    if key in settings:
        settings[key] = value
        save_settings(settings)
    elif key in settings.get("keybindings", {}):
        settings["keybindings"][key] = value
        save_settings(settings)
    else:
        print(f"無效的設定鍵：{key}")


