import flet as ft
import random
import asyncio


class MirrorView:

    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

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

        random_message = random.choice(self.messages)

        await self.type_text(random_message)

        self.controller.add_fear(2)

        self.controller.reduce_identity(1)

    def stare_mirror(self, e):

        self.page.run_task(self.stare_animation)

    # BUILD
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
        stare_button = ft.ElevatedButton(
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

        back_button = ft.ElevatedButton(
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
                            stare_button,
                            back_button,
                        ],
                        wrap=True,
                        spacing=15,
                    )
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
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="img/espejo.jpg",
                        fit="cover",
                    ),
                ),

                # OVERLAY
                ft.Container(
                    expand=True,
                    bgcolor="#00000088",
                ),

                # UI
                bottom_ui,
            ],
        )