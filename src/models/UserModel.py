import bcrypt
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database.connection import get_connection

GMAIL_USER = "noestoyaqui.soporte@gmail.com"
GMAIL_PASS = "lype iimh oyej oovt"


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


def login_user(email, password):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            return False, "No existe una cuenta con ese correo."
        if bcrypt.checkpw(password.encode(), user["password"].encode()):
            return True, user
        return False, "Contraseña incorrecta."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def send_reset_email(email):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            return False, "No existe una cuenta con ese correo."

        token = secrets.token_hex(4).upper()
        hashed_token = bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()

        cursor.execute("""
            UPDATE users SET reset_token = %s, reset_token_expiry = DATE_ADD(NOW(), INTERVAL 15 MINUTE)
            WHERE email = %s
        """, (hashed_token, email))
        conn.commit()

        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = email
        msg["Subject"] = "No Estoy Aquí — Código de recuperación"
        body = f"""
Hola,

Recibimos una solicitud para cambiar tu contraseña.

Tu código de verificación es:

    {token}

Este código expira en 15 minutos.
Si no fuiste tú, ignora este mensaje.

— No Estoy Aquí
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, email, msg.as_string())

        return True, "Código enviado a tu correo."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def verify_token_and_reset(email, token, new_password):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT reset_token FROM users
            WHERE email = %s AND reset_token_expiry > NOW()
        """, (email,))
        user = cursor.fetchone()
        if not user or not user["reset_token"]:
            return False, "Código inválido o expirado."
        if not bcrypt.checkpw(token.upper().encode(), user["reset_token"].encode()):
            return False, "Código incorrecto."

        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        cursor.execute("""
            UPDATE users SET password = %s, reset_token = NULL, reset_token_expiry = NULL
            WHERE email = %s
        """, (hashed, email))
        conn.commit()
        return True, "Contraseña actualizada correctamente."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
