import flet as ft


class ContinueView:
    def __init__(self, page: ft.Page, controller, saves):
        self.page = page
        self.controller = controller
        self.saves = saves or []

    def back_to_menu(self, e):
        from views.MenuView import MenuView

        self.page.controls.clear()
        self.page.add(MenuView(self.page, user={"id": self.controller.user_id}).build())
        self.page.update()

    def load_save(self, e, save_id):
        if self.controller.load_progress(save_id):
            self.controller.resume_game()
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("No se pudo cargar la partida seleccionada."),
                bgcolor="#660000",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def rename_save(self, e, save_id, field: ft.TextField):
        new_name = field.value.strip()
        if not new_name:
            new_name = field.placeholder or "Partida guardada"
            field.value = new_name
        self.controller.update_save_name(save_id, new_name)
        self.page.snack_bar = ft.SnackBar(
            ft.Text("Nombre de partida actualizado."),
            bgcolor="#004400",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def start_new_game(self, e):
        self.controller.reset_game()

    def build(self):
        title = ft.Text(
            "Selecciona una partida",
            size=34,
            weight=ft.FontWeight.BOLD,
            color="#EAEAEA",
            font_family="titulo",
            text_align=ft.TextAlign.CENTER,
        )

        description = ft.Text(
            "Elige el archivo más reciente o modifica el nombre antes de cargar.",
            size=14,
            color="#AAAAAA",
            text_align=ft.TextAlign.CENTER,
            font_family="subtitulo",
        )

        save_items = []
        def close_dialog():
            if self.page.dialog is not None:
                self.page.dialog.open = False
                self.page.dialog = None
                self.page.update()

        def do_delete(sid):
            ok = self.controller.delete_save(sid)
            close_dialog()
            new_saves = self.controller.list_saves()
            self.page.controls.clear()
            self.page.add(ContinueView(self.page, self.controller, new_saves).build())
            if ok:
                self.page.snack_bar = ft.SnackBar(ft.Text("Partida eliminada."), bgcolor="#004400")
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("No se pudo eliminar la partida."), bgcolor="#660000")
            self.page.snack_bar.open = True
            self.page.update()

        def show_delete_dialog(sid):
            def confirm_delete(e):
                do_delete(sid)

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Eliminar partida"),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color="#AAAAAA",
                            icon_size=18,
                            tooltip="Cerrar",
                            on_click=lambda e: close_dialog(),
                        ),
                    ],
                ),
                content=ft.Text("¿Estás seguro? Esta acción no se puede deshacer."),
                actions=[
                    ft.TextButton(content=ft.Text("Cancelar"), on_click=lambda e: close_dialog()),
                    ft.ElevatedButton(content=ft.Text("Eliminar"), on_click=confirm_delete),
                ],
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
        if self.saves:
            for save in self.saves:
                save_name = save.get("save_name") or str(save.get("last_save"))[:16]
                save_field = ft.TextField(
                    value=save_name,
                    label="Nombre de la partida",
                    width=360,
                    color="#EAEAEA",
                    bgcolor="#14141455",
                    border_color="#3A3A3A",
                    on_submit=lambda e, sid=save["id"], field=None: self.rename_save(e, sid, field),
                )
                
                save_field.on_submit = lambda e, sid=save["id"], field=save_field: self.rename_save(e, sid, field)

                save_items.append(
                    ft.Container(
                        padding=ft.Padding(16, 16, 16, 16),
                        bgcolor="#000000AA",
                        border_radius=10,
                        border=ft.border.Border.all(1, "#333333"),
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            str(save.get("last_save"))[:16],
                                            size=12,
                                            color="#FF00FF",
                                        ),
                                        ft.Text(
                                            f"Escena: {save.get('current_scene')}",
                                            size=12,
                                            color="#AAAAAA",
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Container(height=10),
                                save_field,
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            content=ft.Text("Cargar", font_family="btninicio"),
                                            style=ft.ButtonStyle(
                                                color="#EAEAEA",
                                                bgcolor="#440044",
                                                overlay_color="#880088",
                                                side=ft.BorderSide(1, "#660066"),
                                            ),
                                            on_click=lambda e, sid=save["id"]: self.load_save(e, sid),
                                        ),
                                        ft.TextButton(
                                            content=ft.Text("Renombrar", color="#AAAAAA"),
                                            on_click=lambda e, sid=save["id"], field=save_field: self.rename_save(e, sid, field),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="#FF6666",
                                            tooltip="Eliminar partida",
                                            on_click=lambda e, sid=save["id"]: show_delete_dialog(sid),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ],
                            spacing=10,
                        ),
                    )
                )
        else:
            save_items.append(
                ft.Text(
                    "No hay partidas guardadas todavía.",
                    size=14,
                    color="#777777",
                    italic=True,
                )
            )

        load_buttons = ft.Column(
            controls=[
                ft.ElevatedButton(
                    content=ft.Text("Iniciar nueva partida", font_family="btninicio"),
                    width=240,
                    height=48,
                    style=ft.ButtonStyle(
                        color="#EAEAEA",
                        bgcolor="#220022",
                        overlay_color="#550055",
                        side=ft.BorderSide(1, "#330033"),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=self.start_new_game,
                ),
                ft.TextButton(
                    content=ft.Text("← Volver al menú", color="#AAAAAA"),
                    on_click=self.back_to_menu,
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        content = ft.Column(
            controls=[
                title,
                description,
                ft.Container(height=20),
                load_buttons,
                ft.Container(height=20),
                ft.Divider(color="#333333"),
                *save_items,
            ],
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                width=640,
                padding=40,
                bgcolor="#000000CC",
                border_radius=15,
                content=content,
            ),
        )
