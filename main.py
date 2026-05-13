import flet as ft
from views.MenuView import MenuView
from controllers.GameController import GameController


def main(page: ft.Page):
    page.title = "No estoy aquí"

    page.window.width = 1200
    page.window.height = 700

    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#090909"

    page.padding = 0
    page.spacing = 0
    
    page.fonts={
        "titulo" : "assets/fonts/La Machine Company.ttf",
        "subtitulo" : "assets/fonts/Stamp.ttf",
        "btninicio" : "assets/fonts/STAMPWRITER-KIT.ttf"
    }

    menu = MenuView(page)

    page.add(menu.build())


ft.app(target=main, assets_dir="assets")