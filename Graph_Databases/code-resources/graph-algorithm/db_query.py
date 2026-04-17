def add_node(tx,node,**kawargs):
    query = f"""
          CREATE (p:{node} $props)
        """
    tx.run(query=query, props=kawargs)

def add_relationship(tx, nodeA, nodeB, nodeAMatch, nodeBMatch, rel_type, **kwargs):
    query = f"""
        MATCH (a:{nodeA} {{name: $nodeAMatch}})
        MATCH (b:{nodeB} {{name: $nodeBMatch}})
        CREATE (a)-[r:{rel_type} $props]->(b)
    """
    tx.run(query=query, nodeAMatch=nodeAMatch, nodeBMatch=nodeBMatch, props=kwargs)





