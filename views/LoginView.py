import flet as ft
from models.UserModel import register_user, login_user


class AuthView:
    def __init__(self, page: ft.Page):
        self.page = page

    # VOLVER AL MENÚ
    def back_to_menu(self, e):
        from views.MenuView import MenuView
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user=None).build())
        self.page.update()

    def _enter_game(self, user):
        from views.MenuView import MenuView
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user=user).build())
        self.page.update()

    # LOGIN
    def login(self, e, username, password, feedback):
        ok, result = login_user(username.value, password.value)
        if ok:
            self._enter_game(result)
        else:
            feedback.color = "#FF4444"
            feedback.value = result
            self.page.update()

    def register(self, e, username, email, password, feedback):
        if not username.value or not email.value or not password.value:
            feedback.color = "#FF4444"
            feedback.value = "Completa todos los campos."
            self.page.update()
            return
        ok, result = register_user(username.value, email.value, password.value)
        if ok:
            self._enter_game(result)
        else:
            feedback.color = "#FF4444"
            feedback.value = result
            self.page.update()

    # UI PRINCIPAL
    def build(self):

        # TITULO
        title = ft.Text(
            "¿Quién eres?",
            size=38,
            color="#F2F2F2",
            weight=ft.FontWeight.BOLD,
            font_family="titulo",
            text_align=ft.TextAlign.CENTER,
        )

        subtitle = ft.Text(
            "El espejo todavía intenta recordarte.",
            size=15,
            italic=True,
            color="#B8B8B8",
            font_family="subtitulo",
            text_align=ft.TextAlign.CENTER,
        )

        # INPUTS
        username = ft.TextField(
            label="Nombre de usuario",
            width=350,
            border_color="#3A3A3A",
            focused_border_color="#AA00FF",
            color="white",
            label_style=ft.TextStyle(color="#AAAAAA"),
            cursor_color="#FF00FF",
            bgcolor="#11111199",
        )

        email = ft.TextField(
            label="Correo electrónico",
            width=350,
            border_color="#3A3A3A",
            focused_border_color="#AA00FF",
            color="white",
            label_style=ft.TextStyle(color="#AAAAAA"),
            cursor_color="#FF00FF",
            bgcolor="#11111199",
        )

        password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=350,
            border_color="#3A3A3A",
            focused_border_color="#AA00FF",
            color="white",
            label_style=ft.TextStyle(color="#AAAAAA"),
            cursor_color="#FF00FF",
            bgcolor="#11111199",
        )

        # ESTILO BOTONES
        button_style = ft.ButtonStyle(
            color="#EAEAEA",
            bgcolor="#141414AA",
            overlay_color="#552255",
            side=ft.BorderSide(1, "#444444"),
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=20,
        )

        # BOTONES
        feedback = ft.Text(
            "",
            size=13,
            text_align=ft.TextAlign.CENTER,
        )

        login_button = ft.ElevatedButton(
            content=ft.Text("Iniciar sesión"),
            width=350,
            height=50,
            style=button_style,
            on_click=lambda e: self.login(e, username, password, feedback),
        )

        register_button = ft.ElevatedButton(
            content=ft.Text("Registrarse"),
            width=350,
            height=50,
            style=button_style,
            on_click=lambda e: self.register(e, username, email, password, feedback),
        )

        forgot_btn = ft.TextButton(
            content=ft.Text("¿Olvidaste tu contraseña?", color="#777777", size=12),
            on_click=lambda e: [
                self.page.controls.clear(),
                self.page.add(__import__('views.ForgotPasswordView', fromlist=['ForgotPasswordView']).ForgotPasswordView(self.page).build()),
                self.page.update()
            ],
        )

        back_button = ft.TextButton(
            content=ft.Text("← Volver"),
            on_click=self.back_to_menu,
            style=ft.ButtonStyle(
                color="#999999",
            ),
        )

        # MENSAJE ATMOSFÉRICO
        ghost_message = ft.Text(
            "A veces los recuerdos no son tuyos.",
            size=13,
            italic=True,
            color="#777777",
            font_family="subtitulo",
            text_align=ft.TextAlign.CENTER,
        )

        # CONTENIDO CENTRAL
        content = ft.Column(
            controls=[
                title,
                subtitle,
                ft.Container(height=20),
                username,
                email,
                password,
                ft.Container(height=10),
                login_button,
                register_button,
                ft.Container(height=5),
                feedback,
                ft.Container(height=10),
                forgot_btn,
                ghost_message,
                back_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        # LAYOUT FINAL
        return ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/pantallaInicio.jpg",
                fit="cover",
                opacity=0.25,
            ),
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                width=500,
                padding=40,
                border_radius=15,
                bgcolor="#000000CC",
                shadow=ft.BoxShadow(
                    blur_radius=30,
                    spread_radius=1,
                    color="#000000",
                ),
                content=content,
            ),
        )