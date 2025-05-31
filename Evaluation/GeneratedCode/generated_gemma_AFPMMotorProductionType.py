
# FastMCP server code begins here
from fastmcp import FastMCP
from pymodbus.client import ModbusTcpClient

mcp = FastMCP(name="AFPMMotorProductionServer")

# Dummy Modbus server details
MODBUS_IP = "192.168.1.50"
MODBUS_PORT = 502

def connect_to_modbus():
    """Connects to the Modbus TCP server."""
    try:
        client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)
        client.connect()
        return client
    except Exception as e:
        print(f"Error connecting to Modbus server: {e}")
        return None

def disconnect_from_modbus(client):
    """Disconnects from the Modbus TCP server."""
    if client:
        try:
            client.close()
        except Exception as e:
            print(f"Error disconnecting from Modbus server: {e}")

@mcp.tool()
def coill_insertion(coil_id: str) -> str:
    """
    Initiates the coil insertion process for a given coil ID.
    Simulates interaction with a Modbus device to control the coil insertion mechanism.
    """
    print(f"Initiating coil insertion for coil ID: {coil_id}")
    client = connect_to_modbus()
    if client:
        try:
            # Example: Write a register to start the coil insertion
            result = client.write_register(100, int(coil_id))  # Assuming coil_id can be converted to an integer
            if result:
                print(f"Coil insertion started for coil ID: {coil_id} (Modbus write successful)")
            else:
                print(f"Coil insertion failed for coil ID: {coil_id} (Modbus write failed)")
        except Exception as e:
            print(f"Error during coil insertion (Modbus): {e}")
        finally:
            disconnect_from_modbus(client)
    return f"Coil insertion initiated for {coil_id}"

@mcp.tool()
def pressing(pressure: float, duration: int) -> str:
    """
    Controls the pressing process with specified pressure and duration.
    Simulates interaction with a Modbus device to control the pressing mechanism.
    """
    print(f"Initiating pressing with pressure: {pressure} and duration: {duration} seconds")
    client = connect_to_modbus()
    if client:
        try:
            # Example: Write registers for pressure and duration
            result_pressure = client.write_register(101, int(pressure * 100))  # Scale pressure for integer representation
            result_duration = client.write_register(102, duration)
            if result_pressure and result_duration:
                print(f"Pressing started with pressure {pressure} and duration {duration} (Modbus write successful)")
            else:
                print(f"Pressing failed (Modbus write failed)")
        except Exception as e:
            print(f"Error during pressing (Modbus): {e}")
        finally:
            disconnect_from_modbus(client)
    return f"Pressing initiated with pressure {pressure} and duration {duration}"

@mcp.tool()
def cutting(cut_length: float) -> str:
    """
    Performs a cutting operation with the specified length.
    Simulates interaction with a Modbus device to control the cutting mechanism.
    """
    print(f"Initiating cutting with length: {cut_length}")
    client = connect_to_modbus()
    if client:
        try:
            # Example: Write a register for cut length
            result = client.write_register(103, int(cut_length * 100))  # Scale length for integer representation
            if result:
                print(f"Cutting initiated with length {cut_length} (Modbus write successful)")
            else:
                print(f"Cutting failed (Modbus write failed)")
        except Exception as e:
            print(f"Error during cutting (Modbus): {e}")
        finally:
            disconnect_from_modbus(client)
    return f"Cutting initiated with length {cut_length}"

@mcp.tool()
def welding(welding_current: float, welding_time: int) -> str:
    """
    Performs a welding operation with specified current and time.
    Simulates interaction with a Modbus device to control the welding mechanism.
    """
    print(f"Initiating welding with current: {welding_current} and time: {welding_time} seconds")
    client = connect_to_modbus()
    if client:
        try:
            # Example: Write registers for welding current and time
            result_current = client.write_register(104, int(welding_current * 100))  # Scale current for integer representation
            result_time = client.write_register(105, welding_time)
            if result_current and result_time:
                print(f"Welding started with current {welding_current} and time {welding_time} (Modbus write successful)")
            else:
                print(f"Welding failed (Modbus write failed)")
        except Exception as e:
            print(f"Error during welding (Modbus): {e}")
        finally:
            disconnect_from_modbus(client)
    return f"Welding initiated with current {welding_current} and time {welding_time}"

@mcp.tool()
def winding(winding_turns: int) -> str:
    """
    Performs a winding operation with the specified number of turns.
    Simulates interaction with a Modbus device to control the winding mechanism.
    """
    print(f"Initiating winding with {winding_turns} turns")
    client = connect_to_modbus()
    if client:
        try:
            # Example: Write a register for winding turns
            result = client.write_register(106, winding_turns)
            if result:
                print(f"Winding initiated with {winding_turns} turns (Modbus write successful)")
            else:
                print(f"Winding failed (Modbus write failed)")
        except Exception as e:
            print(f"Error during winding (Modbus): {e}")
        finally:
            disconnect_from_modbus(client)
    return f"Winding initiated with {winding_turns} turns"

@mcp.tool()
def inspection_result(result: str) -> str:
    """
    Records the inspection result.
    Simulates logging the inspection result to a database or file.
    """
    print(f"Recording inspection result: {result}")
    client = connect_to_modbus()
    if client:
        try:
            # Example: Write a register to store the inspection result code
            result_code = 0
            if result == "Pass":
                result_code = 1
            elif result == "Fail":
                result_code = 0
            result = client.write_register(107, result_code)
            if result:
                print(f"Inspection result {result} recorded (Modbus write successful)")
            else:
                print(f"Inspection result recording failed (Modbus write failed)")
        except Exception as e:
            print(f"Error recording inspection result (Modbus): {e}")
        finally:
            disconnect_from_modbus(client)
    return f"Inspection result '{result}' recorded."

@mcp.tool()
def edit_coil_turn(coil_id: str, new_turns: int) -> str:
    """
    Edits the number of turns for a specific coil.
    Simulates updating the coil parameters in a database or PLC.
    """
    print(f"Editing coil {coil_id} to {new_turns} turns")
    client = connect_to_modbus()
    if client:
        try:
            # Example: Write registers for coil ID and new turns
            result_id = client.write_register(108, int(coil_id))
            result_turns = client.write_register(109, new_turns)
            if result_id and result_turns:
                print(f"Coil {coil_id} edited to {new_turns} turns (Modbus write successful)")
            else:
                print(f"Coil editing failed (Modbus write failed)")
        except Exception as e:
            print(f"Error editing coil (Modbus): {e}")
        finally:
            disconnect_from_modbus(client)
    return f"Coil {coil_id} edited to {new_turns} turns."

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="192.168.1.108", port=9000)

# FastMCP server code ends here