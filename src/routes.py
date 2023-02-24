from src import app
from src.autenticacao.views.autenticacaoView import AutenticacaoView

AutenticacaoView.register(app, route_base='/autenticacao/')