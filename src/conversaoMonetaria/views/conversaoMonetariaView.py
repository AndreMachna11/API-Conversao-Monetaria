from flask_classful import FlaskView
from flask_classful import route
from flask import request
from src import GeraResponse
from src.autenticacao.service.autenticacaoService import AutenticacaoService
from src.conversaoMonetaria.service.conversaoMonetariaService import ConversaoMonetariaService

class ConversaoMonetariaView(FlaskView):
    route_base = 'conversaoMonetaria'

    @route('/conversao',methods=['GET', 'POST'])
    def conversao_moedas(self):
        
        #Instancia que gerará o response
        RESPONSE = GeraResponse()

        #Le os dados enviados no cabeçalho e do corpo da requisição
        headers = request.headers
        body = request.get_json()

        #Verificação de Existencia do token no cabeçalho
        try:
            token = headers['token']
        except:
            return RESPONSE.gera_response(400,"TOKEN NAO ENVIADO",{})
        

        #Verificando Validade do Token Informado no cabeçalho
        try:
            AUTENTICADOR = AutenticacaoService()
            valida_token = AUTENTICADOR.verifica_validade_token(token)

            if valida_token != True:
                if valida_token == 'TOKEN EXPIRADO':
                    return RESPONSE.gera_response(400,"TOKEN EXPIRADO",{})
                else:
                    return RESPONSE.gera_response(400,"TOKEN INVALIDO",{})
        except:
            return RESPONSE.gera_response(500,"ERRO INTERNO",{})

        #Verificação de existencia e validade da variavel "valor" no corpo da requisição
        try:
            valor = body['valor']
            try:
                valor = float(valor)
            except: 
                return RESPONSE.gera_response(400,"VALOR INVALIDO - INFORME APENAS VALORES SEM PONTOS E TRAÇOS",{})
        except:
            return RESPONSE.gera_response(400,"VALOR NAO ENVIADO NO CORPO DA REQUISICAO",{})

        #Verificação de existencia e validade da variavel "de" no corpo da requisição
        try:
            de = body['de'].upper()
            if len(de) != 3 or de not in ['USD','BRL','EUR','BTC','ETH']:
                return RESPONSE.gera_response(400,"MOEDA DE ORIGEM INVALIDA - INFORME APENAS A SIGLA DE 3 DIGITOS DA MOEDA (USD,BRL,EUR,BTC,ETH)",{})
            else: 
                pass
        except:
            return RESPONSE.gera_response(400,"MOEDA DE ORIGEM NAO ENVIADA NO CORPO DA REQUISICAO",{})

        #Verificação de existencia e validade da variavel "para" no corpo da requisição
        try:
            para = body['para'].upper()
            if len(para) != 3 or para not in ['USD','BRL','EUR','BTC','ETH']:
                return RESPONSE.gera_response(400,"MOEDA DE DESTINO INVALIDA - INFORME APENAS A SIGLA DE 3 DIGITOS DA MOEDA (USD,BRL,EUR,BTC,ETH)",{})
            else: 
                pass
        except:
            return RESPONSE.gera_response(400,"MOEDA DE DESTINO NAO ENVIADA NO CORPO DA REQUISICAO",{})


        #Chamada do Serviço e montagem da resposta em json
        # try:
        CONVERSOR = ConversaoMonetariaService()
        valor_convertido = CONVERSOR.conversor(valor,de,para)

        dict_retorno = {"valor_convertido" : str(valor_convertido)}
        return RESPONSE.gera_response(200,"SUCESSO",dict_retorno)
        # except:
        #     return RESPONSE.gera_response(500,"ERRO INTERNO",{})