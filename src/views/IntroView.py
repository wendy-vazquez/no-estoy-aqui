import flet as ft
import asyncio
from views.audio_utils import make_mute_button

# CAMBIO: 2025 — botón mute agregado


class IntroView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

    def continue_game(self, e):
        self.controller.go_to_room()

    def resize_dialog(self, e=None):

        if hasattr(self, "dialogue_box"):

            self.dialogue_box.width = self.page.window.width - 60

            self.page.update()

    def build(self):

        lines = [
            "Despertas...",
            "La habitación está silenciosa... Demasiado silenciosa.",
            "No recuerdas haberte dormido.",
            "Pero algo..."
            "se siente diferente.",
        ]

        # TEXTO
        self.dialogue_text = ft.Text(
            "",
            size=30,
            color="#FFFFFF",
            font_family="contenido",
            weight=ft.FontWeight.W_500,
            selectable=False,
        )

        # NOMBRE
        name_box = ft.Container(
            padding=ft.Padding(20, 10, 20, 10),
            bgcolor="#000000AA",
            border_radius=12,
            content=ft.Text(
                "???",
                size=22,
                color="#FFFFFF",
                font_family="btninicio",
            ),
        )

        # CAJA DE DIÁLOGO
        self.dialogue_box = ft.Container(
            width=self.page.window.width - 60,
            height=260,
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

                    # TEXTO
                    self.dialogue_text,

                    # ESPACIO FLEXIBLE
                    ft.Container(expand=True),

                    # FLECHITA ABAJO
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Icon(
                                ft.Icons.KEYBOARD_ARROW_DOWN,
                                color="#BEBEBE",
                                size=30,
                            )
                        ]
                    )
                ]
            ),
        )

        # BOTÓN CONTINUAR
        continue_button = ft.TextButton(
            content=ft.Text(
                "CONTINUAR",
                size=20,
                color="#DAB6FF",
                font_family="btninicio",
            ),
            opacity=0,
            animate_opacity=400,
            on_click=self.continue_game,
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

                    ft.Container(height=10),

                    continue_button,
                ],
            ),
        )

        # TYPEWRITER
        async def reveal_text():

            await asyncio.sleep(0.8)

            full_text = "\n".join(lines)

            current = ""

            for char in full_text:

                current += char

                self.dialogue_text.value = current

                self.page.update()

                if char in [".", ","]:
                    await asyncio.sleep(0.09)
                else:
                    await asyncio.sleep(0.025)

            await asyncio.sleep(0.4)

            continue_button.opacity = 1

            self.page.update()

        self.page.run_task(reveal_text)

        self.page.on_resize = self.resize_dialog

        # LAYOUT FINAL
        return ft.Stack(
            expand=True,
            controls=[

                # FONDO
                ft.Image(
                    src="img/intro_bg.jpg",
                    fit="cover",
                    expand=True,
                ),

                # OVERLAY
                ft.Container(
                    expand=True,
                    bgcolor="#00000066",
                ),

                # UI
                bottom_ui,
                # MUTE — CAMBIO: 2025
                make_mute_button(self.page),
            ],
        )