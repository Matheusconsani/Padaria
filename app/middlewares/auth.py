from flask import request, session, redirect

def verificar_sessao():
    if request.path.startswith('/admin') and request.endpoint != 'admin.login':
        if not session.get('logado'):
            return redirect('/admin/login')