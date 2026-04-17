from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import csv 

load_dotenv()

URI = os.getenv("NEO4J_URI_LOCAL")
AUTH = ( os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD_LOCAL') )

class Neo4jProvider:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(URI, auth=AUTH)
            self.driver.verify_connectivity()
            print("Successfully connected to Neo4j")
            
        except Exception as e:
            print("Error connecting to Neo4j:", e)
            raise    

    def closeConnection(self):
        if self.driver:
            self.driver.close()
            print("Connection to Neo4j closed.")

    def create_nodes_from_csv(self, csv_file):
        with self.driver.session() as session:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    session.run(
                        "CREATE (p:Person {name: $name, age: $age, city: $city, email: $email})",
                        name=row['Name'],
                        age=int(row['Age']),
                        city=row['City'],
                        email=row['Email']
                    )
            print(f"Nodes created from {csv_file}")   

    def create_relationship(self, name1, name2):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Person {name: $name1}), (b:Person {name: $name2})
                CREATE (a)-[:FRIENDS_WITH]->(b)
                """,
                name1=name1,
                name2=name2
            )
            print(f"Created FRIENDS_WITH relationship between {name1} and {name2}")             


if __name__ == "__main__":
    neo4j = Neo4jProvider()        
    #neo4j.create_nodes_from_csv('friends.csv')
    neo4j.create_relationship('Bruce Cooper', 'Todd Williams')
    neo4j.create_relationship('Todd Williams', 'Bruce Cooper')
    neo4j.closeConnection()