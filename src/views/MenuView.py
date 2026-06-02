import flet as ft
import pygame
import random
import threading
import time
import sys


class MenuView:
    def __init__(self, page: ft.Page, user=None):
        self.page = page
        self.user = user

    # BOTONES
    def start_game(self, e):
        from views.LoginView import AuthView
        self.page.controls.clear()
        self.page.add(AuthView(self.page).build())
        self.page.update()

    def continue_game(self, e):
        from controllers.GameController import GameController
        from views.ContinueView import ContinueView

        controller = GameController(page=self.page, user_id=self.user["id"])
        saves = controller.list_saves()
        self.page.controls.clear()
        self.page.add(ContinueView(self.page, controller, saves).build())
        self.page.update()

    def settings(self, e):
        from views.ProfileView import ProfileView
        self.page.controls.clear()
        self.page.add(ProfileView(self.page, user=self.user).build())
        self.page.update()

    def exit_game(self, e):
        pygame.mixer.music.stop()
        sys.exit()

    # UI PRINCIPAL
    def build(self):

        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/pianoAmbiental.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


        # TITULO
        title = ft.Text(
            "No EsToy AqUí",
            size=42,
            weight=ft.FontWeight.W_700,
            color="#EAEAEA",
            text_align=ft.TextAlign.CENTER,
            font_family="titulo",
            opacity=0,
            scale=ft.Scale(0.5),
            animate_opacity=ft.Animation(1000, "easeOut"),
            animate_scale=ft.Animation(1000, "easeOut"),
        )

        def animate_title():
            time.sleep(0.8)
            title.opacity = 1
            title.scale = ft.Scale(1)
            self.page.update()

        threading.Thread(target=animate_title, daemon=True).start()

        def color_loop():
            colors = ["#EAEAEA", "#CC0000", "#FF00FF", "#00FFFF"]
            i = 0
            while True:
                time.sleep(3)
                i = (i + 1) % 4
                title.color = colors[i]
                self.page.update()

        threading.Thread(target=color_loop, daemon=True).start()

        # SUBTITULO
        subtitle = ft.Container(
            content=ft.Text(
                "A veces el reflejo recuerda más que tú.",
                size=16,
                italic=True,
                color="#FF00FF",
                text_align=ft.TextAlign.CENTER,
                font_family="subtitulo",
            ),
            shadow=ft.BoxShadow(
                blur_radius=15,
                color="#000000",
                offset=ft.Offset(0, 0),
                spread_radius=8,
            ),
        )

        # MENSAJE FLOTANTE
        creepy_messages = [
            "¿Sigues aquí?",
            "Aún me recuerdas.",
            "No mires el espejo.",
            "Yo sí recuerdo.",
            "Algo cambió mientras dormías.",
            "No eres exactamente tú.",
            "¿Por qué regresaste?",
            "El reflejo no parpadeó.",
            "Nunca despertaste realmente.",
            "Te ves diferente hoy.",
            "...",
            "¿Te sientes diferente?",
            "¿Te miraste al espejo esta mañana?",
            "¿Escuchaste eso?",
            "No estás solo.",
            "El reflejo sonríe.",
            "¿Quién es ese detrás de ti?",
            "El reflejo no te sigue.",
            "¿Por qué el reflejo se ve triste?",
            "El reflejo parpadeó primero.",
        ]

        ghost_message = ft.Text(
            "",
            size=14,
            italic=True,
            color="#AAAAAA",
            opacity=0,
            animate_opacity=1200,
            text_align=ft.TextAlign.CENTER,
            font_family="subtitulo",
        )

        # MENSAJES RANDOM
        # CAMBIO: 2025 — se recorren en orden shuffle para que aparezcan todos sin repetir
        # Se fuerza opacity=0 antes de cambiar el texto para que Flet detecte el cambio y anime
        def random_messages():
            pool = creepy_messages[:]
            while True:
                random.shuffle(pool)
                for msg in pool:
                    time.sleep(random.randint(4, 8))
                    ghost_message.opacity = 0
                    self.page.update()
                    time.sleep(1.2)  # esperar que termine fade-out
                    ghost_message.value = msg
                    ghost_message.opacity = 1
                    self.page.update()
                    time.sleep(3)
                    ghost_message.opacity = 0
                    self.page.update()
                    time.sleep(1.2)  # esperar que termine fade-out antes del siguiente

        threading.Thread(target=random_messages, daemon=True).start()

        # ESTILO BOTONES
        button_style = ft.ButtonStyle(
            color="#EAEAEA",
            bgcolor="#14141455",
            overlay_color="#552255",
            side=ft.BorderSide(1, "#3A3A3A"),
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=20,
        )

        start_button = ft.ElevatedButton(
            content=ft.Text("Iniciar", font_family="btninicio"),
            width=250,
            height=50,
            style=button_style,
            on_click=self.start_game,
        )

        continue_button = ft.ElevatedButton(
            content=ft.Text("Continuar", font_family="btninicio"),
            width=250,
            height=50,
            style=button_style,
            on_click=self.continue_game,
        )

        settings_button = ft.ElevatedButton(
            content=ft.Text("Configuración", font_family="btninicio"),
            width=250,
            height=50,
            style=button_style,
            on_click=self.settings,
        )

        exit_button = ft.ElevatedButton(
            content=ft.Text("Salir", font_family="btninicio"),
            width=250,
            height=50,
            style=button_style,
            on_click=self.exit_game,
        )

        # BOTON MUTE
        mute_btn = ft.IconButton(
            icon=ft.Icons.VOLUME_UP,
            icon_color="#EAEAEA",
            icon_size=20,
            tooltip="Silenciar música",
            on_click=lambda e: toggle_mute(e),
        )

        def toggle_mute(e):
            if pygame.mixer.music.get_volume() > 0:
                pygame.mixer.music.set_volume(0)
                mute_btn.icon = ft.Icons.VOLUME_OFF
            else:
                pygame.mixer.music.set_volume(0.5)
                mute_btn.icon = ft.Icons.VOLUME_UP
            self.page.update()

        # BOTONES SEGUN SESION
        if self.user:
            buttons = [
                continue_button,
                settings_button,
                exit_button,
            ]
        else:
            buttons = [
                start_button,
                exit_button,
            ]

        # CONTENIDO CENTRAL
        content = ft.Column(
            controls=[
                title,
                subtitle,
                ft.Container(height=20),
                ghost_message,
                ft.Container(height=30),
                *buttons,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        # LAYOUT FINAL
        return ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/pantalla1.jpg",
                fit="fitHeight",
                opacity=0.75,
            ),
            alignment=ft.Alignment(0, 0),
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        alignment=ft.Alignment(0, 0),
                        expand=True,
                        content=content,
                    ),
                    ft.Container(
                        right=10,
                        top=10,
                        content=mute_btn,
                    ),
                ],
            ),
        )
