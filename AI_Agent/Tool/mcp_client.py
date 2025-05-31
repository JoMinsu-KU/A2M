import logging
from fastmcp import Client
import json

logger = logging.getLogger(__name__)


#Replace with the actual MCP server address.
MCP_URL = "http://192.168.0.79:9000/mcp"
def get_client():
    logger.debug("Creating MCP client instance.")
    return Client(MCP_URL)

# Start process
async def start_manufacturing():
    try:
        async with get_client() as client:
            logger.info("Calling MCP tool: start_manufacturing")
            response = await client.call_tool("start_manufacturing", {"value": 1})
            logger.info(f"Response from start_manufacturing: {response}")
            return response
    except Exception as e:
        logger.error(f"Error in start_manufacturing: {e}", exc_info=True)
        raise

# Set coil turns.
async def set_coil_turn(turn: int):
    try:
        async with get_client() as client:
            logger.info(f"Calling MCP tool: set_coil_turn with turn={turn}")
            response = await client.call_tool("set_coil_turn", {"value": turn})
            logger.info(f"Response from set_coil_turn: {response}")
            return response
    except Exception as e:
        logger.error(f"Error in set_coil_turn: {e}", exc_info=True)
        raise

# Calculate the number of turns based on the target torque.
async def calculate_required_turns(torque: int):
    try:
        async with get_client() as client:
            logger.info(f"Calling MCP tool: calculate_required_turns_make_afpm with torque={torque}")
            response = await client.call_tool("calculate_required_turns_make_afpm", {"value": torque})
            logger.info(f"Response from calculate_required_turns_make_afpm: {response}")
            return response
    except Exception as e:
        logger.error(f"Error in calculate_required_turns: {e}", exc_info=True)
        raise

# Retrieve submodel.
async def get_submodels(process_name: str):
    try:
        async with get_client() as client:
            logger.info(f"Calling MCP tool: get_submodels with process_name='{process_name}'")
            response = await client.call_tool("get_submodels", {"value": process_name})
            pretty_response = json.loads(response[0].text)
            final_result = json.dumps(pretty_response, indent=2, ensure_ascii=False)
            logger.info(f"Get Submodels Complete ")
            return final_result
    except Exception as e:
        logger.error(f"Error in get_submodels: {e}", exc_info=True)
        raise


# Check connectable processes.
async def check_available_processes():
    try:
        async with get_client() as client:
            logger.info("Calling MCP tool: check_available_processes")
            response = await client.call_tool("check_available_processes", {})
            pretty_response = json.loads(response[0].text)
            final_result = json.dumps(pretty_response,indent=2, ensure_ascii=False)
            logger.info(f"Get Available Process Info Complete ")
            return final_result
    except Exception as e:
        logger.error(f"Error in check_available_processes: {e}", exc_info=True)
        raise