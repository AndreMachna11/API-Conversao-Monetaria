# API-Conversao-Monetaria
-API construida em python utilizando o framework Flask e banco de dados em nuvem MongoDB

-Converte valores monetários entre as moedas USD, BRL, EUR, BTC, ETH

-Usa seu proprio banco de dados em nuvem para consultas atualizando os dados uma vez por dia

-Aplica conceitos de permoface, como pool de conexões e cache para alguns dados

-Responde JSON com formato padronizado ate nos momentos de erro interno e bad request

# Instruçoes para Execução:
git clone https://github.com/AndreMachna11/API-Conversao-Monetaria.git

cd API-Conversao-Monetaria

pip3 install -r requirements.txt

python3 main.py

# Instrução de uso dos end points
São dois end points implementados, um para autenticação de usuarios e outro para a conversão em si

# Autenticação:
post -url: http://127.0.0.1:5000/autenticacao/login

headers: {"login" : "teste@teste.com", "senha": "Lmmbupjo123@"}
  
O retorno será um JSON no formato:

    {
      "status_code": 200,
      "message_response": "SUCESSO",
      "body": {
        "token": "6f1fc2d0a558a94f1ac0a4f5ff69a055a4db12294a54471f6e47ab6f082c2ee4"
      }
    }

Onde o token tem validade de 24 horas deve ser usado para o proximo endpoint

# Conversao Monetaria
post -url: http://127.0.0.1:5000/conversaoMonetaria/conversao

headers: {"Content-Type" : "application/json", "token": "6f1fc2d0a558a94f1ac0a4f5ff69a055a4db12294a54471f6e47ab6f082c2ee4"}

body: {"valor": 4,"de":"brl", para:"eur"}

O retorno será um JSON no formato:

    {
      "status_code": 200,
      "message_response": "SUCESSO",
      "body": {
        "valor_convertido": "0.7334 EUR"
      }
    }


