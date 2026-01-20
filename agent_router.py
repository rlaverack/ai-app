from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic

class State(TypedDict):
    messages: Annotated[list, add_messages]
    route: str

llm = ChatAnthropic(model="claude-sonnet-4-20250514")

def classifier(state: State) -> State:
    return_response = ""
    # 1. Get the latest user message from state["messages"]
    user_input = state["messages"][-1].content    
    # 2. Ask Claude: "Can you answer this confidently? Reply ONLY 'yes' or 'no'"
    response = llm.invoke([
        {"role": "user", "content": f"Classify if the following statement can be answered confidently. Reply with ONLY 'yes' or 'no': {user_input}"}
    ])    
    # 3. Parse the response
    if response.content.strip().lower() == "yes":
        return_response = "answerable"
    else:
        return_response = "fallback"
    # 4. Return {"route": "answerable"} or {"route": "fallback"}
    return {'route': return_response}

def chatbot(state: State) -> State:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def fallback(state: State) -> State:
    fallback_response = {"messages": [
        {"role": "assistant", "content": f"I can't answer that question, could you rephrase?"}
    ]}
    return fallback_response

def route_decision(state: State) -> str:
    if state["route"] == "answerable":
        return "chatbot"
    else:
        return "fallback"

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("classifier", classifier)
graph_builder.add_node("fallback", fallback)
graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("chatbot", END)
graph_builder.add_edge("fallback", END)
graph_builder.add_conditional_edges("classifier", route_decision)
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