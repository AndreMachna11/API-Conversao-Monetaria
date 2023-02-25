from src import pool_de_conexoes
import datetime
import requests

class ConversaoMonetariaService():

    def conversor(self,valor,de,para):
       
        #pega uma conexão da pool de concexões e busca um usuario no banco de dados
        conn = pool_de_conexoes.get_connection()
        database = conn["ServicosFinanceiros"]
        colecao = database["conversao_monetaria"]
        dados = list(colecao.find({"_id":"conversao_lastreada_em_dolar"}))[0]
        
        #Verificação da data_base dos dados
        data_base = dados['data_base']
        hoje = str(datetime.date.today())

        #Caso os dados não tenham sidos atualizados no dia de hoje sera feita uma chamada de api externa para atualizar o banco de dados, o que fará com que as proximas consultas do dia sejam masi rapidas e com dados atualizados
        if data_base != hoje:
            
            url = 'https://min-api.cryptocompare.com/data/price'

            # Parâmetros da requisição
            params_brl = {
                'fsym': 'USD',
                'tsyms': 'BRL'
            }

            params_eur = {
                'fsym': 'USD',
                'tsyms': 'EUR'
            }

            params_btc = {
                'fsym': 'USD',
                'tsyms': 'BTC'
            }

            params_eth = {
                'fsym': 'USD',
                'tsyms': 'ETH'
            }

            response_brl = requests.get(url, params=params_brl)
            response_eur = requests.get(url, params=params_eur)
            response_btc = requests.get(url, params=params_btc)
            response_eth = requests.get(url, params=params_eth)

            result1 = response_brl.json()
            result2 = response_eur.json()
            result3 = response_btc.json()
            result4 = response_eth.json()

            real = result1['BRL']
            euro = result2['EUR']
            bitcoin = result3['BTC']
            eth = result4['ETH']

            #Registra no banco de dados a hora de geração e o token gerado
            documento_procurando = {"_id":"conversao_lastreada_em_dolar"}
            documento_inserido = {"data_base": hoje, "USD": 1, "BRL": real, "EUR": euro,"BTC": bitcoin,"ETH":eth}
            colecao.find_one_and_update(documento_procurando,{'$set': documento_inserido},upsert=True)
            
            #Devolve a conexão ao pool de conexoes
            pool_de_conexoes.release_connection(conn)

            #convertendo para dolar o valor informado
            valor_dolar = documento_inserido[de]*valor 

            #convertendo de dolar para valor alvo
            valor_alvo = valor_dolar*documento_inserido[para]

            return str(valor_alvo) + ' ' + para
        else:

            #convertendo para dolar o valor informado
            valor_dolar = dados[de]*valor 

            #convertendo de dolar para valor alvo
            valor_alvo = valor_dolar*dados[para]
            
            #Devolve a conexão ao pool de conexoes
            pool_de_conexoes.release_connection(conn)

            return str(valor_alvo) + ' ' + para