import flet as ft
import asyncio


class RoomView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

    def go_to_mirror(self, e):
        self.controller.go_to_mirror()

    def go_to_dream(self, e):
        self.controller.go_to_dream()

    def go_to_ending(self, e):
        self.controller.go_to_ending()

    def build(self):

        title = ft.Text(
            "La Habitación",
            size=34,
            color="#FFFFFF",
            font_family="titulo",
            text_align=ft.TextAlign.CENTER,
            opacity=0,
            animate_opacity=ft.Animation(900, "easeIn"),
        )

        description = ft.Text(
            "Todo está en silencio.\nHay un espejo frente a ti.\nLa cama está deshecha.\nLa puerta está cerrada.",
            size=16,
            color="#CCCCCC",
            text_align=ft.TextAlign.CENTER,
            font_family="subtitulo",
            opacity=0,
            animate_opacity=ft.Animation(900, "easeIn"),
        )

        mirror_button = ft.ElevatedButton(
            content=ft.Text("Acercarse al espejo"),
            width=280,
            height=50,
            opacity=0,
            animate_opacity=ft.Animation(800, "easeIn"),
            on_click=self.go_to_mirror,
        )

        sleep_button = ft.ElevatedButton(
            content=ft.Text("Volver a dormir"),
            width=280,
            height=50,
            opacity=0,
            animate_opacity=ft.Animation(800, "easeIn"),
            on_click=self.go_to_dream,
        )

        leave_button = ft.ElevatedButton(
            content=ft.Text("Intentar salir"),
            width=280,
            height=50,
            opacity=0,
            animate_opacity=ft.Animation(800, "easeIn"),
            on_click=self.go_to_ending,
        )

        content = ft.Column(
            controls=[
                title,
                ft.Container(height=20),
                description,
                ft.Container(height=30),
                mirror_button,
                sleep_button,
                leave_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        async def reveal_room_controls():
            await asyncio.sleep(0.3)
            for ctrl in [title, description, mirror_button, sleep_button, leave_button]:
                ctrl.opacity = 1
                self.page.update()
                await asyncio.sleep(0.4)

        self.page.run_task(reveal_room_controls)

        return ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/room1.jpeg",
                fit="cover",
                opacity=0.2,
            ),
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                padding=40,
                bgcolor="#000000BB",
                border_radius=15,
                content=content,
            ),
        )
