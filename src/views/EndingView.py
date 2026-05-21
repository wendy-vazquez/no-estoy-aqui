import flet as ft


class EndingView:

    def __init__(self, page: ft.Page, controller, ending_type):

        self.page = page
        self.controller = controller
        self.ending_type = ending_type

    # =================================================
    # REINICIAR
    # =================================================

    def restart_game(self, e):

        self.controller.reset_game()

    # =================================================
    # OBTENER FINAL
    # =================================================

    def get_ending_text(self):

        endings = {

            "neutral":
            "Despiertas.\n\nPero el espejo sigue ahí.",

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

    # =================================================
    # UI
    # =================================================

    def build(self):

        ending_text = ft.Text(
            self.get_ending_text(),
            size=28,
            text_align=ft.TextAlign.CENTER,
            color="#F0F0F0",
            font_family="subtitulo",
        )

        restart_button = ft.ElevatedButton(
            content=ft.Text("Volver a empezar"),
            width=250,
            height=50,
            on_click=self.restart_game,
        )

        content = ft.Column(
            controls=[
                ending_text,
                ft.Container(height=40),
                restart_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            expand=True,
            bgcolor="#000000",
            alignment=ft.Alignment(0, 0),
            content=content,
        )