def add_fraud_transaction(tx):
    # - Impossible travel rule: Same account used in Delhi and London within 10 minutes.
    query = """
        MATCH (a:Account {id: "ACC001"}), (d:Device {id: "DEV001"})
        CREATE (t:Transaction {
            id: "TXN9992",
            amount: 4500.00,
            time: "2025-11-27 13:01:50",
            location: "London"
        })
        CREATE (m:Merchant {
            id: "MER999",
            store: "Luxury Hub",
            category: "Luxury Goods"
        })
        CREATE (a)-[:MAKES]->(t)
        CREATE (t)-[:USING]->(d)
        CREATE (t)-[:AT]->(m);
    """
    tx.run(query)

def check_impossible_travel(tx):
    # flag the transaction if same account has two transactions in different locations within 30 minutes
    query = """
        MATCH (a:Account)-[:MAKES]->(t1:Transaction),
            (a)-[:MAKES]->(t2:Transaction)
        WHERE datetime({epochMillis: apoc.date.parse(t1.time, 'ms', 'yyyy-MM-dd HH:mm:ss')}) <
            datetime({epochMillis: apoc.date.parse(t2.time, 'ms', 'yyyy-MM-dd HH:mm:ss')})
        AND (
            apoc.date.parse(t2.time, 'ms', 'yyyy-MM-dd HH:mm:ss') -
            apoc.date.parse(t1.time, 'ms', 'yyyy-MM-dd HH:mm:ss')
        ) < 1800 * 1000
        AND t1.location <> t2.location
        RETURN a.id AS accountId, t1.id AS txn1, t2.id AS txn2;
    """

    result = tx.run(query)     
    return [record.data() for record in result]   