from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response, current_app
from app.models.usuario_model import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        senha = request.form.get('senha', '').strip()

        if not username or not senha:
            flash('Preencha todos os campos.', 'danger')
            return render_template('login.html')

        usuario = Usuario.buscar_por_username(username)
        if usuario and usuario.verificar_senha(senha):
            session.clear()
            session['user_id'] = usuario.id
            session['username'] = usuario.username
            session['is_admin'] = usuario.is_admin
            current_app.logger.info(f"Login realizado: {usuario.username} (Admin={usuario.is_admin})")
            flash(f'Bem-vindo(a), {usuario.username}!', 'success')
            
            if usuario.is_admin == 1:
                return redirect(url_for('padaria.produtos'))
            return redirect(url_for('padaria.index'))
        else:
            current_app.logger.warning(f"Falha de login para o usuário: {username}")
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        senha = request.form.get('senha', '').strip()

        if len(username) < 3 or len(senha) < 4:
            flash('Usuário deve ter no mínimo 3 caracteres e senha no mínimo 4.', 'warning')
            return render_template('cadastro_usuario.html')

        # Verifica se o usuário já existe no banco
        if Usuario.buscar_por_username(username):
            flash(f'O usuário "{username}" já está cadastrado! Escolha outro nome ou faça login.', 'danger')
            return render_template('cadastro_usuario.html')

        novo_usuario = Usuario(username=username, is_admin=0)
        novo_usuario.definir_senha(senha)
        novo_usuario.salvar()

        current_app.logger.info(f"Novo cliente cadastrado: {username}")
        flash('Conta criada com sucesso! Faça seu login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro_usuario.html')

@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'Desconhecido')
    session.clear()
    current_app.logger.info(f"Logout realizado: {username}")
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('padaria.index'))

@auth_bp.route('/alternar-tema')
def alternar_tema():
    tema_atual = request.cookies.get('tema', 'claro')
    novo_tema = 'escuro' if tema_atual == 'claro' else 'claro'
    
    destino = request.referrer or url_for('padaria.index')
    resposta = make_response(redirect(destino))
    resposta.set_cookie('tema', novo_tema, max_age=30*24*60*60)
    return resposta