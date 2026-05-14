import flet as ft
from models.UserModel import send_reset_email, verify_token_and_reset


class ForgotPasswordView:

    def __init__(self, page: ft.Page):
        self.page = page

    def back_to_login(self, e):
        from views.LoginView import AuthView
        self.page.controls.clear()
        self.page.add(AuthView(self.page).build())
        self.page.update()

    def build(self):

        feedback = ft.Text("", size=13, text_align=ft.TextAlign.CENTER)

        # -------------------------
        # PASO 1 — CORREO
        # -------------------------
        email_field = ft.TextField(
            label="Correo electrónico",
            width=350,
            border_color="#3A3A3A",
            focused_border_color="#AA00FF",
            color="white",
            label_style=ft.TextStyle(color="#AAAAAA"),
            cursor_color="#FF00FF",
            bgcolor="#11111199",
        )

        # -------------------------
        # PASO 2 — CÓDIGO + NUEVA CONTRASEÑA
        # -------------------------
        token_field = ft.TextField(
            label="Código de verificación",
            width=350,
            border_color="#3A3A3A",
            focused_border_color="#AA00FF",
            color="white",
            label_style=ft.TextStyle(color="#AAAAAA"),
            cursor_color="#FF00FF",
            bgcolor="#11111199",
            visible=False,
        )

        new_password_field = ft.TextField(
            label="Nueva contraseña",
            password=True,
            can_reveal_password=True,
            width=350,
            border_color="#3A3A3A",
            focused_border_color="#AA00FF",
            color="white",
            label_style=ft.TextStyle(color="#AAAAAA"),
            cursor_color="#FF00FF",
            bgcolor="#11111199",
            visible=False,
        )

        confirm_btn = ft.ElevatedButton(
            content=ft.Text("Cambiar contraseña"),
            width=350,
            height=50,
            visible=False,
            style=ft.ButtonStyle(
                color="#EAEAEA",
                bgcolor="#141414AA",
                overlay_color="#552255",
                side=ft.BorderSide(1, "#444444"),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        def send_code(e):
            ok, msg = send_reset_email(email_field.value)
            feedback.color = "#00FF88" if ok else "#FF4444"
            feedback.value = msg
            if ok:
                token_field.visible = True
                new_password_field.visible = True
                confirm_btn.visible = True
                send_btn.visible = False
            self.page.update()

        def change_password(e):
            if not token_field.value or not new_password_field.value:
                feedback.color = "#FF4444"
                feedback.value = "Completa todos los campos."
                self.page.update()
                return
            ok, msg = verify_token_and_reset(email_field.value, token_field.value, new_password_field.value)
            feedback.color = "#00FF88" if ok else "#FF4444"
            feedback.value = msg
            if ok:
                import time, threading
                def go_back():
                    time.sleep(2)
                    self.back_to_login(None)
                threading.Thread(target=go_back, daemon=True).start()
            self.page.update()

        confirm_btn.on_click = change_password

        send_btn = ft.ElevatedButton(
            content=ft.Text("Enviar código"),
            width=350,
            height=50,
            on_click=send_code,
            style=ft.ButtonStyle(
                color="#EAEAEA",
                bgcolor="#141414AA",
                overlay_color="#552255",
                side=ft.BorderSide(1, "#444444"),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        back_btn = ft.TextButton(
            content=ft.Text("← Volver al login", color="#999999"),
            on_click=self.back_to_login,
        )

        content = ft.Column(
            controls=[
                ft.Text("Recuperar contraseña", size=30, color="#EAEAEA", font_family="titulo", text_align=ft.TextAlign.CENTER),
                ft.Text("Ingresa tu correo y te enviaremos un código.", size=13, color="#AAAAAA", italic=True, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                email_field,
                token_field,
                new_password_field,
                ft.Container(height=5),
                send_btn,
                confirm_btn,
                feedback,
                ft.Container(height=5),
                back_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        return ft.Container(
            expand=True,
            bgcolor="#000000",
            image=ft.DecorationImage(
                src="img/pantallaInicio.jpg",
                fit="fitHeight",
                opacity=0.25,
            ),
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
