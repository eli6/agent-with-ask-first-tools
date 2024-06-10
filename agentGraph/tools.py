from langchain.tools import tool


@tool
def send_email_message(query: str) -> str:
    """Create and send email message"""
    return 'Email sent successfully.'



@tool
def create_email_draft(query: str) -> str:
    """Create an email draft without sending it"""
    return 'Email draft created successfully.'



safe_tools = [create_email_draft]
unsafe_tools = [send_email_message]


#map tool to emoji for spicing up the streamlit UI a bit:
tool_emoji = {
    "create_email_draft": "📧",
    "send_email_message": "📩"
}

unsafe_tool_names = {tool.name for tool in unsafe_tools}
