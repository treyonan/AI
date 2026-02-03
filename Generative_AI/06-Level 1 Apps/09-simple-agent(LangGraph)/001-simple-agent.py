import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=2)

response = search.invoke("Who are the top stars of the 2024 Eurocup?")

print("\n----------\n")

print("Who are the top stars of the 2024 Eurocup?")

print("\n----------\n")
print(response)

print("\n----------\n")

tools = [search]

llm_with_tools = llm.bind_tools(tools)

from langgraph.prebuilt import create_react_agent

agent_executor = create_react_agent(llm, tools)

from langchain_core.messages import HumanMessage

response = agent_executor.invoke({"messages": [HumanMessage(content="Where is the soccer Eurocup 2024 played?")]})

print("\n----------\n")

print("Where is the soccer Eurocup 2024 played? (agent)")

print("\n----------\n")
print(response["messages"])

print("\n----------\n")

print("\n----------\n")

print("When and where will it be the 2024 Eurocup final match? (agent with streaming)")

print("\n----------\n")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="When and where will it be the 2024 Eurocup final match?")]}
):
    print(chunk)
    print("----")

print("\n----------\n")

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

agent_executor = create_react_agent(llm, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "001"}}

print("Who won the 2024 soccer Eurocup?")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="Who won the 2024 soccer Eurocup?")]}, config
):
    print(chunk)
    print("----")

print("Who were the top stars of that winner team?")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="Who were the top stars of that winner team?")]}, config
):
    print(chunk)
    print("----")

print("(With new thread_id) About what soccer team we were talking?")

config = {"configurable": {"thread_id": "002"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="About what soccer team we were talking?")]}, config
):
    print(chunk)
    print("----")