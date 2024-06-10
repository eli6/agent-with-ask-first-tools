from agentGraph.state import graph_builder
from typing import Literal

from langchain_mistralai import ChatMistralAI
from agentGraph.state import State, graph_builder

from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver

from agentGraph.tools import safe_tools, unsafe_tools, unsafe_tool_names


tools = [*safe_tools, *unsafe_tools]
memory = SqliteSaver.from_conn_string(":memory:")

#make sure MISTRAL_API_KEY is set in your environment
llm = ChatMistralAI(model="mistral-large-latest")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[*safe_tools])
graph_builder.add_node("tools", tool_node)

danger_tool_node = ToolNode(tools=[*unsafe_tools])
graph_builder.add_node("danger_tools", danger_tool_node)


def route_tools(state: State) -> Literal["tools", "__end__"]:
    """Use in the conditional_edge to route to the ToolNode if the last message has tool calls. Otherwise, route to the end."""
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError("No message found in input state to tool_edge")

    callsDangerTool = any((tc.get("name") in unsafe_tool_names) for tc in ai_message.tool_calls)
        # check if tool calls contains the name of a danger_tool:
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0 and callsDangerTool:
        print("routing to danger_tools")
        return "danger_tools"
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        print("routing to safe tools")
        return "tools"
    return "__end__"


graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # mapping of return values to node names.
    { "tools": "tools", "danger_tools": "danger_tools", "__end__": "__end__"},
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("danger_tools", "chatbot")
graph_builder.set_entry_point("chatbot")

graph = graph_builder.compile(checkpointer=memory, interrupt_before=["danger_tools"])


