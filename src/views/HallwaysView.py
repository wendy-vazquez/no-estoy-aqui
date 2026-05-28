import flet as ft
import asyncio

class HallwaysView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

    def go_to_room(self, e):
        self.controller.go_to_room()

    def go_to_mirror(self, e):
        self.controller.go_to_mirror()

    def go_to_dream(self, e):
        self.controller.go_to_dream()

    def go_to_ending(self, e):
        self.controller.go_to_ending()

    def resize_dialog(self, e=None):

        if hasattr(self, "dialogue_box"):

            self.dialogue_box.width = self.page.window.width - 60

            self.page.update()

    def build(self):

        # TEXTO
        self.dialogue_text = ft.Text(
            "",
            size=34,
            color="#FFFFFF",
            font_family="contenido",
            weight=ft.FontWeight.W_500,
        )

        # NOMBRE
        name_box = ft.Container(
            padding=ft.Padding(20, 10, 20, 10),
            bgcolor="#000000AA",
            border_radius=12,
            content=ft.Text(
                "Pasillos",
                size=22,
                color="#FFFFFF",
                font_family="btninicio",
            ),
        )

        # CAJA DE DIÁLOGO
        self.dialogue_box = ft.Container(
            width=self.page.window.width - 60,
            height=280,
            padding=30,
            bgcolor="#000000CC",
            border_radius=22,

            border=ft.border.Border(
                top=ft.border.BorderSide(3, "#FFFFFF"),
                left=ft.border.BorderSide(3, "#FFFFFF"),
                right=ft.border.BorderSide(3, "#FFFFFF"),
                bottom=ft.border.BorderSide(3, "#FFFFFF"),
            ),
            content=ft.Column(
                [
                    self.dialogue_text,
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
        )