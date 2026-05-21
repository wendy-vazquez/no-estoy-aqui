import flet as ft
import random


class DreamView:

    def __init__(self, page: ft.Page, controller):

        self.page = page
        self.controller = controller

    # =================================================
    # DESPERTAR
    # =================================================

    def wake_up(self, e):

        self.controller.go_to_room()

    # =================================================
    # EXPLORAR SUEÑO
    # =================================================

    def explore_dream(self, e):

        dream_messages = [
            "Las paredes están respirando.",
            "Escuchas pasos detrás de ti.",
            "El cielo está dentro de la habitación.",
            "La puerta desapareció.",
            "Alguien susurró tu nombre.",
        ]

        self.dream_text.value = random.choice(dream_messages)

        self.controller.add_nostalgia(1)
        self.controller.add_fear(1)

        self.page.update()

    # =================================================
    # UI
    # =================================================

    def build(self):

        title = ft.Text(
            "Sueño",
            size=34,
            color="#FFFFFF",
            font_family="titulo",
        )

        self.dream_text = ft.Text(
            "No estás seguro de estar dormido.",
            size=18,
            color="#DDDDDD",
            text_align=ft.TextAlign.CENTER,
        )

        explore_button = ft.ElevatedButton(
            content=ft.Text("🌙 Explorar"),
            width=250,
            height=50,
            on_click=self.explore_dream,
        )

        wake_button = ft.ElevatedButton(
            content=ft.Text("Despertar"),
            width=250,
            height=50,
            on_click=self.wake_up,
        )

        content = ft.Column(
            controls=[
                title,
                ft.Container(height=20),
                self.dream_text,
                ft.Container(height=30),
                explore_button,
                wake_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/sueno.jpg",
                fit="cover",
                opacity=0.30,
            ),
            bgcolor="#000000",
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                padding=40,
                bgcolor="#000000CC",
                border_radius=15,
                content=content,
            ),
        )