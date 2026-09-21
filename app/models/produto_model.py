import json
import os

# Pega o diretório 'app' subindo um nível a partir de 'app/models'
BASE_APP_DIR = os.path.dirname(os.path.dirname(__file__))
CAMINHO_JSON_PRODUTOS = os.path.join(BASE_APP_DIR, 'data', 'json', 'produtos.json')


class ProdutoModel:
    @staticmethod
    def listar_todos():
        if not os.path.exists(CAMINHO_JSON_PRODUTOS):
            return []
        with open(CAMINHO_JSON_PRODUTOS, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def _salvar(produtos):
        pasta = os.path.dirname(CAMINHO_JSON_PRODUTOS)
        os.makedirs(pasta, exist_ok=True)
        with open(CAMINHO_JSON_PRODUTOS, 'w', encoding='utf-8') as f:
            json.dump(produtos, f, ensure_ascii=False, indent=2)

    @classmethod
    def adicionar(cls, nome):
        produtos = cls.listar_todos()
        novo_id = max([p['id'] for p in produtos], default=0) + 1
        produtos.append({"id": novo_id, "nome": nome, "disponivel": True})
        cls._salvar(produtos)

    @classmethod
    def alternar_disponibilidade(cls, produto_id):
        produtos = cls.listar_todos()
        for p in produtos:
            if p['id'] == produto_id:
                p['disponivel'] = not p['disponivel']
                break
        cls._salvar(produtos)

    @classmethod
    def remover(cls, produto_id):
        produtos = cls.listar_todos()
        produtos = [p for p in produtos if p['id'] != produto_id]
        cls._salvar(produtos)