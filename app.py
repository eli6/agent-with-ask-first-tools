import streamlit as st
from agentGraph.graph import graph
from langchain_core.messages import AIMessage, ToolMessage
import json
from agentGraph.tools import tool_emoji
from agentGraph.tools import unsafe_tool_names


config = { "configurable": { "thread_id": "1"}}

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'assistant_action' not in st.session_state:
    st.session_state.assistant_action = False
if 'awaiting_confirmation' not in st.session_state:
    st.session_state.awaiting_confirmation = False
if 'processed_event_ids' not in st.session_state:
    st.session_state.processed_event_ids = set()


def process_event(event):
    event_messages = event["messages"]
    for message in event_messages:
        message_id = message.id
        if message_id not in st.session_state.processed_event_ids:

            ai_message = event["messages"][-1]
            # hi send email info@example.com asking for lunch at 13
            tool = False
            dangerToolCalled = False
            if isinstance(message, AIMessage):
                display_message = ai_message.content
                if display_message != '':
                    st.session_state.messages.append({"role": "assistant", "content": display_message})

                finish_reason = message.response_metadata.get("finish_reason")
                if finish_reason == "tool_calls":
                    dangerToolCalled = handle_tool_call_attempt(ai_message, dangerToolCalled, message)
                    tool = True

            st.session_state.processed_event_ids.add(message_id)

            if(tool & dangerToolCalled):
                st.session_state.awaiting_confirmation = True



def process_tool_call_event(event):
    event_messages = event["messages"]
    for message in event_messages:
        message_id = message.id
        if message_id not in st.session_state.processed_event_ids:

            ai_message = event["messages"][-1]
            if isinstance(message, ToolMessage):
                display_message = ai_message.content
                st.session_state.messages.append({"role": "assistant", "content": display_message})


            if isinstance(message, AIMessage):
                display_message = ai_message.content
                st.session_state.messages.append({"role": "assistant", "content": display_message})

            st.session_state.processed_event_ids.add(message_id)

            st.session_state.awaiting_confirmation = False

#todo message vs ai_message confusion
def perform_assistant_action():
    events = graph.stream(None, config, stream_mode="values")
    for event in events:
       process_tool_call_event(event)

    completion_message = "Action completed. 🎉 Do you need more assistance?"
    st.session_state.messages.append({"role": "assistant", "content": completion_message})
    st.session_state.assistant_action = False

def handle_tool_call_attempt(ai_message, dangerToolCalled, message):
    tool_calls = ai_message.additional_kwargs["tool_calls"][0] # todo handle several tool calls
    function_args = tool_calls["function"]
    arguments_json_str = function_args['arguments']
    arguments_dict = json.loads(arguments_json_str)
    query = arguments_dict['query']
    name = function_args['name']
    emoji = tool_emoji.get(name)
    tool_calls = message.tool_calls
    dangerToolCalled = any((tc.get("name") in unsafe_tool_names) for tc in ai_message.tool_calls)

    if(dangerToolCalled):
        st.session_state.messages.append({"role": "assistant", "content": f"🛠️ I would like to call the tool: *** {emoji} {name} *** with the following content:\n\n {query}"})
        st.session_state.messages.append({"role": "assistant", "content": "⚠️ I am not allowed to do this without your approval💥. Do you allow me to call the tool?"})
    else:
        st.session_state.messages.append({"role": "assistant", "content": f"🛠️ Now calling the tool: *** {emoji} {name} *** with the following content:\n\n {query}"})
    return dangerToolCalled


def cancel_tool_use_with_message(graph, config):
    ai_message = "Action canceled."
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    answer = "No tool user"
    snapshot = graph.get_state(config)
    existing_message = snapshot.values["messages"][-1]
    response_metadata_dict = {"finish_reason": "user interrupt"}
    new_messages = [
        ToolMessage(content=answer, tool_call_id=existing_message.tool_calls[0]["id"]),
        AIMessage(content=answer, response_metadata=response_metadata_dict),
    ]
    graph.update_state(
        config,
        {"messages": new_messages},
    )


def handle_confirmation(graph, config):
    if st.button("✅ Yes"):
        st.session_state.assistant_action = True
        st.session_state.awaiting_confirmation = False
        st.rerun()
    if st.button("❌ No"):
        cancel_tool_use_with_message(graph, config)
        st.session_state.awaiting_confirmation = False
        st.rerun()


# Check for user input
if prompt := st.chat_input("what is up?"):
    if st.session_state.awaiting_confirmation:
        st.session_state.messages.append({"role": "user", "content": prompt})
        ai_message = "I was awaiting confirmation. Please press the 'OK' button to proceed."
        st.session_state.messages.append({"role": "assistant", "content": ai_message})
    else:
        user_reaction = {"messages": ("user", prompt)}
        st.session_state.messages.append({"role": "user", "content": prompt})

        events = graph.stream(user_reaction, config, stream_mode="values")
        for event in events:
            process_event(event)

# Check if the assistant action should be performed
if st.session_state.assistant_action:
    perform_assistant_action()

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if(st.session_state.awaiting_confirmation):
    handle_confirmation(graph, config)
