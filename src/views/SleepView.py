import flet as ft
import random
import asyncio
from views.audio_utils import make_mute_button

class SleepView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        # CAMBIO: 2025 — contador de hundidas; tras 3 muestra mensaje final y solo deja despertar
        self.sink_count = 0

        self.sleep_messages = [
            "Cierras los ojos y el cuarto desaparece.",
            "Algo te arrastra hacia abajo.",
            "Escuchas tu nombre desde muy lejos.",
            "La oscuridad es cálida.",
            "No recuerdas haber cerrado los ojos.",
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

    # HUNDIRSE MÁS EN EL SUEÑO
    async def sink_animation(self):
        self.sink_count += 1
        self.sink_button.disabled = True
        self.bg_image.image = ft.DecorationImage(
            src="img/seguircaida.jpeg",
            fit="cover",
        )
        self.page.update()

        if self.sink_count >= 3:
            await self.type_text("Ya no hay nada más.")
            self.sink_button.visible = False
        else:
            await self.type_text(random.choice(self.sleep_messages))
            self.sink_button.disabled = False

        self.controller.add_nostalgia(2)
        self.controller.reduce_identity(1)
        self.wake_button.visible = True
        self.page.update()

    def sink_deeper(self, e):
        self.page.run_task(self.sink_animation)

    # DESPERTAR — regresa a la habitación
    def wake_up(self, e):
        self.controller.go_to_room()

    # BUILD
    def build(self):

        # FONDO
        self.bg_image = ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/caida1.jpeg",
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
                "Durmiendo...",
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

        # BOTÓN HUNDIRSE
        self.sink_button = ft.ElevatedButton(
            content=ft.Text("Hundirse más", font_family="btninicio", size=18),
            width=240,
            height=52,
            on_click=self.sink_deeper,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        # BOTÓN DESPERTAR — oculto hasta que el jugador se hunda al menos una vez
        self.wake_button = ft.ElevatedButton(
            content=ft.Text("Despertar", font_family="btninicio", size=18),
            width=220,
            height=52,
            visible=False,
            on_click=self.wake_up,
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
                        controls=[self.sink_button, self.wake_button],
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
                "Te recuestas.\n"
                "Los ojos se cierran solos.\n"
                "El cuarto se disuelve a tu alrededor."
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
                ft.Container(expand=True, bgcolor="#000000AA"),
                # UI
                bottom_ui,
                # MUTE — CAMBIO: 2025
                make_mute_button(self.page),
            ],
        )
