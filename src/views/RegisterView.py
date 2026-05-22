import flet as ft
from models.UserModel import register_user


class RegisterView:

    def __init__(self, page: ft.Page):
        self.page = page

    def go_to_login(self, e):
        from views.LoginView import AuthView
        self.page.controls.clear()
        self.page.add(AuthView(self.page).build())
        self.page.update()

    def _enter_game(self, user):
        from views.MenuView import MenuView
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user=user).build())
        self.page.update()

    def register(self, e, username, email, password, confirm, feedback):
        if not username.value or not email.value or not password.value:
            feedback.color = "#FF4444"
            feedback.value = "Completa todos los campos."
            self.page.update()
            return
        if password.value != confirm.value:
            feedback.color = "#FF4444"
            feedback.value = "Las contraseñas no coinciden."
            self.page.update()
            return
        ok, result = register_user(username.value, email.value, password.value)
        if ok:
            self._enter_game(result)
        else:
            feedback.color = "#FF4444"
            feedback.value = result
            self.page.update()

    def build(self):

        title = ft.Text(
            "Crear cuenta",
            size=38,
            color="#F2F2F2",
            weight=ft.FontWeight.BOLD,
            font_family="titulo",
            text_align=ft.TextAlign.CENTER,
        )

        subtitle = ft.Text(
            "El espejo necesita saber tu nombre.",
            size=15,
            italic=True,
            color="#B8B8B8",
            font_family="subtitulo",
            text_align=ft.TextAlign.CENTER,
        )

        field_style = dict(
            width=350,
            border_color="#3A3A3A",
            focused_border_color="#AA00FF",
            color="white",
            label_style=ft.TextStyle(color="#AAAAAA"),
            cursor_color="#FF00FF",
            bgcolor="#11111199",
        )

        username = ft.TextField(label="Nombre de usuario", **field_style)
        email = ft.TextField(label="Correo electrónico", **field_style)
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, **field_style)
        confirm = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, **field_style)

        feedback = ft.Text("", size=13, text_align=ft.TextAlign.CENTER)

        button_style = ft.ButtonStyle(
            color="#EAEAEA",
            bgcolor="#141414AA",
            overlay_color="#552255",
            side=ft.BorderSide(1, "#444444"),
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=20,
        )

        register_button = ft.ElevatedButton(
            content=ft.Text("Registrarse"),
            width=350,
            height=50,
            style=button_style,
            on_click=lambda e: self.register(e, username, email, password, confirm, feedback),
        )

        content = ft.Column(
            controls=[
                title,
                subtitle,
                ft.Container(height=20),
                username,
                email,
                password,
                confirm,
                ft.Container(height=5),
                register_button,
                feedback,
                ft.Container(height=5),
                ft.TextButton(
                    content=ft.Text("¿Ya tienes cuenta? Inicia sesión", color="#AA00FF", size=12),
                    on_click=self.go_to_login,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        return ft.Container(
            expand=True,
            image=ft.DecorationImage(
                src="img/pantallaInicio.jpg",
                fit="cover",
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
