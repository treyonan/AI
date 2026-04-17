import requests 

url = "http://localhost:8000/graphql"

def create_user(username, email):
    query = """
    mutation ($username: String!, $email: String!) {
        createUser(username: $username, email: $email) {
            username
            email
        }
    }
    """
    variables = {"username": username, "email": email}
    response = requests.post(url, json={"query": query, "variables": variables})
    return response.json()


def create_product(name, price):
    query = """
    mutation ($name: String!, $price: Float!) {
        createProduct(name: $name, price: $price) {
            name
            price
        }
    }
    """
    variables = {"name": name, "price": price}
    response = requests.post(url, json={"query": query, "variables": variables})
    return response.json()


def create_order(user_id, product_ids):
    query = """
    mutation ($userId: ID!, $productIds: [ID!]!) {
        createOrder(userId: $userId, productIds: $productIds) {
            id
            date
            totalAmount
        }
    }
    """
    variables = {"userId": user_id, "productIds": product_ids}
    response = requests.post(url, json={"query": query, "variables": variables})
    return response.json()


def get_all_users():
    query = """
       query{
         users{
           username,
           email
         }
       }
    """
    response = requests.post(url,json={'query': query})
    return response.json()

def get_user_orders(userId):
    query = """
        query ($id: ID!) {
        user(id: $id) {
            orders {
                id
                date
                totalAmount
            }
        }
        }
        """
    variables = {"id": userId}
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()

def get_order_products(orderId):
    query = """
        query ($id: ID!) {
        order(id: $id) {
            products {
                id
                name
                price
            }
        }
        }
        """
    variables = {"id": orderId}
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()

# from the user id get the orders and from the order get the products
def get_user_orders_and_products(userId):
    query = """
        query ($id: ID!) {
        user(id: $id){
          id
          username 
          orders {
            id
            date
            totalAmount
            products {
              id
              name
              price
            }
          }
        }
    """
    variables = {"id": userId}
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()


if __name__ == "__main__":
    #result = create_user("john","john@gmail.com")
    #result = create_product("Laptop", 999.99)
    #result = create_order("362ca8ef-db66-4350-94c0-2ae816728f6d", ["7c8ba303-aa2d-4aa9-ac15-ea9858cdcf21"])
    result = get_all_users()
    print("result---",result)