from flask import Flask
import os
import json
from dotenv import load_dotenv
from dotenv import find_dotenv
from src.db import MongoDBConnectionPool
load_dotenv(find_dotenv())

#Cache para a consulta de tokens ativos
cache_tokens = {}

#Instanciamento do pool de conexoes que será usado durante toda a aplicação
pool_de_conexoes = MongoDBConnectionPool(10, os.getenv('string_de_conexao'))

#Classe que padroniza a geração de response dos serviços da api
class GeraResponse():
    def gera_response(self,status_code,message_response,body):

        dict_retorno = {
            "status_code": int(status_code),
            "message_response": str(message_response),
            "body": body
        }       

        return json.dumps(dict_retorno), int(status_code)

app = Flask(__name__)