from src import app
from src.autenticacao.views.autenticacaoView import AutenticacaoView
from src.conversaoMonetaria.views.conversaoMonetariaView import ConversaoMonetariaView

AutenticacaoView.register(app, route_base='/autenticacao/')
ConversaoMonetariaView.register(app, route_base='/conversaoMonetaria/')