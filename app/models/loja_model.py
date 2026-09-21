import json
import os

# Pega o diretório 'app' subindo um nível a partir de 'app/models'
BASE_APP_DIR = os.path.dirname(os.path.dirname(__file__))
CAMINHO_JSON_CONFIG = os.path.join(BASE_APP_DIR, 'data', 'json', 'config.json')


class LojaModel:
    @staticmethod
    def esta_aberta():
        if not os.path.exists(CAMINHO_JSON_CONFIG):
            return True
        with open(CAMINHO_JSON_CONFIG, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('loja_aberta', True)

    @classmethod
    def alternar_status_loja(cls):
        status_atual = cls.esta_aberta()
        pasta = os.path.dirname(CAMINHO_JSON_CONFIG)
        os.makedirs(pasta, exist_ok=True)
        with open(CAMINHO_JSON_CONFIG, 'w', encoding='utf-8') as f:
            json.dump({"loja_aberta": not status_atual}, f, indent=2)