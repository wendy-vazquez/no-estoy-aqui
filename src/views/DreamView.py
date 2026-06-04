import flet as ft
import random
import asyncio
from views.audio_utils import make_mute_button

# CAMBIO: 2025 — DreamView rediseñada con estética unificada
# CAMBIO: 2025 — primera exploración → sueño1.jpeg
# CAMBIO: 2025 — segunda exploración → sueñomonstruo.jpeg + "te estube buscando" + botón huir
# CAMBIO: 2025 — fondo semitransparente en caja de diálogo y name_box


class DreamView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        # explore_count: 0=inicial, 1=primera exploración, 2+=segunda exploración
        self.explore_count = 0

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

    # HUIR — CAMBIO: 2025 — muestra "no hay salida" y va al final
    async def flee_animation(self):
        self.flee_button.disabled = True
        self.page.update()
        await self.type_text("No hay salida.")
        await asyncio.sleep(0.8)
        self.controller.go_to_ending()

    def flee(self, e):
        self.page.run_task(self.flee_animation)

    # EXPLORAR SUEÑO
    async def explore_animation(self):
        self.explore_count += 1
        self.explore_button.disabled = True

        if self.explore_count == 1:
            # PRIMERA EXPLORACIÓN → sueño1.jpeg
            self.bg_image.image = ft.DecorationImage(
                src="img/sueño1.jpeg",
                fit="cover",
            )
            self.page.update()
            await self.type_text(random.choice(self.dream_messages))
            self.controller.add_nostalgia(1)
            self.controller.add_fear(1)
            self.explore_button.disabled = False

        else:
            # SEGUNDA EXPLORACIÓN → sueñomonstruo.jpeg + mensaje + botón huir
            self.bg_image.image = ft.DecorationImage(
                src="img/sueñomonstruo.jpeg",
                fit="cover",
            )
            self.explore_button.visible = False
            self.flee_button.visible = True
            self.page.update()
            await self.type_text("Te estube buscando.")
            self.controller.add_fear(5)
            self.controller.reduce_identity(3)

        self.page.update()

    def explore_dream(self, e):
        self.page.run_task(self.explore_animation)

    # BUILD
    def build(self):

        # FONDO — guardado en self.bg_image para cambiarlo en explore_animation
        self.bg_image = ft.Container(
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

        # NOMBRE — CAMBIO: 2025 fondo semitransparente
        name_box = ft.Container(
            padding=ft.Padding(20, 10, 20, 10),
            bgcolor="#00000077",
            border_radius=12,
            content=ft.Text(
                "Sueño",
                size=22,
                color="#FFFFFF",
                font_family="btninicio",
            ),
        )

        # CAJA DIÁLOGO — CAMBIO: 2025 fondo semitransparente (#00000077 en lugar de #000000CC)
        self.dialogue_box = ft.Container(
            width=self.page.window.width - 60,
            height=260,
            padding=30,
            bgcolor="#00000077",
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

        # BOTÓN HUIR
        self.flee_button = ft.ElevatedButton(
            content=ft.Text("¡Huir!", font_family="btninicio", size=18),
            width=200,
            height=52,
            visible=False,
            on_click=self.flee,
            color="#FFFFFF",
            bgcolor="#3A0000AA",
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
                        controls=[self.explore_button, self.flee_button],
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
                self.bg_image,
                # OVERLAY
                ft.Container(expand=True, bgcolor="#00000066"),
                # UI
                bottom_ui,
                # MUTE
                make_mute_button(self.page),
            ],
        )
