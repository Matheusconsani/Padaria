import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(BASE_DIR, 'data')
PEDIDOS_PATH = os.path.join(JSON_DIR, 'pedidos.json')

class Pedido:
    def __init__(self, usuario_id, username, nome_cliente, cpf, telefone, cep, endereco, forma_pagamento, itens, total):
        self.usuario_id = usuario_id
        self.username = username
        self.nome_cliente = nome_cliente
        self.cpf = cpf
        self.telefone = telefone
        self.cep = cep
        self.endereco = endereco
        self.forma_pagamento = forma_pagamento
        self.itens = itens
        self.total = round(total, 2)
        self.data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    def salvar_json(self):
        os.makedirs(JSON_DIR, exist_ok=True)
        pedidos_existentes = self.listar_todos()

        novo_id = max([p.get('pedido_id', 0) for p in pedidos_existentes], default=0) + 1

        novo_registro = {
            "pedido_id": novo_id,
            "data_hora": self.data_hora,
            "usuario_id": self.usuario_id,
            "username": self.username,
            "dados_cliente": {
                "nome_cliente": self.nome_cliente,
                "cpf": self.cpf,
                "telefone": self.telefone,
                "cep": self.cep,
                "endereco": self.endereco,
                "forma_pagamento": self.forma_pagamento
            },
            "itens": self.itens,
            "total": self.total
        }

        pedidos_existentes.append(novo_registro)

        with open(PEDIDOS_PATH, 'w', encoding='utf-8') as arquivo:
            json.dump(pedidos_existentes, arquivo, indent=4, ensure_ascii=False)

        return novo_id

    @staticmethod
    def listar_todos():
        if not os.path.exists(PEDIDOS_PATH):
            return []
        try:
            with open(PEDIDOS_PATH, 'r', encoding='utf-8') as arquivo:
                conteudo = json.load(arquivo)
                if not isinstance(conteudo, list):
                    return []
                # Ordena pelo pedido_id crescente (primeiro pedido feito aparece primeiro)
                return sorted(conteudo, key=lambda p: p.get('pedido_id', 0))
        except (json.JSONDecodeError, IOError):
            return []