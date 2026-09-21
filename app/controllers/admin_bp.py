from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.produto_model import ProdutoModel
from app.models.usuario_model import UsuarioModel
from app.models.loja_model import LojaModel

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 🔴 Se o usuário já estiver logado, redireciona direto para o painel
    if session.get('logado'):
        return redirect(url_for('admin.painel'))

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        if UsuarioModel.validar_login(usuario, senha):
            session.permanent = True  # Validade de 3 horas
            session['logado'] = True
            return redirect(url_for('admin.painel'))
        
        return "Usuário ou senha incorretos."

    return render_template('login.html')

@admin_bp.route('/painel')
def painel():
    produtos = ProdutoModel.listar_todos()
    loja_aberta = LojaModel.esta_aberta()
    return render_template('admin.html', produtos=produtos, loja_aberta=loja_aberta)

@admin_bp.route('/loja/toggle', methods=['POST'])
def alternar_loja():
    LojaModel.alternar_status_loja()
    return redirect(url_for('admin.painel'))

@admin_bp.route('/produto/adicionar', methods=['POST'])
def adicionar_produto():
    nome = request.form.get('nome')
    if nome:
        ProdutoModel.adicionar(nome)
    return redirect(url_for('admin.painel'))

@admin_bp.route('/produto/status/<int:produto_id>', methods=['POST'])
def alternar_status(produto_id):
    ProdutoModel.alternar_disponibilidade(produto_id)
    return redirect(url_for('admin.painel'))

@admin_bp.route('/produto/remover/<int:produto_id>', methods=['POST'])
def remover_produto(produto_id):
    ProdutoModel.remover(produto_id)
    return redirect(url_for('admin.painel'))

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))