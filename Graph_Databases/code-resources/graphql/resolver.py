from dotenv import load_dotenv
from ariadne import load_schema_from_path, make_executable_schema, QueryType, MutationType, ObjectType, graphql_sync
import os 
import uuid 
from db import Neo4jConnection 
from ariadne.wsgi import GraphQL
from wsgiref.simple_server import make_server


load_dotenv() 
URI = os.getenv("NEO4J_URI_LOCAL")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD_LOCAL"))


query = QueryType()
mutation = MutationType()
product_type = ObjectType("Product")
order_type = ObjectType("Order")
user_type = ObjectType("User")

neo4j = Neo4jConnection(URI,auth=AUTH)

@mutation.field("createUser")
def resolve_create_user(_, info, username, email):
    user_id = str(uuid.uuid4())
    cypher_query = """
    CREATE (u:User {id: $user_id, username: $username, email: $email})
    RETURN u { .id, .username, .email } AS user
    """
    parameters = {
        "user_id": user_id,
        "username": username,
        "email": email
    }
    result = neo4j.query(cypher_query, parameters)
    return result[0]["user"] if result else None


@mutation.field("createProduct")
def resolve_create_product(_, info, name, price):
    product_id = str(uuid.uuid4())
    cypher_query = """
    CREATE (p:Product {id: $product_id, name: $name, price: $price})
    RETURN p { .id, .name, .price } AS product
    """
    parameters = {
        "product_id": product_id,
        "name": name,
        "price": price
    }
    result = neo4j.query(cypher_query, parameters)
    return result[0]["product"] if result else None

@mutation.field("createOrder")
def resolve_create_order(_, info, userId, productIds):
    order_id = str(uuid.uuid4())
    query = """
    MATCH (u:User {id: $user_id})
    WITH u
    CREATE (o:Order {id: $order_id, date: date(), totalAmount:0})
    MERGE (u)-[:PLACED]->(o)
    WITH o, $product_ids AS pids
    UNWIND pids AS pid
    MATCH (p:Product {id: pid})
    MERGE (o)-[:CONTAINS]->(p)
    WITH o, collect(p) AS products
    SET o.totalAmount = reduce(total=0, prod IN products | total + prod.price)
    RETURN o { .id, .date, .totalAmount } AS order
    """
    resp = neo4j.query(query, parameters={"user_id": userId, "order_id": order_id, "product_ids": productIds})
    return resp[0]['order']


@query.field("users")
def resolve_users(_, info):
    cypher_query = """
    MATCH (u:User)
    RETURN u { .id, .username, .email } AS user
    """
    result = neo4j.query(cypher_query)
    return [record["user"] for record in result]

@query.field("products")
def resolve_products(_, info):
    cypher_query = """
    MATCH (p:Product)
    RETURN p { .id, .name, .price } AS product
    """
    result = neo4j.query(cypher_query)
    return [record["product"] for record in result]


@user_type.field("orders")
def resolve_user_orders(obj, info):
    cypher_query = """
    MATCH (u:User {id: $user_id})-[:PLACED]->(o:Order)
    RETURN o { .id, .date, .totalAmount } AS order
    """
    parameters = {"user_id": obj["id"]}
    result = neo4j.query(cypher_query, parameters)
    return [record["order"] for record in result]


@order_type.field("products")
def resolve_order_products(obj, info):
    cypher_query = """
    MATCH (o:Order {id: $order_id})-[:CONTAINS]->(p:Product)
    RETURN p { .id, .name, .price } AS product
    """
    parameters = {"order_id": obj["id"]}
    result = neo4j.query(cypher_query, parameters)
    return [record["product"] for record in result]

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, user_type, order_type, product_type
)

app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    server = make_server("0.0.0.0",8000,app)
    print("server is running....")
    server.serve_forever()




