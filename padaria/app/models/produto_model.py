from app.db import DatabaseConnection

class Produto:
    def __init__(self, nome, subtitulo, imagem_url, preco, estoque, categoria_id, usuario_id, id=None, categoria_nome=None):
        self.id = id
        self.nome = nome
        self.subtitulo = subtitulo
        self.imagem_url = imagem_url
        self.preco = preco
        self.estoque = estoque
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id
        self.categoria_nome = categoria_nome

    def salvar(self):
        with DatabaseConnection() as db:
            sql = """
                INSERT INTO produtos (nome, subtitulo, imagem_url, preco, estoque, categoria_id, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            db.cursor.execute(sql, (self.nome, self.subtitulo, self.imagem_url, self.preco, self.estoque, self.categoria_id, self.usuario_id))
            self.id = db.cursor.lastrowid
            return self.id

    def atualizar(self):
        with DatabaseConnection() as db:
            sql = """
                UPDATE produtos
                SET nome = ?, subtitulo = ?, imagem_url = ?, preco = ?, estoque = ?, categoria_id = ?
                WHERE id = ? AND usuario_id = ?
            """
            db.cursor.execute(sql, (self.nome, self.subtitulo, self.imagem_url, self.preco, self.estoque, self.categoria_id, self.id, self.usuario_id))
            return db.cursor.rowcount > 0

    @classmethod
    def listar_todos(cls, busca=None):
        """Lista todos os produtos cadastrados para a vitrine da página inicial."""
        with DatabaseConnection() as db:
            if busca:
                sql = """
                    SELECT p.*, c.nome AS categoria_nome
                    FROM produtos p
                    JOIN categorias c ON p.categoria_id = c.id
                    WHERE p.nome LIKE ?
                    ORDER BY p.id DESC
                """
                db.cursor.execute(sql, (f'%{busca}%',))
            else:
                sql = """
                    SELECT p.*, c.nome AS categoria_nome
                    FROM produtos p
                    JOIN categorias c ON p.categoria_id = c.id
                    ORDER BY p.id DESC
                """
                db.cursor.execute(sql)
            rows = db.cursor.fetchall()
            return [
                cls(
                    id=r['id'],
                    nome=r['nome'],
                    subtitulo=r['subtitulo'],
                    imagem_url=r['imagem_url'],
                    preco=r['preco'],
                    estoque=r['estoque'],
                    categoria_id=r['categoria_id'],
                    usuario_id=r['usuario_id'],
                    categoria_nome=r['categoria_nome']
                ) for r in rows
            ]

    @classmethod
    def listar_por_usuario(cls, usuario_id, busca=None):
        with DatabaseConnection() as db:
            if busca:
                sql = """
                    SELECT p.*, c.nome AS categoria_nome
                    FROM produtos p
                    JOIN categorias c ON p.categoria_id = c.id
                    WHERE p.usuario_id = ? AND p.nome LIKE ?
                    ORDER BY p.nome
                """
                db.cursor.execute(sql, (usuario_id, f'%{busca}%'))
            else:
                sql = """
                    SELECT p.*, c.nome AS categoria_nome
                    FROM produtos p
                    JOIN categorias c ON p.categoria_id = c.id
                    WHERE p.usuario_id = ?
                    ORDER BY p.nome
                """
                db.cursor.execute(sql, (usuario_id,))
            rows = db.cursor.fetchall()
            return [
                cls(
                    id=r['id'],
                    nome=r['nome'],
                    subtitulo=r['subtitulo'],
                    imagem_url=r['imagem_url'],
                    preco=r['preco'],
                    estoque=r['estoque'],
                    categoria_id=r['categoria_id'],
                    usuario_id=r['usuario_id'],
                    categoria_nome=r['categoria_nome']
                ) for r in rows
            ]

    @classmethod
    def buscar_por_id(cls, produto_id, usuario_id):
        with DatabaseConnection() as db:
            sql = "SELECT * FROM produtos WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (produto_id, usuario_id))
            r = db.cursor.fetchone()
            if r:
                return cls(
                    id=r['id'],
                    nome=r['nome'],
                    subtitulo=r['subtitulo'],
                    imagem_url=r['imagem_url'],
                    preco=r['preco'],
                    estoque=r['estoque'],
                    categoria_id=r['categoria_id'],
                    usuario_id=r['usuario_id']
                )
            return None

    @classmethod
    def excluir(cls, produto_id, usuario_id):
        with DatabaseConnection() as db:
            sql = "DELETE FROM produtos WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (produto_id, usuario_id))
            return db.cursor.rowcount > 0
    
    @classmethod
    def buscar_publico_por_id(cls, produto_id):
        with DatabaseConnection() as db:
            sql = "SELECT * FROM produtos WHERE id = ?"
            db.cursor.execute(sql, (produto_id,))
            r = db.cursor.fetchone()
            if r:
                return cls(
                    id=r['id'],
                    nome=r['nome'],
                    subtitulo=r['subtitulo'],
                    imagem_url=r['imagem_url'],
                    preco=r['preco'],
                    estoque=r['estoque'],
                    categoria_id=r['categoria_id'],
                    usuario_id=r['usuario_id']
                )
            return None
        
    @classmethod
    def baixar_estoque(cls, produto_id, quantidade):
        """Desconta a quantidade comprada garantindo que o estoque nunca fique negativo."""
        with DatabaseConnection() as db:
            sql = """
                UPDATE produtos
                SET estoque = estoque - ?
                WHERE id = ? AND estoque >= ?
            """
            db.cursor.execute(sql, (quantidade, produto_id, quantidade))
            return db.cursor.rowcount > 0