from app.db import DatabaseConnection
from app.models.usuario_model import Usuario
from app.models.categoria_model import Categoria
from app.models.produto_model import Produto

def inicializar_banco():
    with DatabaseConnection() as db:
        # Tabela de Usuários com nível de acesso (is_admin: 1 = Padeiro, 0 = Cliente)
        db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
            )
        ''')

        # Tabela de Categorias
        db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
        ''')

        # Tabela de Produtos (com subtítulo curto e URL da foto)
        db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                subtitulo TEXT NOT NULL,
                imagem_url TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
        ''')

    # Criar usuário Padeiro (Administrador) se não existir
    if not Usuario.buscar_por_username('padeiro'):
        admin = Usuario(username='padeiro', is_admin=1)
        admin.definir_senha('123456')
        admin_id = admin.salvar()

        # Dados iniciais para a vitrine não começar vazia
        cat_paes = Categoria(nome='Pães Artesanais', usuario_id=admin_id)
        cat_id = cat_paes.salvar()

        prod1 = Produto(
            nome='Pão Francês Crocante',
            subtitulo='Fornada quentinha a cada hora com casca dourada e miolo macio.',
            imagem_url='https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?w=500&q=80',
            preco=0.85,
            estoque=120,
            categoria_id=cat_id,
            usuario_id=admin_id
        )
        prod1.salvar()

        prod2 = Produto(
            nome='Croissant Amanteigado',
            subtitulo='Massa folhada francesa tradicional feita com manteiga pura.',
            imagem_url='https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500&q=80',
            preco=8.50,
            estoque=35,
            categoria_id=cat_id,
            usuario_id=admin_id
        )
        prod2.salvar()

        print("Banco inicializado! Padeiro (Admin): padeiro | Senha: 123456")
    else:
        print("Banco de dados já estava inicializado.")

if __name__ == '__main__':
    inicializar_banco()