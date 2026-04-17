from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri,auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def execute_write(self, method):
        with self.driver.session() as session:
            return session.execute_write(method)    

    def query(self, method):
        with self.driver.session() as session:
            result = session.execute_read(method)
            return [record for record in result]