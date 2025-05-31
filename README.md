# 🤖 LLM-based Industrial Automation Integration Platform

This project integrates Large Language Models (LLMs) into industrial automation workflows, allowing users to control manufacturing equipment through natural language commands. The system leverages Asset Administration Shells (AAS), Modbus TCP, and a Streamlit web interface to offer an end-to-end smart manufacturing control environment.

---

## 📁 Project Structure

```
├── AI_Agent/              # LLM-powered Streamlit interface and tool invoker
├── BaSyxMinimal/          # Eclipse BaSyx-based AAS Registry & Submodel Server
├── mcp_server.py          # FastMCP server with Modbus-based PLC control tools
├── research_code.ipynb    # Jupyter Notebook for experiments and evaluations
```

---

## 🧠 Key Features

- **Natural Language Command Execution**: Use LLMs to interpret user instructions and map them to the correct control tools.
- **AAS Integration**: Access and interact with digital twins using Eclipse BaSyx.
- **Real-Time Equipment Control**: Control PLC-connected devices via Modbus TCP.
- **Streamlit Interface**: Web-based GUI for intuitive human-AI interaction.
- **Experimental Toolkit**: Jupyter-based evaluation of model-generated code, tool usage, and system performance.

---

## 🚀 Getting Started

### 1. Set up the Python environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r AI_Agent/requirements.txt
```

### 2. Run the FastMCP control server

```bash
python mcp_server.py
```

### 3. Launch the Streamlit UI

```bash
cd AI_Agent
streamlit run streamlitChat.py
```

### 4. Start the AAS Server (Docker)

```bash
cd BaSyxMinimal
docker-compose up -d
```

---

## 🔧 System Architecture

```
[User]
  ↓
[Streamlit LLM Agent]
  ↓
[FastMCP Tool Server] ←→ [PLC Equipment]
  ↓
[Eclipse BaSyx AAS Registry]
```

---

## 📊 Research & Evaluation

The `research_code.ipynb` notebook contains experiments and evaluation tasks related to:
- LangChain-based tool reasoning
- LLM-generated control scripts
- Multi-model evaluation (GPT-4o, Claude 4, Gemini, etc.)


---

_This README was inspired by the LLM4IAS project._
