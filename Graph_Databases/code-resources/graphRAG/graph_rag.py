from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os 

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI_LOCAL")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD_LOCAL")


graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
)

schema = graph.schema
print(schema)


from langchain_core.prompts import PromptTemplate

CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You generate Cypher queries for a Neo4j graph.

Use ONLY the labels, relationships, and properties
defined in the schema below.
Do NOT invent anything.
If the question cannot be answered using this schema,
return an empty result.

Schema:
{schema}

Question:
{question}

Cypher:
"""
)

from langchain_openai import ChatOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY)

question = "Which device has the ip address 193.87.247.40, return the device details"

cypher = llm.invoke(
    CYPHER_PROMPT.format(
        schema=schema,
        question=question
    )
)

print("---")
print(cypher.content)
