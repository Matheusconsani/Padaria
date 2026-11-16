import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.utils.auth_middleware import admin_required
from app.models.categoria_model import Categoria
from app.models.produto_model import Produto
from app.models.pedido_model import Pedido

padaria_bp = Blueprint('padaria', __name__)

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def salvar_imagem_upload(arquivo):
    """Salva o arquivo enviado em app/static/img/ e retorna o caminho relativo."""
    if not arquivo or arquivo.filename == '':
        return None
    
    extensao = arquivo.filename.rsplit('.', 1)[-1].lower() if '.' in arquivo.filename else ''
    if extensao not in EXTENSOES_PERMITIDAS:
        return 'INVALIDA'

    nome_seguro = secure_filename(arquivo.filename)
    nome_unico = f"{uuid.uuid4().hex[:8]}_{nome_seguro}"
    pasta_destino = os.path.join(current_app.static_folder, 'img')
    os.makedirs(pasta_destino, exist_ok=True)
    
    caminho_completo = os.path.join(pasta_destino, nome_unico)
    arquivo.save(caminho_completo)
    
    return f"img/{nome_unico}"

# ================= PÁGINA INICIAL (VITRINE) =================

@padaria_bp.route('/')
def index():
    busca = request.args.get('busca', '').strip()
    produtos_vitrine = Produto.listar_todos(busca=busca if busca else None)
    return render_template('index.html', produtos=produtos_vitrine, busca=busca)

# ================= ENTIDADE 1: CATEGORIAS (APENAS PADEIRO) =================

@padaria_bp.route('/categorias', methods=['GET', 'POST'])
@admin_required
def categorias():
    user_id = session['user_id']

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        if not nome or len(nome) < 2:
            flash('O nome da categoria deve ter pelo menos 2 caracteres.', 'danger')
        else:
            nova_cat = Categoria(nome=nome, usuario_id=user_id)
            nova_cat.salvar()
            current_app.logger.info(f"Categoria '{nome}' criada pelo padeiro ID {user_id}")
            flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('padaria.categorias'))

    lista_categorias = Categoria.listar_por_usuario(user_id)
    return render_template('categorias.html', categorias=lista_categorias)

@padaria_bp.route('/categorias/<int:id>/editar', methods=['POST'])
@admin_required
def editar_categoria(id):
    user_id = session['user_id']
    nome = request.form.get('nome', '').strip()

    if not nome or len(nome) < 2:
        flash('Nome inválido para atualização.', 'danger')
        return redirect(url_for('padaria.categorias'))

    cat = Categoria.buscar_por_id(id, user_id)
    if cat:
        cat.nome = nome
        cat.atualizar()
        current_app.logger.info(f"Categoria ID {id} atualizada")
        flash('Categoria atualizada!', 'success')
    else:
        flash('Categoria não encontrada ou acesso negado.', 'danger')

    return redirect(url_for('padaria.categorias'))

@padaria_bp.route('/categorias/<int:id>/excluir', methods=['POST'])
@admin_required
def excluir_categoria(id):
    user_id = session['user_id']
    if Categoria.excluir(id, user_id):
        current_app.logger.info(f"Categoria ID {id} excluída")
        flash('Categoria excluída com sucesso!', 'info')
    else:
        flash('Não foi possível excluir a categoria.', 'danger')
    return redirect(url_for('padaria.categorias'))

# ================= ENTIDADE 2: PRODUTOS (APENAS PADEIRO) =================

@padaria_bp.route('/produtos', methods=['GET', 'POST'])
@admin_required
def produtos():
    user_id = session['user_id']

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        subtitulo = request.form.get('subtitulo', '').strip()
        imagem_url = request.form.get('imagem_url', '').strip()
        arquivo_foto = request.files.get('imagem_arquivo')
        preco_str = request.form.get('preco', '').replace(',', '.').strip()
        estoque_str = request.form.get('estoque', '').strip()
        categoria_id_str = request.form.get('categoria_id', '').strip()

        caminho_upload = salvar_imagem_upload(arquivo_foto)
        if caminho_upload == 'INVALIDA':
            flash('Formato de imagem inválido! Use PNG, JPG, JPEG ou WEBP.', 'danger')
            return redirect(url_for('padaria.produtos'))

        imagem_final = caminho_upload if caminho_upload else imagem_url

        if not nome or not subtitulo or not imagem_final or not preco_str or not estoque_str or not categoria_id_str:
            flash('Preencha todos os campos e envie uma foto (arquivo ou URL).', 'danger')
            return redirect(url_for('padaria.produtos'))

        if len(subtitulo) > 120:
            flash('O subtítulo deve ter no máximo 120 caracteres.', 'warning')
            return redirect(url_for('padaria.produtos'))

        try:
            preco = float(preco_str)
            estoque = int(estoque_str)
            categoria_id = int(categoria_id_str)
            if preco < 0 or estoque < 0:
                raise ValueError()
        except ValueError:
            flash('Preço e estoque devem ser números válidos e positivos.', 'danger')
            return redirect(url_for('padaria.produtos'))

        if not Categoria.buscar_por_id(categoria_id, user_id):
            flash('Categoria selecionada inválida.', 'danger')
            return redirect(url_for('padaria.produtos'))

        novo_produto = Produto(
            nome=nome,
            subtitulo=subtitulo,
            imagem_url=imagem_final,
            preco=preco,
            estoque=estoque,
            categoria_id=categoria_id,
            usuario_id=user_id
        )
        novo_produto.salvar()
        current_app.logger.info(f"Produto '{nome}' cadastrado pelo padeiro ID {user_id}")
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('padaria.produtos'))

    busca = request.args.get('busca', '').strip()
    lista_produtos = Produto.listar_por_usuario(user_id, busca=busca if busca else None)
    lista_categorias = Categoria.listar_por_usuario(user_id)
    return render_template('produtos.html', produtos=lista_produtos, categorias=lista_categorias, busca=busca)

@padaria_bp.route('/produtos/<int:id>/editar', methods=['POST'])
@admin_required
def editar_produto(id):
    user_id = session['user_id']
    produto = Produto.buscar_por_id(id, user_id)

    if not produto:
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('padaria.produtos'))

    nome = request.form.get('nome', '').strip()
    subtitulo = request.form.get('subtitulo', '').strip()
    imagem_url = request.form.get('imagem_url', '').strip()
    arquivo_foto = request.files.get('imagem_arquivo')

    caminho_upload = salvar_imagem_upload(arquivo_foto)
    if caminho_upload == 'INVALIDA':
        flash('Formato de imagem inválido! Use PNG, JPG, JPEG ou WEBP.', 'danger')
        return redirect(url_for('padaria.produtos'))

    imagem_final = caminho_upload if caminho_upload else (imagem_url or produto.imagem_url)

    try:
        preco = float(request.form.get('preco', '').replace(',', '.'))
        estoque = int(request.form.get('estoque', ''))
        categoria_id = int(request.form.get('categoria_id', ''))
        if not nome or not subtitulo or not imagem_final or preco < 0 or estoque < 0:
            raise ValueError()
    except ValueError:
        flash('Dados inválidos na edição do produto.', 'danger')
        return redirect(url_for('padaria.produtos'))

    if not Categoria.buscar_por_id(categoria_id, user_id):
        flash('Categoria inválida.', 'danger')
        return redirect(url_for('padaria.produtos'))

    produto.nome = nome
    produto.subtitulo = subtitulo
    produto.imagem_url = imagem_final
    produto.preco = preco
    produto.estoque = estoque
    produto.categoria_id = categoria_id
    produto.atualizar()

    current_app.logger.info(f"Produto ID {id} atualizado")
    flash('Produto atualizado com sucesso!', 'success')
    return redirect(url_for('padaria.produtos'))

@padaria_bp.route('/produtos/<int:id>/excluir', methods=['POST'])
@admin_required
def excluir_produto(id):
    user_id = session['user_id']
    if Produto.excluir(id, user_id):
        current_app.logger.info(f"Produto ID {id} excluído")
        flash('Produto removido!', 'info')
    else:
        flash('Erro ao remover produto.', 'danger')
    return redirect(url_for('padaria.produtos'))

# ================= CARRINHO DE COMPRAS (SESSION + JSON) =================

@padaria_bp.route('/carrinho/adicionar/<int:id>', methods=['POST'])
def adicionar_carrinho(id):
    if not session.get('user_id'):
        flash('Crie uma conta ou faça login para adicionar produtos ao carrinho.', 'warning')
        return redirect(url_for('auth.cadastro'))

    produto = Produto.buscar_publico_por_id(id)
    if not produto:
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('padaria.index'))

    if produto.estoque <= 0:
        flash(f'"{produto.nome}" está esgotado no momento.', 'warning')
        return redirect(url_for('padaria.index'))

    carrinho = session.get('carrinho', [])
    item_encontrado = False

    for item in carrinho:
        if item['id'] == produto.id:
            if item['quantidade'] + 1 > produto.estoque:
                flash(f'Estoque máximo atingido! Temos apenas {produto.estoque} unidade(s) de "{produto.nome}".', 'warning')
                return redirect(url_for('padaria.index'))
            
            item['quantidade'] += 1
            item['subtotal'] = round(item['quantidade'] * item['preco'], 2)
            item_encontrado = True
            break

    if not item_encontrado:
        carrinho.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': float(produto.preco),
            'imagem_url': produto.imagem_url,
            'quantidade': 1,
            'subtotal': float(produto.preco)
        })

    session['carrinho'] = carrinho
    session.modified = True
    flash(f'"{produto.nome}" foi adicionado ao seu carrinho!', 'success')
    return redirect(url_for('padaria.index'))

@padaria_bp.route('/carrinho')
def ver_carrinho():
    if not session.get('user_id'):
        flash('Cadastre-se ou faça login para acessar seu carrinho.', 'warning')
        return redirect(url_for('auth.cadastro'))

    carrinho = session.get('carrinho', [])
    total = sum(item['subtotal'] for item in carrinho)
    return render_template('carrinho.html', carrinho=carrinho, total=total)

@padaria_bp.route('/carrinho/remover/<int:id>', methods=['POST'])
def remover_carrinho(id):
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))

    carrinho = session.get('carrinho', [])
    carrinho = [item for item in carrinho if item['id'] != id]
    session['carrinho'] = carrinho
    session.modified = True
    flash('Item removido do carrinho.', 'info')
    return redirect(url_for('padaria.ver_carrinho'))

@padaria_bp.route('/carrinho/pagar', methods=['POST'])
def finalizar_pedido():
    if not session.get('user_id'):
        return redirect(url_for('auth.cadastro'))

    carrinho = session.get('carrinho', [])
    if not carrinho:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('padaria.index'))

    nome_cliente = request.form.get('nome_cliente', '').strip()
    cpf = request.form.get('cpf', '').strip()
    telefone = request.form.get('telefone', '').strip()
    cep = request.form.get('cep', '').strip()
    endereco = request.form.get('endereco', '').strip()
    forma_pagamento = request.form.get('forma_pagamento', '').strip()

    if not all([nome_cliente, cpf, telefone, cep, endereco, forma_pagamento]):
        flash('Preencha todos os campos obrigatórios para concluir o pedido.', 'danger')
        return redirect(url_for('padaria.ver_carrinho'))

    for item in carrinho:
        produto_atual = Produto.buscar_publico_por_id(item['id'])
        if not produto_atual or produto_atual.estoque < item['quantidade']:
            disponivel = produto_atual.estoque if produto_atual else 0
            flash(f'Estoque insuficiente para "{item["nome"]}". Disponível: {disponivel} unidade(s). Ajuste seu carrinho.', 'danger')
            return redirect(url_for('padaria.ver_carrinho'))

    for item in carrinho:
        sucesso = Produto.baixar_estoque(item['id'], item['quantidade'])
        if not sucesso:
            flash(f'Não foi possível reservar "{item["nome"]}". Verifique o estoque.', 'danger')
            return redirect(url_for('padaria.ver_carrinho'))

    total = sum(item['subtotal'] for item in carrinho)

    pedido = Pedido(
        usuario_id=session['user_id'],
        username=session['username'],
        nome_cliente=nome_cliente,
        cpf=cpf,
        telefone=telefone,
        cep=cep,
        endereco=endereco,
        forma_pagamento=forma_pagamento,
        itens=carrinho,
        total=total
    )
    pedido_id = pedido.salvar_json()

    session['carrinho'] = []
    session.modified = True

    current_app.logger.info(f"Pedido #{pedido_id} finalizado pelo usuário {session['username']}")
    flash(f'Pedido #{pedido_id} realizado com sucesso! Já estamos preparando tudo para você.', 'success')
    return redirect(url_for('padaria.index'))

# ================= FILA DE PEDIDOS (APENAS PADEIRO) =================

@padaria_bp.route('/pedidos')
@admin_required
def listar_pedidos():
    pedidos = Pedido.listar_todos()
    return render_template('pedidos.html', pedidos=pedidos)