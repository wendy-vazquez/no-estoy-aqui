import flet as ft
import random
import asyncio
from views.audio_utils import make_mute_button

class DreamView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

        self.dream_messages = [
            "Las paredes están respirando.",
            "Escuchas pasos detrás de ti.",
            "El cielo está dentro de la habitación.",
            "La puerta desapareció.",
            "Alguien susurró tu nombre.",
            "El suelo no tiene fondo.",
            "Reconoces este lugar, pero no recuerdas haberlo visto.",
        ]

    def resize_dialog(self, e=None):
        if hasattr(self, "dialogue_box"):
            self.dialogue_box.width = self.page.window.width - 60
            self.page.update()

    async def type_text(self, text):
        self.dialogue_text.value = ""
        self.page.update()
        current = ""
        for char in text:
            current += char
            self.dialogue_text.value = current
            self.page.update()
            if char in [".", ","]:
                await asyncio.sleep(0.08)
            else:
                await asyncio.sleep(0.02)

    # EXPLORAR SUEÑO
    async def explore_animation(self):
        self.explore_button.disabled = True
        self.page.update()
        await self.type_text(random.choice(self.dream_messages))
        self.controller.add_nostalgia(1)
        self.controller.add_fear(1)
        self.explore_button.disabled = False
        self.page.update()

    def explore_dream(self, e):
        self.page.run_task(self.explore_animation)

    # BUILD
    def build(self):

        # FONDO
        bg = ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/sueñopuerta.jpeg",
                fit="cover",
            ),
        )

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
                "Sueño",
                size=22,
                color="#FFFFFF",
                font_family="btninicio",
            ),
        )

        # CAJA DIÁLOGO
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
                    self.dialogue_text,
                    ft.Container(expand=True),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#BEBEBE", size=34)
                        ],
                    ),
                ],
            ),
        )

        # BOTÓN EXPLORAR
        self.explore_button = ft.ElevatedButton(
            content=ft.Text("Explorar", font_family="btninicio", size=18),
            width=220,
            height=52,
            on_click=self.explore_dream,
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
                        controls=[self.explore_button],
                        wrap=True,
                        spacing=15,
                    ),
                ],
            ),
        )

        # TEXTO INICIAL
        async def initial_text():
            await asyncio.sleep(0.5)
            await self.type_text(
                "No estás seguro de estar dormido.\n"
                "Todo se siente demasiado real.\n"
                "O quizás demasiado extraño."
            )

        self.page.run_task(initial_text)
        self.page.on_resize = self.resize_dialog

        # LAYOUT
        return ft.Stack(
            expand=True,
            controls=[
                # FONDO
                bg,
                # OVERLAY
                ft.Container(expand=True, bgcolor="#00000099"),
                # UI
                bottom_ui,
                # MUTE — CAMBIO: 2025
                make_mute_button(self.page),
            ],
        )
