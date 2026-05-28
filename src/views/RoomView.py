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
                "Habitación",
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
                top=ft.BorderSide(1, "#3A3A3A"),
                bottom=ft.BorderSide(1, "#3A3A3A"),
                left=ft.BorderSide(1, "#3A3A3A"),
                right=ft.BorderSide(1, "#3A3A3A"),
            ),

            content=ft.Column(
                expand=True,
                controls=[

                    self.dialogue_text,

                    ft.Container(expand=True),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Icon(
                                ft.Icons.KEYBOARD_ARROW_DOWN,
                                color="#BEBEBE",
                                size=34,
                            )
                        ]
                    )
                ]
            ),
        )

        # BOTONES
        mirror_button = ft.ElevatedButton(
            content=ft.Text(
                "Acercarse al espejo",
                font_family="btninicio",
                size=18,
            ),
            width=300,
            height=52,
            opacity=0,
            animate_opacity=400,
            on_click=self.go_to_mirror,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        sleep_button = ft.ElevatedButton(
            content=ft.Text(
                "Volver a dormir",
                font_family="btninicio",
                size=18,
            ),
            width=300,
            height=52,
            opacity=0,
            animate_opacity=400,
            on_click=self.go_to_dream,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        leave_button = ft.ElevatedButton(
            content=ft.Text(
                "Intentar salir",
                font_family="btninicio",
                size=18,
            ),
            width=300,
            height=52,
            opacity=0,
            animate_opacity=400,
            on_click=self.go_to_ending,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        # UI INFERIOR
        bottom_ui = ft.Container(
            expand=True,

            alignment=ft.alignment.Alignment(0, 1),

            padding=ft.Padding(30, 0, 30, 25),

            content=ft.Column(
                tight=True,

                alignment=ft.MainAxisAlignment.END,

                horizontal_alignment=ft.CrossAxisAlignment.START,

                controls=[

                    name_box,

                    ft.Container(height=12),

                    self.dialogue_box,

                    ft.Container(height=18),

                    ft.Row(
                        controls=[
                            mirror_button,
                            sleep_button,
                            leave_button,
                        ],
                        wrap=True,
                        spacing=15,
                    )
                ],
            ),
        )

        # ANIMACIÓN TEXTO
        async def reveal_room():

            text = (
                "Todo está en silencio...\n"
                "Hay un espejo frente a ti.\n"
                "La cama está deshecha.\n"
                "La puerta está cerrada."
            )

            current = ""

            await asyncio.sleep(0.5)

            for char in text:

                current += char

                self.dialogue_text.value = current

                self.page.update()

                if char in [".", ","]:
                    await asyncio.sleep(0.08)
                else:
                    await asyncio.sleep(0.02)

            await asyncio.sleep(0.3)

            mirror_button.opacity = 1
            self.page.update()

            await asyncio.sleep(0.2)

            sleep_button.opacity = 1
            self.page.update()

            await asyncio.sleep(0.2)

            leave_button.opacity = 1
            self.page.update()

        self.page.run_task(reveal_room)

        self.page.on_resize = self.resize_dialog

        # LAYOUT FINAL
        return ft.Stack(
            expand=True,
            controls=[

                # FONDO
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="img/room1.jpeg",
                        fit="cover",
                    ),
                ),

                # OVERLAY
                ft.Container(
                    expand=True,
                    bgcolor="#00000066",
                ),

                # UI
                bottom_ui,
            ],
        )