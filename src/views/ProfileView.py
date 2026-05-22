import flet as ft
from database.connection import get_connection


def get_user_profile(user_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT username, email, created_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM game_progress WHERE user_id = %s ORDER BY last_save DESC LIMIT 1", (user_id,))
        progress = cursor.fetchone()

        cursor.execute("SELECT ending_name, unlocked_at FROM endings WHERE user_id = %s ORDER BY unlocked_at DESC", (user_id,))
        endings = cursor.fetchall()

        cursor.execute("SELECT dream_name, dream_description, discovered_at FROM dream_logs WHERE user_id = %s ORDER BY discovered_at DESC LIMIT 5", (user_id,))
        dreams = cursor.fetchall()

        return user, progress, endings, dreams
    except Exception as e:
        print(f"Error al cargar perfil: {e}")
        return None, None, [], []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


class ProfileView:

    def __init__(self, page: ft.Page, user):
        self.page = page
        self.user = user

    def logout(self, e):
        from views.MenuView import MenuView
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user=None).build())
        self.page.update()

    def back_to_menu(self, e):
        from views.MenuView import MenuView
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user=self.user).build())
        self.page.update()

    def build(self):
        user, progress, endings, dreams = get_user_profile(self.user["id"])

        def section_title(text):
            return ft.Text(text, size=18, color="#FF00FF", weight=ft.FontWeight.BOLD, font_family="titulo")

        def info_row(label, value):
            return ft.Row(
                controls=[
                    ft.Text(f"{label}:", size=13, color="#AAAAAA", width=160),
                    ft.Text(str(value), size=13, color="#EAEAEA"),
                ],
            )

        # INFO CUENTA
        account_section = ft.Column(
            controls=[
                section_title("Cuenta"),
                info_row("Usuario", user["username"] if user else "-"),
                info_row("Correo", user["email"] if user else "-"),
                info_row("Miembro desde", str(user["created_at"])[:10] if user else "-"),
            ],
            spacing=8,
        )

        # PROGRESO
        if progress:
            progress_section = ft.Column(
                controls=[
                    ft.Container(height=10),
                    section_title("Progreso actual"),
                    info_row("Escena actual", progress["current_scene"]),
                    info_row("Nostalgia", progress["nostalgia"]),
                    info_row("Curiosidad", progress["curiosity"]),
                    info_row("Nivel de identidad", progress["identity_level"]),
                    info_row("Estado del espejo", progress["mirror_state"]),
                    info_row("Ultimo guardado", str(progress["last_save"])[:16]),
                ],
                spacing=8,
            )
        else:
            progress_section = ft.Column(
                controls=[
                    ft.Container(height=10),
                    section_title("Progreso actual"),
                    ft.Text("Sin partida guardada.", size=13, color="#777777", italic=True),
                ],
                spacing=8,
            )

        # FINALES
        if endings:
            ending_rows = [info_row(e["ending_name"], str(e["unlocked_at"])[:10]) for e in endings]
        else:
            ending_rows = [ft.Text("Ningún final desbloqueado aún.", size=13, color="#777777", italic=True)]

        endings_section = ft.Column(
            controls=[
                ft.Container(height=10),
                section_title("Finales conseguidos"),
                *ending_rows,
            ],
            spacing=8,
        )

        # SUEÑOS
        if dreams:
            dream_rows = [
                ft.Column(
                    controls=[
                        ft.Text(d["dream_name"], size=13, color="#EAEAEA", weight=ft.FontWeight.BOLD),
                        ft.Text(d["dream_description"], size=12, color="#AAAAAA", italic=True),
                    ],
                    spacing=2,
                )
                for d in dreams
            ]
        else:
            dream_rows = [ft.Text("Ningún sueño registrado aún.", size=13, color="#777777", italic=True)]

        dreams_section = ft.Column(
            controls=[
                ft.Container(height=10),
                section_title("Sueños recientes"),
                *dream_rows,
            ],
            spacing=8,
        )

        # BOTONES
        back_btn = ft.TextButton(
            content=ft.Text("← Volver al menú", color="#AAAAAA"),
            on_click=self.back_to_menu,
        )

        logout_btn = ft.ElevatedButton(
            content=ft.Text("Cerrar sesión"),
            width=250,
            height=45,
            style=ft.ButtonStyle(
                color="#EAEAEA",
                bgcolor="#440000AA",
                overlay_color="#880000",
                side=ft.BorderSide(1, "#660000"),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self.logout,
        )

        content = ft.Column(
            controls=[
                ft.Text("Perfil", size=34, color="#EAEAEA", font_family="titulo", text_align=ft.TextAlign.CENTER),
                ft.Divider(color="#333333"),
                account_section,
                progress_section,
                endings_section,
                dreams_section,
                ft.Container(height=10),
                ft.Divider(color="#333333"),
                logout_btn,
                back_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Container(
            expand=True,
            bgcolor="#000000",
            image=ft.DecorationImage(
                src="img/pantallaInicio.jpg",
                fit="cover",
                opacity=0.2,
            ),
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                width=520,
                padding=40,
                bgcolor="#000000CC",
                border_radius=15,
                content=content,
            ),
        )
