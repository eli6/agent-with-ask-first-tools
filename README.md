
---

# 🤖 Streamlit AI Agent with two tool nodes: 'Safe' and 'Unsafe/Ask-first' tools

Welcome to the Streamlit AI Agent App! This app leverages LangGraph to create an interactive AI agent with dummy tools for creating email drafts and sending emails. 🚀

It is a demonstration of the following scenario: the tools are organised into 'safe' tools that the agent can use right away, and 'unsafe' tools where the agent has to ask the human-in-the-loop before proceeding.

## Features

- 🌟 **AI Agent**: An AI-powered assistant that helps you draft and send emails.
- ✉️ **Create Email Drafts**: Dummy function for sending email drafts (here you could import the Gmail tools for example for real world usage)
- 📧 **Send Emails**: Dummy function for sending emails

## Installation

Follow these steps to set up the app on your local machine:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/eli6/agent-with-ask-first-tools.git
    cd agent-with-ask-first-tools
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv 
    ```
    (or python3)

3. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Make sure your MistralAI (or other provider) key is set in your environment.
 
 To run the app out of the box, make sure your MISTRAL_API_KEY is set to your API key value.

6. **Run the app**:
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Launch the app**: Open your web browser and go to `http://localhost:8501`.

2. **Interact with the AI Agent**:
    - **Creating Email Drafts**: Type your prompt to create a dummy email draft.
    - **Sending Emails**: Confirm the draft and send the email.

## Code Overview

## Contributions

Feel free to fork this repository and submit pull requests. Contributions are always welcome! 🌟

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Streamlit**: For providing an awesome framework for creating interactive web apps.
- **LangGraph**: For the powerful graph-based language modeling.

Enjoy using the Streamlit AI Agent App! 😊
