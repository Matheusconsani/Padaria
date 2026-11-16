from app.db import DatabaseConnection

class Categoria:
    def __init__(self, nome, usuario_id, id=None):
        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id

    def salvar(self):
        with DatabaseConnection() as db:
            sql = "INSERT INTO categorias (nome, usuario_id) VALUES (?, ?)"
            db.cursor.execute(sql, (self.nome, self.usuario_id))
            self.id = db.cursor.lastrowid
            return self.id

    def atualizar(self):
        with DatabaseConnection() as db:
            sql = "UPDATE categorias SET nome = ? WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (self.nome, self.id, self.usuario_id))
            return db.cursor.rowcount > 0

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        with DatabaseConnection() as db:
            sql = "SELECT id, nome, usuario_id FROM categorias WHERE usuario_id = ? ORDER BY nome"
            db.cursor.execute(sql, (usuario_id,))
            rows = db.cursor.fetchall()
            return [cls(id=r['id'], nome=r['nome'], usuario_id=r['usuario_id']) for r in rows]

    @classmethod
    def buscar_por_id(cls, categoria_id, usuario_id):
        with DatabaseConnection() as db:
            sql = "SELECT id, nome, usuario_id FROM categorias WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (categoria_id, usuario_id))
            r = db.cursor.fetchone()
            if r:
                return cls(id=r['id'], nome=r['nome'], usuario_id=r['usuario_id'])
            return None

    @classmethod
    def excluir(cls, categoria_id, usuario_id):
        with DatabaseConnection() as db:
            sql = "DELETE FROM categorias WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (categoria_id, usuario_id))
            return db.cursor.rowcount > 0