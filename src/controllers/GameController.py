import datetime
import flet as ft
import traceback


class GameController:

    def __init__(self, page: ft.Page, user_id: int = None):

        self.page = page
        self.user_id = user_id
        self.save_id = None

        self.player_data = {
            "fear": 0,
            "nostalgia": 0,
            "identity": 100,
            "curiosity": 0,
            "current_scene": "intro",
            "mirror_state": "normal",
            "save_name": None,
        }

    # NAVEGACIÓN
    def _go_to_menu(self, e):
        self.save_progress()
        from views.MenuView import MenuView
        from models.UserModel import login_user
        self.page.controls.clear()
        self.page.add(MenuView(self.page, user={"id": self.user_id}).build())
        self.page.update()

    def _navigate(self, view):
        home_btn = ft.Container(
            top=10,
            left=10,
            content=ft.IconButton(
                icon=ft.Icons.HOME,
                icon_color="#AAAAAA",
                icon_size=22,
                tooltip="Volver al menú",
                on_click=self._go_to_menu,
            ),
        )
        self.page.controls.clear()
        self.page.add(
            ft.Stack(
                expand=True,
                controls=[
                    view.build(),
                    home_btn,
                ],
            )
        )
        self.page.update()

    def start_intro(self):
        from views.IntroView import IntroView
        self.player_data["current_scene"] = "intro"
        self._navigate(IntroView(page=self.page, controller=self))

    def go_to_room(self):
        from views.RoomView import RoomView
        self.player_data["current_scene"] = "room"
        self._navigate(RoomView(page=self.page, controller=self))
        
    def go_to_hallways(self):
        from views.HallwaysView import HallwaysView
        self.player_data["current_scene"] = "hallways"
        self._navigate(HallwaysView(page=self.page, controller=self))

    def go_to_mirror(self):
        from views.MirrorView import MirrorView
        self.player_data["current_scene"] = "mirror"
        self._navigate(MirrorView(page=self.page, controller=self))

    def go_to_dream(self):
        from views.DreamView import DreamView
        self.player_data["current_scene"] = "dream"
        self._navigate(DreamView(page=self.page, controller=self))

    def go_to_ending(self, ending_type=None):
        from views.EndingView import EndingView
        self.player_data["current_scene"] = "ending"
        if ending_type is None:
            ending_type = self._calculate_ending()
        self._navigate(EndingView(page=self.page, controller=self, ending_type=ending_type))

    def resume_game(self):
        scene = self.player_data.get("current_scene", "intro")
        if scene == "room":
            self.go_to_room()
        elif scene == "hallways":
            self.go_to_hallways()
        elif scene == "mirror":
            self.go_to_mirror()
        elif scene == "dream":
            self.go_to_dream()
        elif scene == "ending":
            self.go_to_ending()
        else:
            self.start_intro()

    # LÓGICA DE FINALES
    def _calculate_ending(self):
        fear     = self.player_data["fear"]
        nostalgia = self.player_data["nostalgia"]
        identity  = self.player_data["identity"]
        curiosity = self.player_data["curiosity"]

        if identity <= 20:
            return "lost"
        if fear >= 10:
            return "fear"
        if nostalgia >= 10:
            return "nostalgia"
        if curiosity >= 10:
            return "curiosity"
        return "neutral"

    # SISTEMA EMOCIONAL
    def add_fear(self, amount=1):
        self.player_data["fear"] += amount

    def add_nostalgia(self, amount=1):
        self.player_data["nostalgia"] += amount

    def reduce_identity(self, amount=1):
        self.player_data["identity"] = max(0, self.player_data["identity"] - amount)

    def add_curiosity(self, amount=1):
        self.player_data["curiosity"] += amount

    def set_mirror_state(self, state):
        self.player_data["mirror_state"] = state

    # GUARDAR PROGRESO EN DB
    def save_progress(self):
        if not self.user_id:
            return
        from database.connection import get_connection
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            save_name = self.player_data.get("save_name")
            if not save_name:
                save_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                self.player_data["save_name"] = save_name

            if self.save_id:
                cursor.execute("""
                    UPDATE game_progress
                    SET current_scene = %s,
                        fear = %s,
                        nostalgia = %s,
                        identity_level = %s,
                        curiosity = %s,
                        mirror_state = %s,
                        save_name = %s,
                        last_save = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (
                    self.player_data["current_scene"],
                    self.player_data["fear"],
                    self.player_data["nostalgia"],
                    self.player_data["identity"],
                    self.player_data["curiosity"],
                    self.player_data["mirror_state"],
                    save_name,
                    self.save_id,
                ))
            else:
                cursor.execute("""
                    INSERT INTO game_progress (user_id, current_scene, fear, nostalgia, identity_level, curiosity, mirror_state, save_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.user_id,
                    self.player_data["current_scene"],
                    self.player_data["fear"],
                    self.player_data["nostalgia"],
                    self.player_data["identity"],
                    self.player_data["curiosity"],
                    self.player_data["mirror_state"],
                    save_name,
                ))
                self.save_id = cursor.lastrowid
            conn.commit()
        except Exception as e:
            print(f"Error al guardar progreso: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def load_progress(self, save_id=None):
        if not self.user_id:
            return False
        from database.connection import get_connection
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            if save_id:
                cursor.execute("SELECT * FROM game_progress WHERE id = %s AND user_id = %s", (save_id, self.user_id))
            else:
                cursor.execute("SELECT * FROM game_progress WHERE user_id = %s ORDER BY last_save DESC LIMIT 1", (self.user_id,))
            row = cursor.fetchone()
            if row:
                self.save_id = row["id"]
                self.player_data["current_scene"] = row["current_scene"]
                self.player_data["fear"]           = row["fear"]
                self.player_data["nostalgia"]      = row["nostalgia"]
                self.player_data["identity"]       = row["identity_level"]
                self.player_data["curiosity"]      = row["curiosity"]
                self.player_data["mirror_state"]   = row["mirror_state"]
                self.player_data["save_name"]      = row.get("save_name") or str(row["last_save"])[0:16]
                return True
            return False
        except Exception as e:
            print(f"Error al cargar progreso: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def list_saves(self):
        if not self.user_id:
            return []
        from database.connection import get_connection
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM game_progress WHERE user_id = %s ORDER BY last_save DESC", (self.user_id,))
            return cursor.fetchall() or []
        except Exception as e:
            print(f"Error al listar partidas guardadas: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def update_save_name(self, save_id, new_name):
        if not self.user_id:
            return
        from database.connection import get_connection
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE game_progress SET save_name = %s WHERE id = %s AND user_id = %s",
                (new_name, save_id, self.user_id),
            )
            conn.commit()
            if self.save_id == save_id:
                self.player_data["save_name"] = new_name
        except Exception as e:
            print(f"Error al actualizar nombre de guardado: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def delete_save(self, save_id):
        if not self.user_id or not save_id:
            return False
        from database.connection import get_connection
        conn = None
        cursor = None
        try:
            print(f"[DEBUG] delete_save called with save_id={save_id}, user_id={self.user_id}")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM game_progress WHERE id = %s AND user_id = %s", (save_id, self.user_id))
            affected = cursor.rowcount
            conn.commit()
            print(f"[DEBUG] delete_save affected rows: {affected}")
            # if we deleted the currently loaded save, clear local state
            if affected and self.save_id == save_id:
                self.save_id = None
                self.player_data["save_name"] = None
            return affected > 0
        except Exception as e:
            print(f"Error al eliminar guardado: {e}")
            traceback.print_exc()
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def set_save_name(self, name):
        self.player_data["save_name"] = name

    # OBTENER DATOS
    def get_player_data(self):
        return self.player_data

    # REINICIAR JUEGO
    def reset_game(self):
        self.save_id = None
        self.player_data = {
            "fear": 0,
            "nostalgia": 0,
            "identity": 100,
            "curiosity": 0,
            "current_scene": "intro",
            "mirror_state": "normal",
            "save_name": None,
        }
        self.start_intro()
