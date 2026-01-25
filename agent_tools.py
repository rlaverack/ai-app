from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from datetime import datetime
from langchain_tavily import TavilySearch
# 1. Define your State (same as before)
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Define your tools
@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression. Example: '2 + 2' or '10 * 5'"""
    try:
        # Remove whitespace and validate the expression contains only safe characters
        expr = expression.strip()
        
        # Allow only numbers, operators, parentheses, and decimal points
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expr):
            return f"Error: Invalid characters in expression '{expression}'"
        
        # Evaluate the mathematical expression
        result = eval(expr)
        
        # Return the result as a string
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return f"Error: Invalid expression syntax '{expression}'"
    except Exception as e:
        return f"Error: {str(e)}"

@tool  
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

search_tool = TavilySearch(max_results=3)

# 3. Create LLM with tools bound
tools = [calculator, get_current_time, search_tool]
llm = ChatAnthropic(model="claude-sonnet-4-20250514")
llm_with_tools = llm.bind_tools(tools)

# 4. Define the chatbot node (calls LLM)
def chatbot(state: State) -> State:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# 5. Define routing logic
def should_continue(state: State) -> str:
    """Check if the last message has tool calls."""
    last_message = state["messages"][-1]
    has_tools = hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0
    return "tools" if has_tools else "end"
# 6. Build the graph
tool_node = ToolNode(tools)

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")  # After tools, go back to chatbot
graph_builder.add_conditional_edges("chatbot", should_continue, {
    "tools": "tools",
    "end": END
})
graph = graph_builder.compile()

# 7. Test it
if __name__ == "__main__":
    # Test with a calculation
    result = graph.invoke({"messages": [{"role": "user", "content": "What is 42 * 17?"}]})
    print(result["messages"][-1].content)
    
    # Test with time
    result = graph.invoke({"messages": [{"role": "user", "content": "What time is it?"}]})
    print(result["messages"][-1].content)
    
    # Test with something that needs no tools
    result = graph.invoke({"messages": [{"role": "user", "content": "What is the capital of France?"}]})
    print(result["messages"][-1].content)

    # Test with web search
    result = graph.invoke({"messages": [{"role": "user", "content": "What was the score of the most recent NFL playoff game?"}]})
    print(result["messages"][-1].content)