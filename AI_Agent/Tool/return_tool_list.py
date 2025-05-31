from langchain.agents import Tool
from Tool.tool_wrapper import sync_tool_wrapper
from Tool.mcp_client import (
    start_manufacturing,
    set_coil_turn,
    calculate_required_turns,
    get_submodels,
    check_available_processes
)


import logging


logger = logging.getLogger(__name__)


def get_tools():
    logger.info("Loading tools for LangChain agent")
    tools = [
        Tool.from_function(
            name="start_manufacturing",
            description="Start the AFPM process (write 1 to the Modbus 30000 address)",
            func=sync_tool_wrapper(start_manufacturing)
        ),
        Tool.from_function(
            name="set_coil_turn",
            description="set coil turn. ex) 45",
            func=sync_tool_wrapper(set_coil_turn, param_name="turn")
        ),
        Tool.from_function(
            name="calculate_required_turns_make_afpm",
            description="Enter the target torque and it will calculate the number of turns required. 예: 5(Nm)",
            func=sync_tool_wrapper(calculate_required_turns, param_name="torque")
        ),
        Tool.from_function(
            name="get_submodels",
            description="Returns the features of the input process",
            func=sync_tool_wrapper(get_submodels, param_name="process_name")
        ),
        Tool.from_function(
            name="check_available_processes",
            description="Check which AAS-defined processes are currently reachable (ping + MCP check).",
            func=sync_tool_wrapper(check_available_processes)
        )
    ]
    return tools
