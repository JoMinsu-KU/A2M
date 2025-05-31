# FastMCP server code begins here
import logging
from fastmcp import FastMCP
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# FastMCP server declaration
mcp = FastMCP(name="AFPMMotorProductionTypeServer")

# Modbus PLC Configuration
MODBUS_HOST = "192.168.1.50"
MODBUS_PORT = 502

# Define Modbus register addresses (dummy addresses for simulation)
REG_COIL_INSERTION_START = 100
REG_PRESSING_START = 101
REG_CUTTING_START = 102
REG_WELDING_START = 103
REG_WINDING_START = 104
REG_INSPECTION_STATUS = 200
REG_COIL_TURN_SETPOINT = 300

@mcp.tool()
def coil_insertion() -> str:
    """
    Initiates the coil insertion process on the production line.
    This typically involves activating pneumatic or servo systems to place a coil.
    Simulates writing to a PLC register to start the process.
    """
    logging.info("Attempting to initiate coil insertion process.")
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT} for coil insertion.")
            return f"Error: Could not connect to PLC for coil insertion."

        logging.info(f"Writing 1 to register {REG_COIL_INSERTION_START} to start coil insertion.")
        # Example: Write a '1' to a specific register to trigger the start
        result = client.write_register(REG_COIL_INSERTION_START, 1, unit=1) # unit=1 is common for Modbus TCP slave ID
        
        if result.isError():
            logging.error(f"Modbus error during coil insertion: {result}")
            return f"Error: Modbus communication failed during coil insertion command."
        
        logging.info("Coil insertion process started successfully via Modbus.")
        return "Coil insertion process started successfully."
    except ModbusException as e:
        logging.error(f"Modbus exception during coil insertion: {e}")
        return f"Error: Modbus exception during coil insertion - {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred during coil insertion: {e}")
        return f"Error: An unexpected error occurred during coil insertion - {e}"
    finally:
        if client.is_socket_open():
            client.close()
        logging.info("Modbus client connection closed for coil insertion.")

@mcp.tool()
def pressing() -> str:
    """
    Activates the pressing station for the current component.
    This could involve hydraulic or mechanical presses.
    Simulates writing to a PLC register to activate the press.
    """
    logging.info("Attempting to activate pressing station.")
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT} for pressing.")
            return f"Error: Could not connect to PLC for pressing."

        logging.info(f"Writing 1 to register {REG_PRESSING_START} to activate pressing.")
        result = client.write_register(REG_PRESSING_START, 1, unit=1)
        
        if result.isError():
            logging.error(f"Modbus error during pressing: {result}")
            return f"Error: Modbus communication failed during pressing command."
            
        logging.info("Pressing process activated successfully via Modbus.")
        return "Pressing process activated successfully."
    except ModbusException as e:
        logging.error(f"Modbus exception during pressing: {e}")
        return f"Error: Modbus exception during pressing - {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred during pressing: {e}")
        return f"Error: An unexpected error occurred during pressing - {e}"
    finally:
        if client.is_socket_open():
            client.close()
        logging.info("Modbus client connection closed for pressing.")

@mcp.tool()
def cutting() -> str:
    """
    Triggers the cutting mechanism for material processing.
    This could be for wires, laminations, or other raw materials.
    Simulates writing to a PLC register to start the cutting operation.
    """
    logging.info("Attempting to trigger cutting mechanism.")
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT} for cutting.")
            return f"Error: Could not connect to PLC for cutting."

        logging.info(f"Writing 1 to register {REG_CUTTING_START} to trigger cutting.")
        result = client.write_register(REG_CUTTING_START, 1, unit=1)

        if result.isError():
            logging.error(f"Modbus error during cutting: {result}")
            return f"Error: Modbus communication failed during cutting command."

        logging.info("Cutting mechanism triggered successfully via Modbus.")
        return "Cutting mechanism triggered successfully."
    except ModbusException as e:
        logging.error(f"Modbus exception during cutting: {e}")
        return f"Error: Modbus exception during cutting - {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred during cutting: {e}")
        return f"Error: An unexpected error occurred during cutting - {e}"
    finally:
        if client.is_socket_open():
            client.close()
        logging.info("Modbus client connection closed for cutting.")

@mcp.tool()
def welding() -> str:
    """
    Starts the welding process for joining components.
    Could be spot welding, laser welding, etc.
    Simulates writing to a PLC register to initiate welding.
    """
    logging.info("Attempting to start welding process.")
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT} for welding.")
            return f"Error: Could not connect to PLC for welding."

        logging.info(f"Writing 1 to register {REG_WELDING_START} to start welding.")
        result = client.write_register(REG_WELDING_START, 1, unit=1)

        if result.isError():
            logging.error(f"Modbus error during welding: {result}")
            return f"Error: Modbus communication failed during welding command."

        logging.info("Welding process started successfully via Modbus.")
        return "Welding process started successfully."
    except ModbusException as e:
        logging.error(f"Modbus exception during welding: {e}")
        return f"Error: Modbus exception during welding - {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred during welding: {e}")
        return f"Error: An unexpected error occurred during welding - {e}"
    finally:
        if client.is_socket_open():
            client.close()
        logging.info("Modbus client connection closed for welding.")

@mcp.tool()
def winding() -> str:
    """
    Initiates the coil winding process on the designated machine.
    This is a core process in motor manufacturing.
    Simulates writing to a PLC register to start the winding machine.
    """
    logging.info("Attempting to initiate winding process.")
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT} for winding.")
            return f"Error: Could not connect to PLC for winding."

        logging.info(f"Writing 1 to register {REG_WINDING_START} to start winding.")
        result = client.write_register(REG_WINDING_START, 1, unit=1)

        if result.isError():
            logging.error(f"Modbus error during winding: {result}")
            return f"Error: Modbus communication failed during winding command."

        logging.info("Winding process initiated successfully via Modbus.")
        return "Winding process initiated successfully."
    except ModbusException as e:
        logging.error(f"Modbus exception during winding: {e}")
        return f"Error: Modbus exception during winding - {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred during winding: {e}")
        return f"Error: An unexpected error occurred during winding - {e}"
    finally:
        if client.is_socket_open():
            client.close()
        logging.info("Modbus client connection closed for winding.")

@mcp.tool()
def inspection_result(component_id: str) -> dict:
    """
    Retrieves the latest inspection result for a given component ID from the PLC.
    Simulates reading a status register from the PLC and interpreting it.
    """
    logging.info(f"Attempting to retrieve inspection result for component ID: {component_id}.")
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT} for inspection result.")
            return {"component_id": component_id, "error": "Could not connect to PLC for inspection."}

        logging.info(f"Reading holding register {REG_INSPECTION_STATUS} for inspection status.")
        # Example: Read 1 holding register for status (0 = Fail, 1 = Pass, 2 = In Progress, etc.)
        result = client.read_holding_registers(REG_INSPECTION_STATUS, 1, unit=1)
        
        if result.isError():
            logging.error(f"Modbus error retrieving inspection result: {result}")
            return {"component_id": component_id, "error": "Modbus communication failed during inspection."}

        status_code = result.registers[0] if result.registers else -1 # Default to -1 if no registers
        
        status_map = {
            0: "Fail",
            1: "Pass",
            2: "In Progress",
        }
        status_text = status_map.get(status_code, "Unknown")
        
        mock_details = f"Mocked inspection data for component {component_id}. PLC raw status: {status_code}."
        if status_code == -1 and not result.registers:
             mock_details = f"No data read from PLC register {REG_INSPECTION_STATUS} for component {component_id}."
        
        logging.info(f"Inspection result for {component_id}: {status_text}, Details: {mock_details}")
        return {
            "component_id": component_id,
            "status": status_text,
            "raw_plc_value": status_code,
            "details": mock_details
        }
    except ModbusException as e:
        logging.error(f"Modbus exception retrieving inspection result: {e}")
        return {"component_id": component_id, "error": f"Modbus exception - {e}"}
    except Exception as e:
        logging.error(f"An unexpected error occurred retrieving inspection result: {e}")
        return {"component_id": component_id, "error": f"Unexpected error - {e}"}
    finally:
        if client.is_socket_open():
            client.close()
        logging.info(f"Modbus client connection closed for inspection result ({component_id}).")

@mcp.tool()
def edit_coil_turn(new_turn_count: int) -> str:
    """
    Updates the coil turn count setpoint on the winding machine PLC.
    The new_turn_count specifies the desired number of turns for the coil.
    Simulates writing this new setpoint to a PLC register.
    """
    logging.info(f"Attempting to edit coil turn count to: {new_turn_count}.")
    if not isinstance(new_turn_count, int) or new_turn_count < 0 or new_turn_count > 65535: # Assuming 16-bit register
        logging.warning(f"Invalid coil turn count: {new_turn_count}. Must be an integer between 0 and 65535.")
        return "Error: Invalid coil turn count. Must be an integer between 0 and 65535."

    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT, timeout=3)
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {MODBUS_HOST}:{MODBUS_PORT} for editing coil turn.")
            return f"Error: Could not connect to PLC for editing coil turn."

        logging.info(f"Writing {new_turn_count} to register {REG_COIL_TURN_SETPOINT} for coil turn setpoint.")
        result = client.write_register(REG_COIL_TURN_SETPOINT, new_turn_count, unit=1)

        if result.isError():
            logging.error(f"Modbus error editing coil turn: {result}")
            return f"Error: Modbus communication failed during coil turn update."
            
        logging.info(f"Coil turn count successfully updated to {new_turn_count} via Modbus.")
        return f"Coil turn count updated to {new_turn_count}."
    except ModbusException as e:
        logging.error(f"Modbus exception editing coil turn: {e}")
        return f"Error: Modbus exception during coil turn update - {e}"
    except Exception as e:
        logging.error(f"An unexpected error occurred editing coil turn: {e}")
        return f"Error: An unexpected error occurred during coil turn update - {e}"
    finally:
        if client.is_socket_open():
            client.close()
        logging.info("Modbus client connection closed for editing coil turn.")

# Starting the server
if __name__ == "__main__":
    # The host '192.168.1.108' is for the FastMCP server itself.
    # The Modbus PLC is assumed to be at '192.168.1.50'.
    mcp.run(transport="streamable-http", host="192.168.1.108", port=9000)

# FastMCP server code ends here