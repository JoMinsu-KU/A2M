# 🤖 AI Agent + FastMCP Integration Server

This project implements an API-like FastMCP server to support AI agents in discovering and invoking available tools dynamically.  
It provides core interfaces for agent reasoning and is designed to operate as part of a smart manufacturing control architecture.

---

## 🧠 Project Overview

- Built using [`FastMCP`](https://github.com/jlowin/fastmcp)
- Exposes tools to AI agents for reasoning-based orchestration
- Loads available tools dynamically from a configured registry or directory
- Includes a Streamlit frontend for chat-style interaction
- Designed for use with agents that interpret AAS metadata and generate FastMCP-compatible tool calls

---

## 📁 Folder Structure

```
AI_Agent/
├── mcp_server.py              # Main FastMCP server with tool registration
├── streamlitChat.py           # Streamlit-based frontend for agent interaction
├── requirements.txt           # Python dependencies
├── Tool/
│   ├── mcp_client.py          # Client for querying tools from another MCP server
│   ├── return_tool_list.py    # Tool that returns available tool metadata
│   └── tool_wrapper.py        # Wrapper for registering tools dynamically
├── test_main.http             # REST testing script (for debugging endpoints)
├── .idea/                     # PyCharm project settings
└── README.md                  # This file
```

---

## ⚙️ How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the FastMCP tool server:
   ```bash
   python mcp_server.py
   ```

3. (Optional) Start Streamlit-based agent UI:
   ```bash
   streamlit run streamlitChat.py
   ```

---

## 🧩 Key Functionalities

- `return_tool_list`: Returns the list of registered tools (idShort, parameters, etc.)
- `tool_wrapper`: Wraps and registers tools with FastMCP dynamically
- `mcp_client`: Allows agent to communicate with other MCP servers to pull tool metadata

---

## 🔌 Use Case

This server acts like a lightweight **API service** for AI agents that generate or execute FastMCP-based process plans.  
Agents can:

- Query which tools are currently available
- Execute tools via HTTP
- Use AAS-derived context to plan actions

This setup complements the FastMCP code generation/evaluation pipeline by providing a runtime environment for agent reasoning.

---

## 📬 Contact

For questions or collaboration, please contact:  
**[jms663100@kyungnam.ac.kr](mailto:jms663100@kyungnam.ac.kr)**
