import flet as ft
import random


class MirrorView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

    def return_room(self, e):
        self.controller.go_to_room()

    def stare_mirror(self, e):
        messages = [
            "El reflejo tardó demasiado en moverse.",
            "Tus ojos no parecen tuyos.",
            "El espejo respiró.",
            "Tu reflejo sonrió.",
            "Algo detrás de ti desapareció.",
        ]
        self.message.value = random.choice(messages)
        self.controller.add_fear(2)
        self.controller.reduce_identity(1)
        self.page.update()

    def build(self):

        title = ft.Text(
            "Espejo",
            size=34,
            color="#FFFFFF",
            font_family="titulo",
        )

        self.message = ft.Text(
            "El espejo parece observarte.",
            size=18,
            color="#CCCCCC",
            text_align=ft.TextAlign.CENTER,
        )

        stare_button = ft.ElevatedButton(
            content=ft.Text("Mirar fijamente"),
            width=250,
            height=50,
            on_click=self.stare_mirror,
        )

        back_button = ft.TextButton(
            content=ft.Text("Volver"),
            on_click=self.return_room,
        )

        content = ft.Column(
            controls=[
                title,
                ft.Container(height=20),
                self.message,
                ft.Container(height=30),
                stare_button,
                back_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/espejo.jpg",
                fit="cover",
                opacity=0.25,
            ),
            bgcolor="#000000",
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                padding=40,
                bgcolor="#000000BB",
                border_radius=15,
                content=content,
            ),
        )
