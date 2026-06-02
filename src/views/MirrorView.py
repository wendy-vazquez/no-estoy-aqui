import flet as ft
import random
import asyncio
from views.audio_utils import make_mute_button

# CAMBIO: 2025 — botón mute agregado en todas las vistas
# CAMBIO: 2025 — tras la segunda mirada solo aparece el botón "Correr" (va a HallwaysView)


class MirrorView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

        # ESTADO DE MIRADAS
        # stare_count controla cuántas veces el jugador ha mirado el espejo:
        #   0 → imagen inicial (espejo.jpg)
        #   1 → primera mirada (acercarse1.jpeg) — CAMBIO: 2025
        #   2+ → segunda mirada (monstruo1.jpeg) + solo botón "Correr" — CAMBIO: 2025
        self.stare_count = 0

        self.messages = [
            "El reflejo tardó demasiado en moverse.",
            "Tus ojos no parecen tuyos.",
            "El espejo respiró.",
            "Tu reflejo sonrió.",
            "Algo detrás de ti desapareció.",
            "Jurarias que el reflejo parpadeó antes que tú.",
            "Hay alguien más dentro del espejo.",
        ]

    # ACCIONES
    def return_room(self, e):
        self.controller.go_to_room()

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

    async def stare_animation(self):

        self.stare_count += 1

        # PRIMERA MIRADA → acercarse1.jpeg
        # CAMBIO: 2025 — al mirar por primera vez cambia el fondo a acercarse1.jpeg
        if self.stare_count == 1:
            self.bg_image.image = ft.DecorationImage(
                src="img/acercarse1.jpeg",
                fit="cover",
            )
            self.page.update()
            await self.type_text(random.choice(self.messages))
            self.controller.add_fear(2)
            self.controller.reduce_identity(1)

        # SEGUNDA MIRADA → monstruo1.jpeg + solo botón "Correr"
        # CAMBIO: 2025 — se ocultan stare y back, solo queda el botón de correr al pasillo
        else:
            self.bg_image.image = ft.DecorationImage(
                src="img/monstruo1.jpeg",
                fit="cover",
            )
            self.stare_button.visible = False
            self.back_button.visible = False
            self.hallway_button.visible = True
            self.page.update()
            await self.type_text(
                "Algo en el espejo no eres tú.\n"
                "Sus ojos te siguen.\n"
                "Tienes que correr."
            )
            self.controller.add_fear(5)
            self.controller.reduce_identity(3)

    def stare_mirror(self, e):
        self.page.run_task(self.stare_animation)

    # BUILD
    def build(self):

        # FONDO
        self.bg_image = ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/espejo.jpg",
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
                "Espejo",
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

        # BOTÓN CORRER AL PASILLO
        # CAMBIO: 2025 — oculto hasta la segunda mirada; reemplaza a stare y back
        self.hallway_button = ft.ElevatedButton(
            content=ft.Text(
                "¡Correr!",
                font_family="btninicio",
                size=18,
            ),
            width=200,
            height=52,
            visible=False,
            on_click=lambda e: self.controller.go_to_hallways(),
            color="#FFFFFF",
            bgcolor="#3A0000AA",
        )

        # BOTONES — guardados en self para poder ocultarlos en stare_animation
        self.stare_button = ft.ElevatedButton(
            content=ft.Text(
                "Mirar fijamente",
                font_family="btninicio",
                size=18,
            ),
            width=300,
            height=52,
            on_click=self.stare_mirror,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        self.back_button = ft.ElevatedButton(
            content=ft.Text(
                "Volver",
                font_family="btninicio",
                size=18,
            ),
            width=220,
            height=52,
            on_click=self.return_room,
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
                            self.stare_button,
                            self.back_button,
                            self.hallway_button,
                        ],
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
                "El espejo parece observarte.\n"
                "Tu reflejo está inmóvil.\n"
                "Sientes algo extraño en el pecho."
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
                ft.Container(expand=True, bgcolor="#00000088"),
                # UI
                bottom_ui,
                # MUTE — CAMBIO: 2025
                make_mute_button(self.page),
            ],
        )
