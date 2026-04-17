from neo4j import GraphDatabase
from dotenv import load_dotenv
import os 
from db_query import add_node, add_relationship
import csv 

load_dotenv()
road_network_file = "road_network_data.csv"
road_places_file = "road_places_data.csv"
road_network_relationship = "road_network_relationship.csv"

URI = os.getenv("NEO4J_URI_LOCAL")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD_LOCAL"))


class Neo4JProvider:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(URI, auth=AUTH)
            self.driver.verify_connectivity()
        except Exception as e:
            raise Exception("There is a connection exception ")    
    
    def closeConnection(self):
        self.driver.close()

    def createNode(self,filename:str):
        with self.driver.session() as session:
            with open(filename,newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    session.execute_write(add_node, node=row['type'], **row)
                        
           
    def createNodeRelationship(self, filename:str):
        with self.driver.session() as session:
            with open(filename,newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                            filtered_item = {k: v for k, v in row.items() if k not in ['interceptor_start_point', 'interceptor_end_point']}
                            session.execute_write(
                                add_relationship, 
                                nodeA = "Interceptor",
                                nodeB = "Interceptor",
                                nodeAMatch = row['interceptor_start_point'],
                                nodeBMatch = row['interceptor_end_point'],
                                rel_type="CONNECTED_TO",
                                **filtered_item 
                            )
     
               
    def calShortestPathDijkstraApoc(self,start_node:str, end_node:str):
        with self.driver.session() as session:
            session.run(
                """
                    MATCH ()-[r:CONNECTED_TO]->()
                    SET r.cost =
                        toFloat(r.distance_km) * 0.4 +
                        toFloat(r.time) * 0.8 +
                        toFloat(r.traffic_factor) * 2.0
                """
            )
            result = session.run(
                """
                MATCH (start:Interceptor {name: $start}), (end:Interceptor {name: $end})
                CALL apoc.algo.dijkstra(start, end, 'CONNECTED_TO', 'cost')
                YIELD path
                RETURN [n IN nodes(path) | n.name] AS pathNodes
                """,
                start=start_node,
                end=end_node
            )

            record = result.single()
            if record is None:
                return [], None

            path = record["pathNodes"]
            return path

                                 
    
    def calShortestPathDijkstra(self, start_node:str, end_node:str):
        # calculate shortest path using Dijkstra's algorithm
        with self.driver.session() as session:
            # Dijkstra requires one weight property 
            session.run(
                """
                    MATCH ()-[r:CONNECTED_TO]->()
                    SET r.cost =
                        toFloat(r.distance_km) * 0.4 +
                        toFloat(r.time) * 0.8 +
                        toFloat(r.traffic_factor) * 2.0
                """
            )
            """
              - Removes any existing in-memory graph projection named "roads".
              - GDS algorithms don't run directly on your stored Neo4j graph; they run on a projected in-memory graph.
              - If you try to project a graph with the same name twice, Neo4j will throw an error.

            """
            session.run("CALL gds.graph.drop('roads', false) YIELD graphName")
            
            # - Creates a new in‑memory graph projection called "roads"
            session.run(
                """
                CALL gds.graph.project(
                'roads',
                'Interceptor',                                
                { CONNECTED_TO: { properties: 'cost',          
                                    orientation: 'NATURAL' } } 
                )
                """
            )

            result = session.run(
                """
                MATCH (start:Interceptor {name: $start}), (end:Interceptor {name: $end})
                CALL gds.shortestPath.dijkstra.stream(
                'roads',
                {
                    sourceNode: id(start),
                    targetNode: id(end),
                    relationshipWeightProperty: 'cost'
                }
                )
                YIELD totalCost, nodeIds
                RETURN
                [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS pathNodes,
                totalCost
                """,
                start=start_node,
                end=end_node
            )

            record = result.single()
            if record is None:
                return [], None

            path = record["pathNodes"]
            total_cost = record["totalCost"]
            return path, total_cost


if __name__ == "__main__":
    provider = Neo4JProvider()
    #provider.createNode(road_network_file)
    #provider.createNode(road_places_file)
    #provider.createNodeRelationship(road_network_relationship)
    #result = provider.calShortestPathDijkstraApoc("Elliott Prairie", "Michael Street")
    path, totalCost = provider.calShortestPathDijkstra("Elliott Prairie", "Michael Street")
    print(path, totalCost)
   