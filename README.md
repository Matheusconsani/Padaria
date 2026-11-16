# 🥖 La Boulangerie — Sistema Web de Gestão de Padaria

Aplicação web desenvolvida no padrão **MPA (Multi-Page Application)** utilizando **Python**, **Flask**, **Jinja2** e **SQLite3** puro (sem ORMs), seguindo rigorosamente a arquitetura **MVC (Model-View-Controller)** com rotas modularizadas em Blueprints[cite: 2, 3].

Projeto desenvolvido como trabalho final da disciplina **Laboratório de Programação 1 (SPOLBP1)** — Técnico em Desenvolvimento de Sistemas[cite: 2].

---

## ✨ Funcionalidades Principais

* **Autenticação e Níveis de Acesso:** Cadastro de clientes, login, logout e hash seguro de senhas com `werkzeug.security`[cite: 2]. Separação entre **Cliente** (acesso à vitrine e compras) e **Padeiro/Administrador** (gerenciamento completo do catálogo e pedidos).
* **Vitrine Pública e Busca:** Exibição responsiva dos produtos com foto (upload local ou URL externa), título, subtítulo descritivo, preço, disponibilidade em estoque e filtro de pesquisa por nome[cite: 2].
* **Gerenciamento de Categorias e Produtos (CRUD):** Criação, listagem, edição e exclusão protegidas por middleware (`@admin_required`), com relacionamento via chave estrangeira (`ON DELETE CASCADE`)[cite: 2, 4].
* **Carrinho de Compras e Checkout:** Armazenamento de itens na `session` do Flask, validação rigorosa de estoque (impedindo compras acima do disponível e descontando unidades automaticamente no SQLite) e registro dos pedidos finalizados em arquivo `.json` organizados por ordem de chegada[cite: 4].
* **Recursos de Servidor:** Uso de `DatabaseConnection` com gerenciador de contexto (`__enter__` e `__exit__`), queries SQL parametrizadas contra SQL Injection, mensagens `flash` categorizadas, cookie para alternância de tema (Claro/Escuro), logs (`app.logger`) e página personalizada para erro `404`[cite: 3, 4, 5].

---

## 📂 Estrutura do Projeto (MVC)

```text
padaria/
├── iniciar_bd.py               # Script de criação das tabelas SQLite e usuário inicial[cite: 3, 4]
├── banco_sistema.db            # Banco de dados SQLite gerado automaticamente[cite: 3]
├── run.py                      # Ponto de entrada da aplicação Flask[cite: 3]
├── requirements.txt            # Dependências do projeto[cite: 3]
├── README.md                   # Documentação do sistema[cite: 3]
└── app/
    ├── __init__.py             # Factory create_app(), secret_key, errorhandler 404 e Blueprints[cite: 3, 4, 5]
    ├── db.py                   # Classe DatabaseConnection (__enter__ e __exit__)[cite: 3]
    ├── data/
    │   └── pedidos.json        # Histórico de pedidos finalizados ordenados cronologicamente
    ├── models/                 # Camada Model (POO + SQL parametrizado)[cite: 2, 3]
    │   ├── usuario_model.py
    │   ├── categoria_model.py
    │   ├── produto_model.py
    │   └── pedido_model.py
    ├── controllers/            # Camada Controller (Blueprints, zero SQL)[cite: 2, 3]
    │   ├── auth_bp.py
    │   └── padaria_bp.py
    ├── utils/
    │   └── auth_middleware.py  # Decorators @login_required e @admin_required (objeto g)[cite: 3, 4]
    ├── views/                  # Camada View (Templates Jinja2 com herança)[cite: 2, 3]
    │   ├── base.html
    │   ├── index.html
    │   ├── login.html
    │   ├── cadastro_usuario.html
    │   ├── categorias.html
    │   ├── produtos.html
    │   ├── carrinho.html
    │   ├── pedidos.html
    │   └── 404.html
    └── static/                 # Arquivos estáticos (CSS modularizado e imagens)[cite: 3]
