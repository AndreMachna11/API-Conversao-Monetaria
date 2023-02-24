from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient

# Define a função que será executada em uma thread do pool
def fetch_data():
    with MongoClient("mongodb://localhost:27017/") as client:
        db = client["my_database"]
        collection = db["my_collection"]
        return collection.find({})  # Exemplo de consulta

# Cria o pool de threads
pool = ThreadPoolExecutor(max_workers=10)

# Submete a função para ser executada em uma das threads do pool
future = pool.submit(fetch_data)

# Obtém o resultado da execução da função
result = future.result()

# Imprime o resultado
for doc in result:
    print(doc)
