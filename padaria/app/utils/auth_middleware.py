from functools import wraps
from flask import session, redirect, url_for, flash, g, current_app
from app.models.usuario_model import Usuario

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        usuario = Usuario.buscar_por_id(user_id)
        if not usuario:
            session.clear()
            current_app.logger.warning(f"Sessão inválida detectada para user_id={user_id}")
            flash('Sessão expirada. Entre novamente.', 'danger')
            return redirect(url_for('auth.login'))
        
        g.usuario = usuario
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Faça login como padeiro para acessar a área administrativa.', 'warning')
            return redirect(url_for('auth.login'))
        
        usuario = Usuario.buscar_por_id(user_id)
        if not usuario:
            session.clear()
            return redirect(url_for('auth.login'))
        
        if usuario.is_admin != 1:
            current_app.logger.warning(f"Acesso negado à área do padeiro para o cliente: {usuario.username}")
            flash('Acesso restrito! Apenas padeiros podem gerenciar produtos e categorias.', 'danger')
            return redirect(url_for('padaria.index'))
        
        g.usuario = usuario
        return f(*args, **kwargs)
    return decorated_function