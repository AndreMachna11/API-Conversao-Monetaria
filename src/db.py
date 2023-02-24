from pymongo import MongoClient
from queue import Queue
from threading import Lock
from datetime import datetime, timedelta

#Definição da classe de pool de conexõee para Gerenciamento das conexões entre a API e o banco de dados mongoDB
class MongoDBConnectionPool:
    def __init__(self, max_connections, connection_string, timeout=300):
        self.max_connections = max_connections
        self.connection_string = connection_string
        self.timeout = timeout
        self.connection_queue = Queue(max_connections)
        self.lock = Lock()
        self.connections = set()

    def get_connection(self):
        with self.lock:
            if not self.connection_queue.empty():
                connection, expiry = self.connection_queue.get()
                if expiry > datetime.now():
                    return connection
                else:
                    connection.close()
                    self.connections.remove(connection)
            if len(self.connections) < self.max_connections:
                connection = MongoClient(self.connection_string)
                self.connections.add(connection)
                return connection
        return None

    def release_connection(self, connection):
        expiry = datetime.now() + timedelta(seconds=self.timeout)
        self.connection_queue.put((connection, expiry))

    def close(self):
        with self.lock:
            while not self.connection_queue.empty():
                connection, _ = self.connection_queue.get()
                connection.close()
            for connection in self.connections:
                connection.close()
            self.connections.clear()