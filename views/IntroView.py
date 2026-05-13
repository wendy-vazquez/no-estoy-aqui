# views/intro_view.py

import flet as ft
import time
import threading


class IntroView:

    def __init__(self, page: ft.Page, controller):

        self.page = page
        self.controller = controller

    # =================================================
    # CONTINUAR
    # =================================================

    def continue_game(self, e):

        self.controller.go_to_room()

    # =================================================
    # EFECTO TEXTO
    # =================================================

    def animate_text(self):

        full_text = (
            "Despiertas.\n\n"
            "La habitación está silenciosa.\n\n"
            "No recuerdas haberte dormido.\n\n"
            "Pero algo...\n"
            "se siente diferente."
        )

        current_text = ""

        for char in full_text:

            current_text += char

            self.story_text.value = current_text

            self.page.update()

            time.sleep(0.03)

    # =================================================
    # UI
    # =================================================

    def build(self):

        # -------------------------
        # TEXTO PRINCIPAL
        # -------------------------

        self.story_text = ft.Text(
            "",
            size=24,
            color="#EAEAEA",
            text_align=ft.TextAlign.CENTER,
            font_family="subtitulo",
        )

        # -------------------------
        # BOTÓN
        # -------------------------

        continue_button = ft.ElevatedButton(
            content=ft.Text("Continuar"),
            width=220,
            height=50,
            on_click=self.continue_game,
        )

        # -------------------------
        # CONTENIDO
        # -------------------------

        content = ft.Column(
            controls=[
                self.story_text,
                ft.Container(height=40),
                continue_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # -------------------------
        # ANIMACIÓN TEXTO
        # -------------------------

        threading.Thread(
            target=self.animate_text,
            daemon=True,
        ).start()

        # -------------------------
        # LAYOUT
        # -------------------------

        return ft.Container(
            expand=True,
            bgcolor="#000000",
            alignment=ft.Alignment(0, 0),
            content=content,
        )