from werkzeug.security import generate_password_hash, check_password_hash
from app.db import DatabaseConnection

class Usuario:
    def __init__(self, username, senha_hash=None, is_admin=0, id=None):
        self.id = id
        self.username = username
        self.senha_hash = senha_hash
        self.is_admin = is_admin

    def definir_senha(self, senha_plana):
        self.senha_hash = generate_password_hash(senha_plana)

    def verificar_senha(self, senha_plana):
        return check_password_hash(self.senha_hash, senha_plana)

    def salvar(self):
        with DatabaseConnection() as db:
            sql = "INSERT INTO usuarios (username, senha_hash, is_admin) VALUES (?, ?, ?)"
            db.cursor.execute(sql, (self.username, self.senha_hash, self.is_admin))
            self.id = db.cursor.lastrowid
            return self.id

    @classmethod
    def buscar_por_username(cls, username):
        with DatabaseConnection() as db:
            sql = "SELECT id, username, senha_hash, is_admin FROM usuarios WHERE LOWER(username) = LOWER(?)"
            db.cursor.execute(sql, (username.strip(),))
            row = db.cursor.fetchone()
            if row:
                return cls(id=row['id'], username=row['username'], senha_hash=row['senha_hash'], is_admin=row['is_admin'])
            return None

    @classmethod
    def buscar_por_id(cls, user_id):
        with DatabaseConnection() as db:
            sql = "SELECT id, username, senha_hash, is_admin FROM usuarios WHERE id = ?"
            db.cursor.execute(sql, (user_id,))
            row = db.cursor.fetchone()
            if row:
                return cls(id=row['id'], username=row['username'], senha_hash=row['senha_hash'], is_admin=row['is_admin'])
            return None