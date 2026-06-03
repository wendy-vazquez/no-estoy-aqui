import flet as ft
import pygame

def make_mute_button(page: ft.Page) -> ft.Container:
    """Devuelve un Container posicionado con el botón de mute listo para usar en un Stack."""

    btn = ft.IconButton(
        icon=ft.Icons.VOLUME_UP,
        icon_color="#EAEAEA",
        icon_size=20,
        tooltip="Silenciar música",
    )

    def toggle(e):
        try:
            if pygame.mixer.music.get_volume() > 0:
                pygame.mixer.music.set_volume(0)
                btn.icon = ft.Icons.VOLUME_OFF
            else:
                pygame.mixer.music.set_volume(0.5)
                btn.icon = ft.Icons.VOLUME_UP
            page.update()
        except Exception:
            pass  # pygame no inicializado, ignorar

    btn.on_click = toggle

    return ft.Container(right=10, top=10, content=btn)
