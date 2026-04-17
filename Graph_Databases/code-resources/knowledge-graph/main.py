from dotenv import load_dotenv
import os 
from db import Neo4jConnection
from seeder import add_node, add_relationship
load_dotenv()
from fraud_detection import add_fraud_transaction, check_impossible_travel


URI = os.getenv("NEO4J_URI_LOCAL")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD_LOCAL"))

database = Neo4jConnection(URI, auth=AUTH)
load_dummy_data = False 

if __name__ == "__main__":

    # load the dummy data 
    if load_dummy_data:
        database.execute_write(add_node)
        database.execute_write(add_relationship)

    # a customer submit a transaction 
    #database.execute_write(add_fraud_transaction)   

    results = database.query(check_impossible_travel) 

    if(len(results)>0):
        if results[0]['txn2'] == "TXN9992":
            print("Fraud detected due to impossible travel!")

