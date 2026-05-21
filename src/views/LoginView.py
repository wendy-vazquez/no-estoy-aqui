import flet as ft
from models.UserModel import login_user


class AuthView:

    def __init__(self, page: ft.Page):
        self.page = page

    def back_to_menu(self, e):
        from views.MenuView import MenuView
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user=None).build())
        self.page.update()

    def go_to_register(self, e):
        from views.RegisterView import RegisterView
        self.page.controls.clear()
        self.page.add(RegisterView(self.page).build())
        self.page.update()

    def go_to_forgot(self, e):
        from views.ForgotPasswordView import ForgotPasswordView
        self.page.controls.clear()
        self.page.add(ForgotPasswordView(self.page).build())
        self.page.update()

    def _enter_game(self, user):
        from views.MenuView import MenuView
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user=user).build())
        self.page.update()

    def login(self, e, email, password, feedback):
        ok, result = login_user(email.value, password.value)
        if ok:
            self._enter_game(result)
        else:
            feedback.color = "#FF4444"
            feedback.value = result
            self.page.update()

    def build(self):

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

        feedback = ft.Text("", size=13, text_align=ft.TextAlign.CENTER)

        button_style = ft.ButtonStyle(
            color="#EAEAEA",
            bgcolor="#141414AA",
            overlay_color="#552255",
            side=ft.BorderSide(1, "#444444"),
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=20,
        )

        login_button = ft.ElevatedButton(
            content=ft.Text("Iniciar sesión"),
            width=350,
            height=50,
            style=button_style,
            on_click=lambda e: self.login(e, email, password, feedback),
        )

        content = ft.Column(
            controls=[
                title,
                subtitle,
                ft.Container(height=20),
                email,
                password,
                ft.Container(height=5),
                login_button,
                feedback,
                ft.Container(height=5),
                ft.TextButton(
                    content=ft.Text("¿Olvidaste tu contraseña?", color="#777777", size=12),
                    on_click=self.go_to_forgot,
                ),
                ft.TextButton(
                    content=ft.Text("¿No tienes cuenta? Regístrate", color="#AA00FF", size=12),
                    on_click=self.go_to_register,
                ),
                ft.TextButton(
                    content=ft.Text("← Volver al menú", color="#555555", size=12),
                    on_click=self.back_to_menu,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        return ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/pantallaInicio.jpg",
                fit="fitHeight",
                opacity=0.25,
            ),
            bgcolor="#000000",
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                width=500,
                padding=40,
                border_radius=15,
                bgcolor="#000000CC",
                shadow=ft.BoxShadow(blur_radius=30, spread_radius=1, color="#000000"),
                content=content,
            ),
        )
