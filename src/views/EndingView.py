import flet as ft
from views.audio_utils import make_mute_button

class EndingView:

    def __init__(self, page: ft.Page, controller, ending_type):

        self.page = page
        self.controller = controller
        self.ending_type = ending_type

    # REINICIAR
    def restart_game(self, e):

        self.controller.reset_game()

    def resize_dialog(self, e=None):
        if hasattr(self, "dialogue_box"):
            self.dialogue_box.width = self.page.window.width - 60
            self.page.update()

    # OBTENER FINAL
    def get_ending_text(self):

        endings = {

            "neutral":
            "¿Donde estoy?\n\n¿Que fue todo esto?",

            "mirror":
            "El reflejo ocupó tu lugar.\n\nY tú ya no estás aquí.",

            "dream":
            "Nunca despertaste realmente.",

            "acceptance":
            "Finalmente reconociste tu propio rostro.",
        }

        return endings.get(
            self.ending_type,
            endings["neutral"]
        )

    # UI
    def build(self):

        ending_text = ft.Text(
            self.get_ending_text(),
            size=30,
            text_align=ft.TextAlign.CENTER,
            color="#050505",
            font_family="contenido",
            weight=ft.FontWeight.W_500,
        )

        name_box = ft.Container(
            padding=ft.Padding(20, 10, 20, 10),
            bgcolor="#000000AA",
            border_radius=12,
            content=ft.Text(
                "Final",
                size=22,
                color="#FFFFFF",
                font_family="btninicio",
            ),
        )

        self.dialogue_box = ft.Container(
            width=self.page.window.width - 60,
            padding=ft.Padding(30, 30, 30, 30),
            bgcolor="#000000CC",
            border_radius=22,
            border=ft.border.Border(
                top=ft.BorderSide(1, "#3A3A3A"),
                bottom=ft.BorderSide(1, "#3A3A3A"),
                left=ft.BorderSide(1, "#3A3A3A"),
                right=ft.BorderSide(1, "#3A3A3A"),
            ),
            content=ft.Column(
                controls=[
                    ending_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        restart_button = ft.ElevatedButton(
            content=ft.Text("Volver a empezar", font_family="btninicio", size=18),
            width=260,
            height=52,
            on_click=self.restart_game,
            color="#FFFFFF",
            bgcolor="#1A1A1AAA",
        )

        content = ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                name_box,
                ft.Container(height=20),
                self.dialogue_box,
                ft.Container(height=30),
                restart_button,
            ],
        )

        self.page.on_resize = self.resize_dialog

        return ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="img/fin1.jpeg",
                        fit="cover",
                    ),
                ),
                ft.Container(expand=True, bgcolor="#00000066"),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0.25),
                    content=content,
                ),
                make_mute_button(self.page),
            ],
        )
