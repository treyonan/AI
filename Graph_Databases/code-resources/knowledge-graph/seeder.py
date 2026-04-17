dummy_data = {
   "customers": [
  {"id": "CUST000", "name": "Brandy Payne", "age": 28, "location": "Nelsonstad"},
  {"id": "CUST001", "name": "Gregory Hernandez", "age": 50, "location": "Strongbury"},
  {"id": "CUST002", "name": "Felicia Orr", "age": 22, "location": "Port Alyssa"},
  {"id": "CUST003", "name": "Shane Wright", "age": 21, "location": "Sototon"},
  {"id": "CUST004", "name": "Alexis Mays", "age": 30, "location": "North Jenniferview"}
 ],
 "accounts": [
  {"id": "ACC000", "type": "Checking", "balance": 8587.97},
  {"id": "ACC001", "type": "Checking", "balance": 9554.51},
  {"id": "ACC002", "type": "Checking", "balance": 1885.20},
  {"id": "ACC003", "type": "Savings", "balance": 6821.14},
  {"id": "ACC004", "type": "Savings", "balance": 1205.02}
],
"devices": [
  {"id": "DEV000", "ip_address": "12.102.150.89", "phone": "+1-880-677-7812x9312", "card_reader": "f39130f3-9753-4359-a7c3-b58622b1871a"},
  {"id": "DEV001", "ip_address": "193.87.247.40", "phone": "386.591.7223x764", "card_reader": "1ec6e8ba-4ddb-43f6-a286-9583ae42f33f"},
  {"id": "DEV002", "ip_address": "106.82.134.208", "phone": "001-844-585-5771", "card_reader": "544fea11-b5da-4389-a0e6-404448afba60"},
  {"id": "DEV003", "ip_address": "131.14.215.244", "phone": "477.931.9414x5057", "card_reader": "ee9a1f50-48fd-4302-9165-89879e19a9ab"},
  {"id": "DEV004", "ip_address": "124.165.253.170", "phone": "344-215-0150", "card_reader": "d06b8007-0e5b-4553-ab2d-280100eab41b"}
],
"transactions": [
  {"id": "TXN000", "amount": 151.93, "time": "2025-11-16 16:58:00", "location": "North Brooke"},
  {"id": "TXN001", "amount": 308.06, "time": "2025-11-27 13:00:50", "location": "Delhi"},
  {"id": "TXN002", "amount": 320.95, "time": "2025-11-15 19:47:55", "location": "Phillipsfurt"},
  {"id": "TXN003", "amount": 106.88, "time": "2025-11-24 02:43:51", "location": "East Amandatown"},
  {"id": "TXN004", "amount": 193.85, "time": "2025-11-24 08:18:29", "location": "Cruzberg"}
],
"merchants": [
  {"id": "MER000", "store": "Acme Retailers", "category": "Electronics"},
  {"id": "MER001", "store": "FreshMart", "category": "Grocery"},
  {"id": "MER002", "store": "StyleHub", "category": "Clothing"},
  {"id": "MER003", "store": "FuelPoint", "category": "Fuel"},
  {"id": "MER004", "store": "Foodies", "category": "Dining"}
] 
}

def add_node(tx):
    for customer in dummy_data["customers"]:
        query = """
          CREATE (c: Customer $props)
         """
        tx.run(query=query, props=customer)
    for account in dummy_data["accounts"]:
        query = """
          CREATE (a: Account $props)
         """
        tx.run(query=query, props=account)
    for device in dummy_data["devices"]:
        query = """
          CREATE (d: Device $props)
         """
        tx.run(query=query, props=device)
    for transaction in dummy_data["transactions"]:
        query = """
          CREATE (t: Transaction $props)
         """
        tx.run(query=query, props=transaction)
    for merchant in dummy_data["merchants"]:
        query = """
          CREATE (m: Merchant $props)
         """
        tx.run(query=query, props=merchant)                

def add_relationship(tx):

    # 1. Relationship: Customer OWNS Account
    for i in range(len(dummy_data["customers"])):
        query = """
          MATCH (c: Customer {id: $customer_id})
          MATCH (a: Account {id: $account_id})
          CREATE (c)-[:OWNS]->(a)
         """
        tx.run(query=query, customer_id=dummy_data["customers"][i]["id"], account_id=dummy_data["accounts"][i]["id"])

    # 2. Account makes Transaction
    for i in range(len(dummy_data["accounts"])):
        query = """
          MATCH (a: Account {id: $account_id})
          MATCH (t: Transaction {id: $transaction_id})
          CREATE (a)-[:MAKES]->(t)
            """
        tx.run(query=query, account_id=dummy_data["accounts"][i]["id"], transaction_id=dummy_data["transactions"][i]["id"])     

    # 3. Transaction at Merchant
    for i in range(len(dummy_data["transactions"])):
        query = """
          MATCH (t: Transaction {id: $transaction_id})
          MATCH (m: Merchant {id: $merchant_id})
          CREATE (t)-[:AT]->(m)
            """
        tx.run(query=query, transaction_id=dummy_data["transactions"][i]["id"], merchant_id=dummy_data["merchants"][i]["id"])

    # 4. Transaction using Device
    for i in range(len(dummy_data["transactions"])):
        query = """
          MATCH (t: Transaction {id: $transaction_id})
          MATCH (d: Device {id: $device_id})
          CREATE (t)-[:USING]->(d)
            """
        tx.run(query=query, transaction_id=dummy_data["transactions"][i]["id"], device_id=dummy_data["devices"][i]["id"])        

    # 5. Customer USES Device
    for i in range(len(dummy_data["customers"])):
        query = """
          MATCH (c: Customer {id: $customer_id})
          MATCH (d: Device {id: $device_id})
          CREATE (c)-[:USES]->(d)
            """
        tx.run(query=query, customer_id=dummy_data["customers"][i]["id"], device_id=dummy_data["devices"][i]["id"])    