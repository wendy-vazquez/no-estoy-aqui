import flet as ft
import asyncio
from views.audio_utils import make_mute_button

# CAMBIO: 2025 — escenario completo del pasillo con narrativa, fases y navegación
# CAMBIO: 2025 — botón mute agregado


class HallwaysView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

        # FASES DEL PASILLO
        # phase controla el avance narrativo:
        #   0 → texto inicial, botones: "Avanzar" y "Escuchar"
        #   1 → tras avanzar, aparece algo al fondo
        #   2 → tras escuchar, se revela una puerta
        self.phase = 0

    # ACCIONES
    def go_to_room(self, e):
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

    # FASE 1 — avanzar por el pasillo
    async def advance_animation(self):
        self.phase = 1
        self.advance_button.disabled = True
        self.page.update()
        await self.type_text(
            "Das un paso.\n"
            "El suelo cruje bajo tus pies.\n"
            "Al fondo del pasillo hay una silueta inmóvil."
        )
        self.controller.add_fear(3)
        self.controller.add_curiosity(2)
        # Mostrar botón de puerta
        self.door_button.visible = True
        self.page.update()

    def advance_hallway(self, e):
        self.page.run_task(self.advance_animation)

    # FASE 2 — escuchar el pasillo
    # CAMBIO: 2025 — al escuchar cambia el fondo a puertas1.jpeg
    async def listen_animation(self):
        self.phase = 2
        self.listen_button.disabled = True
        self.bg_image.image = ft.DecorationImage(
            src="img/puerta1.jpeg",
            fit="cover",
        )
        self.page.update()
        await self.type_text(
            "Silencio.\n"
            "Luego un susurro: tu nombre.\n"
            "Una puerta al costado está entreabierta."
        )
        self.controller.add_nostalgia(2)
        self.controller.reduce_identity(1)
        self.door_button.visible = True
        self.page.update()

    def listen_hallway(self, e):
        self.page.run_task(self.listen_animation)

    # FASE 3 — entrar por la puerta (va al sueño)
    def enter_door(self, e):
        self.controller.go_to_dream()

    # BUILD
    def build(self):

        # FONDO
        self.bg_image = ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/pasillos.jpeg",
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
                "Pasillo",
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

        # BOTÓN AVANZAR
        self.advance_button = ft.ElevatedButton(
            content=ft.Text("Avanzar", font_family="btninicio", size=18),
            width=220,
            height=52,
            on_click=self.advance_hallway,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        # BOTÓN ESCUCHAR
        self.listen_button = ft.ElevatedButton(
            content=ft.Text("Escuchar", font_family="btninicio", size=18),
            width=220,
            height=52,
            on_click=self.listen_hallway,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        # BOTÓN PUERTA — oculto hasta que avance o escuche
        self.door_button = ft.ElevatedButton(
            content=ft.Text("Entrar por la puerta", font_family="btninicio", size=18),
            width=280,
            height=52,
            visible=False,
            on_click=self.enter_door,
            color="#FFFFFF",
            bgcolor="#1A003AAA",
        )

        # BOTÓN VOLVER
        back_button = ft.ElevatedButton(
            content=ft.Text("Volver", font_family="btninicio", size=18),
            width=180,
            height=52,
            on_click=self.go_to_room,
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
                            self.advance_button,
                            self.listen_button,
                            self.door_button,
                            back_button,
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
                "El pasillo se extiende ante ti.\n"
                "Las paredes parecen respirar.\n"
                "Unas voces salen de las puertas."
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
