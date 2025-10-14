from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph

from prompts import (
    agent_system_prompt,
    default_background,
    default_response_preferences,
)
from schemas import State

# from tools import get_tools, get_tools_by_name

load_dotenv(".env")

AGENT_TOOLS_PROMPT = """
1. write_email(to, subject, content) - Send emails to specified recipients
2. Done - E-mail has been sent
"""

# Get tools
# tools = get_tools()
# tools_by_name = get_tools_by_name(tools)

# Initialize the LLM, enforcing tool use (of any available tools) for agent
llm = init_chat_model("azure_openai:gpt-4o", temperature=0.0)
# llm_with_tools = llm.bind_tools(tools, tool_choice="any")


# Nodes
def llm_call(state: State):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            llm.invoke(
                [
                    {
                        "role": "system",
                        "content": agent_system_prompt.format(
                            tools_prompt="No tools",
                            # tools_prompt=AGENT_TOOLS_PROMPT,
                            background=default_background,
                            response_preferences=default_response_preferences,
                        ),
                    },
                ]
                + state["messages"]
            )
        ]
    }


# def tool_node(state: State):
#     """Performs the tool call"""

#     result = []
#     for tool_call in state["messages"][-1].tool_calls:
#         tool = tools_by_name[tool_call["name"]]
#         observation = tool.invoke(tool_call["args"])
#         result.append(
#             {"role": "tool", "content": observation, "tool_call_id": tool_call["id"]}
#         )
#     return {"messages": result}


# Conditional edge function
# def should_continue(state: State) -> Literal["Action", "__end__"]:
#     """Route to Action, or end if Done tool called"""
#     messages = state["messages"]
#     last_message = messages[-1]
#     if last_message.tool_calls:
#         for tool_call in last_message.tool_calls:
#             if tool_call["name"] == "Done":
#                 return END
#             else:
#                 return "Action"


# Build workflow
agent_builder = StateGraph(State)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
# agent_builder.add_node("environment", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
# agent_builder.add_conditional_edges(
#     "llm_call",
#     should_continue,
#     {
#         # Name returned by should_continue : Name of next node to visit
#         "Action": "environment",
#         END: END,
#     },
# )
# agent_builder.add_edge("environment", "llm_call")

# Compile the agent
agent = agent_builder.compile()
