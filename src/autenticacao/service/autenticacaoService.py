from src import pool_de_conexoes
import secrets
import datetime as dt
from datetime import datetime
import hashlib

class AutenticacaoService():

    def login(self,user,password):
       
        #Abre uma conexão da pool e busca um usuario no banco de dados
        conn = pool_de_conexoes.get_connection()
        database = conn["ServicosFinanceiros"]
        colecao = database["usuarios_api"]
        registro_usuario = list(colecao.find({"usuario":user}))
        
        #Verifica se o usuario existe
        if len(registro_usuario) == 0:
            return 'USUARIO NAO ENCONTRADO'     

        #Verifica se a senha está correta
        if registro_usuario[0]['senha'] != hashlib.md5((password).encode()).hexdigest():
            return 'SENHA ERRADA'

        #Gera um token aleatorio de 64 caracteres
        token = secrets.token_hex(32)

        #Registra no banco de dados a hora de geração e o token gerado
        documento_procurando = {"usuario":user}
        documento_inserido = {"ultimo_token_gerado": token, "data_geracao_ultimo_token": datetime.now()}
        colecao.find_one_and_update(documento_procurando,{'$set': documento_inserido},upsert=True)

        #Devolve a conexão ao pool de conexoes
        pool_de_conexoes.release_connection(conn)
        
        return token

    def verifica_validade_token(self,token):
        
        #Checka se o token existe entre os token existentes gerados para usuarios validos
        try:
            validade = cache_tokens[token]
        except:
            return 'TOKEN INVALIDO'
        
        #Checka se além de exitir ele foi gerado dentro das ultimas 24 horas
        difference = dt.datetime.now() - validade
        if difference.total_seconds() > 86400:
            del cache_tokens[token]
            return 'TOKEN EXPIRADO'

        return True