import bcrypt
from database.connection import get_connection


def register_user(username, email, password):
    conn = None
    cursor = None
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        conn.commit()
        return True, {"id": cursor.lastrowid, "username": username, "email": email}
    except Exception as e:
        error = str(e)
        if "username" in error:
            return False, "Ese nombre de usuario ya existe."
        elif "email" in error:
            return False, "Ese correo ya está registrado."
        return False, f"Error: {error}"
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def login_user(username, password):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return False, "Usuario no encontrado."
        if bcrypt.checkpw(password.encode(), user["password"].encode()):
            return True, user
        return False, "Contraseña incorrecta."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
