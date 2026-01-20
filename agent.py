from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatAnthropic(model="claude-sonnet-4-20250514")

def chatbot(state: State) -> State:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

if __name__ == "__main__":
    messages = []
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        messages.append({"role": "user", "content": user_input})
        result = graph.invoke({"messages": messages})
        messages = result["messages"]  # This now has the full history
        print(f"Claude: {messages[-1].content}")