class UsuarioModel:
    USUARIO_ADMIN = "admin"
    SENHA_ADMIN = "1234"

    @classmethod
    def validar_login(cls, usuario, senha):
        return usuario == cls.USUARIO_ADMIN and senha == cls.SENHA_ADMIN