import flet as ft
import asyncio


class IntroView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

    def continue_game(self, e):
        self.controller.go_to_room()

    def build(self):

        lines = [
            "Despiertas.",
            "La habitación está silenciosa.",
            "No recuerdas haberte dormido.",
            "Pero algo...",
            "se siente diferente.",
        ]

        text_controls = [
            ft.Text(
                line,
                size=24,
                color="#EAEAEA",
                text_align=ft.TextAlign.CENTER,
                font_family="contenido",
                opacity=0,
                animate_opacity=ft.Animation(900, "easeIn"),
            )
            for line in lines
        ]

        continue_button = ft.ElevatedButton(
            content=ft.Text("Continuar", 
            font_family="btninicio"),
            width=220,
            height=50,
            opacity=0,
            animate_opacity=ft.Animation(800, "easeIn"),
            on_click=self.continue_game,
            color="#D595F0",
            bgcolor="#0E105F",
        )

        content = ft.Column(
            controls=[
                *text_controls,
                ft.Container(height=40),
                continue_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        async def reveal_lines():
            await asyncio.sleep(0.3)
            for ctrl in text_controls:
                ctrl.opacity = 1
                self.page.update()
                await asyncio.sleep(1.2)
            continue_button.opacity = 1
            self.page.update()

        self.page.run_task(reveal_lines)

        return ft.Container(
            expand=True,
            bgcolor="#000000",
            alignment=ft.Alignment(0, 0),
            content=content,
        )
