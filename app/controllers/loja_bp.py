from flask import Blueprint, render_template
from app.models.produto_model import ProdutoModel
from app.models.loja_model import LojaModel

loja_bp = Blueprint('loja', __name__)

@loja_bp.route('/')
def home():
    produtos = ProdutoModel.listar_todos()
    loja_aberta = LojaModel.esta_aberta()
    return render_template('loja.html', produtos=produtos, loja_aberta=loja_aberta)