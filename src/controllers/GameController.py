import flet as ft


class GameController:

    def __init__(self, page: ft.Page, user_id: int = None):

        self.page = page
        self.user_id = user_id

        self.player_data = {
            "fear": 0,
            "nostalgia": 0,
            "identity": 100,
            "curiosity": 0,
            "current_scene": "intro",
            "mirror_state": "normal",
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
            cursor.execute("""
                INSERT INTO game_progress (user_id, current_scene, fear, nostalgia, identity_level, curiosity, mirror_state)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    current_scene = VALUES(current_scene),
                    fear = VALUES(fear),
                    nostalgia = VALUES(nostalgia),
                    identity_level = VALUES(identity_level),
                    curiosity = VALUES(curiosity),
                    mirror_state = VALUES(mirror_state),
                    last_save = CURRENT_TIMESTAMP
            """, (
                self.user_id,
                self.player_data["current_scene"],
                self.player_data["fear"],
                self.player_data["nostalgia"],
                self.player_data["identity"],
                self.player_data["curiosity"],
                self.player_data["mirror_state"],
            ))
            conn.commit()
        except Exception as e:
            print(f"Error al guardar progreso: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def load_progress(self):
        if not self.user_id:
            return False
        from database.connection import get_connection
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM game_progress WHERE user_id = %s ORDER BY last_save DESC LIMIT 1", (self.user_id,))
            row = cursor.fetchone()
            if row:
                self.player_data["current_scene"] = row["current_scene"]
                self.player_data["fear"]           = row["fear"]
                self.player_data["nostalgia"]      = row["nostalgia"]
                self.player_data["identity"]       = row["identity_level"]
                self.player_data["curiosity"]      = row["curiosity"]
                self.player_data["mirror_state"]   = row["mirror_state"]
                return True
            return False
        except Exception as e:
            print(f"Error al cargar progreso: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    # OBTENER DATOS
    def get_player_data(self):
        return self.player_data

    # REINICIAR JUEGO
    def reset_game(self):
        self.player_data = {
            "fear": 0,
            "nostalgia": 0,
            "identity": 100,
            "curiosity": 0,
            "current_scene": "intro",
            "mirror_state": "normal",
        }
        self.start_intro()
