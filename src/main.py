import sys
from pathlib import Path

import flet as ft

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = Path(__file__).resolve().parent
for path in (str(SRC_DIR), str(ROOT_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

from views.MenuView import MenuView


async def start(page: ft.Page):
    page.title = "No estoy aquí"
    page.window.width = 600
    page.window.height = 900
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#090909"
    page.padding = 0
    page.spacing = 0
    page.fonts = {
        "titulo": "assets/fonts/La Machine Company.ttf",
        "subtitulo": "assets/fonts/Stamp.ttf",
        "btninicio": "assets/fonts/STAMPWRITER-KIT.ttf",
        "contenido": "assets/fonts/typenoksidi.ttf",
    }
    menu = MenuView(page)
    page.add(menu.build())


def main():
    assets_path = str(ROOT_DIR / "assets")
    ft.app(target=start, assets_dir=assets_path)

if __name__ == "__main__":
    main()