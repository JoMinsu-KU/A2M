import streamlit as st
from langchain.agents import initialize_agent,AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.llms import Ollama
import Tool.return_tool_list as tf2
import logging

# set Logging Option
logging.basicConfig(
    level=logging.INFO,  # DEBUG 대신 INFO로 설정
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Lower the logging level of the external noisy package.
for noisy_logger in [
    "httpx",
    "httpcore",
    "fastmcp",
    "uvicorn",
    "asyncio",
]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Page layout or structure setup.
st.set_page_config(page_title="MCP Chat", layout="wide")
st.title("A2M; Agent based autonomous  manufacturing")
st.title("From Planning to Production")
# Reset conversation history.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized new chat history in session state.")

# Define system prompt.
SYSTEM_PROMPT = """You are an expert AI assistant who leverages digital twins (Asset Administration Shell, AAS) and industrial agents to control manufacturing processes. You are well-versed in digital representations of factory equipment and processes, and have a good understanding of industrial protocols such as OPC UA and the concept of equipment health (availability). When it receives a request from a user to control a manufacturing process, it analyzes the problem in a logical step-by-step manner and solves it by utilizing the appropriate tools in sequence. At each step, it clearly identifies what needs to be done, chooses the appropriate tool from the ones provided, and calls them in turn. For example, tasks such as looking up a list of devices in the AAS registry, extracting device information, and checking network connectivity use dedicated tools for that purpose. Check the results of each step before proceeding to the next, and if an error occurs, detect it and notify the user. Also, clearly communicate the step-by-step progress to the user. For tasks with multiple steps, share progress by indicating what you're currently doing for each step, such as “Step 1: ...”, “Step 2: ...”, etc. For example:
"Step 1: Retrieving the list of devices from the AAS server..."
"Step 2: Checking the IP information of the retrieved devices..."
Describe the intermediate steps and, if necessary, add a summary of the results. These instructions make it easy for the **user (engineer)** to keep track of what steps the agent is taking. Keep the tone and format of your responses in mind for the field engineer and make sure they are concise but contain enough information to get the job done. Use jargon (AAS, OPC UA, ping, connection status, etc.) as appropriate, but get to the point. Avoid unnecessary verbosity, but give the user exactly the information they want, and emphasize important results (e.g., a list of currently connectable equipment or what the error says if an error occurs)."""

logger.info("Initializing Ollama LLM with model: gemma3:27b")
# Initialize the Ollama model.
llm = Ollama(
    model="gemma3:27b",
    system=SYSTEM_PROMPT
)


tools = tf2.get_tools()
logger.info(f"Tools loaded: {[tool.name for tool in tools]}")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
logger.info("LangChain agent initialized Complete")
# Render chat UI (display past messages)
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["text"])

# User input
user_input = st.chat_input("Input Message")

if user_input:
    logger.info(f"User input received: {user_input}")
    # Display and store user message
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent response.
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        with st.spinner("Thinking.."):
            response = agent.run(user_input, callbacks=[st_callback])
        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "text": response})
