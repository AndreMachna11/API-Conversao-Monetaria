from src import pool_de_conexoes
import secrets
import datetime as dt
from datetime import datetime
import hashlib
from src import cache_tokens

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

        #Gera um token aleatorio de 64 caracteres registra sua hora e salve no cache
        token = secrets.token_hex(32)
        geracao = datetime.now()
        cache_tokens[registro_usuario[0]['usuario']] = {"token":token,"gerado_em":geracao}
        
        #Registra no banco de dados a hora de geração e o token gerado
        documento_procurando = {"usuario":user}
        documento_inserido = {"ultimo_token_gerado": token, "data_geracao_ultimo_token": geracao}
        colecao.find_one_and_update(documento_procurando,{'$set': documento_inserido},upsert=True)

        #Devolve a conexão ao pool de conexoes
        pool_de_conexoes.release_connection(conn)
        
        return token

    def verifica_validade_token(self,token):
        
        #Checka se o token existe entre os token existentes gerados e salvos no cache
        token_encontrado = False
        for user in cache_tokens:
            if cache_tokens[user]["token"] == token:
                token_encontrado = True
                geracao = cache_tokens[user]["gerado_em"]
                usuario = user
                break
            else:
                pass
        
        #Retorna se o token não foi encontrado no cache
        if token_encontrado == False:
            return 'TOKEN INVALIDO - USE O END POINT DE LOGIN'
        else:
            pass

        #Checka se além de exitir ele foi gerado dentro das ultimas 24 horas
        difference = dt.datetime.now() - geracao
        if difference.total_seconds() > 86400:
            del cache_tokens[usuario]
            return 'TOKEN EXPIRADO - USE O END POINT DE LOGIN'

        return True