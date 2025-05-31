
# FastMCP server code begins here

from fastmcp import FastMCP
from pymodbus.client import ModbusTcpClient
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AFPMMotorProduction")

# Initialize FastMCP server
mcp = FastMCP(name="AFPMMotorProductionServer")

# Initialize Modbus client
modbus_client = ModbusTcpClient('192.168.1.50', port=502)

def connect_modbus():
    """Establish connection to Modbus server"""
    if not modbus_client.connected:
        try:
            modbus_client.connect()
            logger.info("Connected to Modbus server")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Modbus server: {e}")
            return False
    return True

@mcp.tool()
def coil_insertion(coil_id: str, position: str, force: float = 10.0) -> dict:
    """
    Insert a coil into the motor assembly.
    
    Args:
        coil_id: Unique identifier for the coil
        position: Target position for insertion (e.g., "top", "bottom", "side")
        force: Force to apply during insertion in Newtons
        
    Returns:
        Dictionary containing operation status and details
    """
    logger.info(f"Starting coil insertion process for coil {coil_id} at position {position} with force {force}N")
    
    if connect_modbus():
        try:
            # Simulate writing to PLC registers
            # Register 100: Coil insertion command (1 = start)
            # Register 101: Force value (scaled by 10)
            modbus_client.write_register(100, 1)
            modbus_client.write_register(101, int(force * 10))
            
            # Simulate process time
            time.sleep(2)
            
            # Read status register
            response = modbus_client.read_holding_registers(200, 1)
            status_code = response.registers[0] if response else 0
            
            if status_code == 1:
                result = {"status": "success", "message": f"Coil {coil_id} inserted successfully at {position}"}
            else:
                result = {"status": "error", "message": f"Failed to insert coil {coil_id}, error code: {status_code}"}
        except Exception as e:
            result = {"status": "error", "message": f"Modbus communication error: {str(e)}"}
    else:
        result = {"status": "error", "message": "Could not connect to PLC"}
    
    logger.info(f"Coil insertion result: {result}")
    return result

@mcp.tool()
def pressing(component_id: str, pressure: float, duration: float) -> dict:
    """
    Perform pressing operation on motor components.
    
    Args:
        component_id: Identifier for the component to be pressed
        pressure: Pressure to apply in bar
        duration: Duration of pressing operation in seconds
        
    Returns:
        Dictionary containing operation status and details
    """
    logger.info(f"Starting pressing operation for component {component_id} with {pressure} bar for {duration} seconds")
    
    if connect_modbus():
        try:
            # Simulate writing to PLC registers
            # Register 110: Pressing command (1 = start)
            # Register 111: Pressure value (scaled by 10)
            # Register 112: Duration in milliseconds
            modbus_client.write_register(110, 1)
            modbus_client.write_register(111, int(pressure * 10))
            modbus_client.write_register(112, int(duration * 1000))
            
            # Simulate process time (shorter than actual for demo)
            time.sleep(min(duration, 3))
            
            # Read status register
            response = modbus_client.read_holding_registers(210, 1)
            status_code = response.registers[0] if response else 0
            
            if status_code == 1:
                result = {
                    "status": "success", 
                    "message": f"Pressing operation completed for component {component_id}",
                    "actual_pressure": pressure * (0.95 + random.random() * 0.1),  # Simulate slight variation
                    "actual_duration": duration
                }
            else:
                result = {"status": "error", "message": f"Pressing operation failed, error code: {status_code}"}
        except Exception as e:
            result = {"status": "error", "message": f"Modbus communication error: {str(e)}"}
    else:
        result = {"status": "error", "message": "Could not connect to PLC"}
    
    logger.info(f"Pressing operation result: {result}")
    return result

@mcp.tool()
def cutting(wire_type: str, length: float, angle: float = 90.0) -> dict:
    """
    Cut wires or materials to specified length and angle.
    
    Args:
        wire_type: Type of wire or material to cut
        length: Length to cut in millimeters
        angle: Cutting angle in degrees (default 90°)
        
    Returns:
        Dictionary containing operation status and details
    """
    logger.info(f"Starting cutting operation for {wire_type} wire, length: {length}mm, angle: {angle}°")
    
    if connect_modbus():
        try:
            # Simulate writing to PLC registers
            # Register 120: Cutting command (1 = start)
            # Register 121: Length in 0.1mm
            # Register 122: Angle in 0.1 degrees
            modbus_client.write_register(120, 1)
            modbus_client.write_register(121, int(length * 10))
            modbus_client.write_register(122, int(angle * 10))
            
            # Simulate process time
            time.sleep(1.5)
            
            # Read status register
            response = modbus_client.read_holding_registers(220, 1)
            status_code = response.registers[0] if response else 0
            
            if status_code == 1:
                actual_length = length * (0.98 + random.random() * 0.04)  # Simulate cutting accuracy
                result = {
                    "status": "success", 
                    "message": f"Successfully cut {wire_type} wire",
                    "actual_length": round(actual_length, 2),
                    "actual_angle": angle
                }
            else:
                result = {"status": "error", "message": f"Cutting operation failed, error code: {status_code}"}
        except Exception as e:
            result = {"status": "error", "message": f"Modbus communication error: {str(e)}"}
    else:
        result = {"status": "error", "message": "Could not connect to PLC"}
    
    logger.info(f"Cutting operation result: {result}")
    return result

@mcp.tool()
def welding(joint_id: str, temperature: float, duration: float) -> dict:
    """
    Perform welding operation on specified joint.
    
    Args:
        joint_id: Identifier for the joint to be welded
        temperature: Welding temperature in Celsius
        duration: Duration of welding operation in seconds
        
    Returns:
        Dictionary containing operation status and details
    """
    logger.info(f"Starting welding operation for joint {joint_id} at {temperature}°C for {duration} seconds")
    
    if connect_modbus():
        try:
            # Simulate writing to PLC registers
            # Register 130: Welding command (1 = start)
            # Register 131: Temperature in Celsius
            # Register 132: Duration in 0.1 seconds
            modbus_client.write_register(130, 1)
            modbus_client.write_register(131, int(temperature))
            modbus_client.write_register(132, int(duration * 10))
            
            # Simulate process time (shorter than actual for demo)
            time.sleep(min(duration, 2.5))
            
            # Read status and temperature registers
            response = modbus_client.read_holding_registers(230, 2)
            if response:
                status_code = response.registers[0]
                actual_temp = response.registers[1]
                
                if status_code == 1:
                    result = {
                        "status": "success", 
                        "message": f"Welding completed for joint {joint_id}",
                        "actual_temperature": actual_temp,
                        "actual_duration": duration
                    }
                else:
                    result = {"status": "error", "message": f"Welding operation failed, error code: {status_code}"}
            else:
                result = {"status": "error", "message": "Failed to read welding status"}
        except Exception as e:
            result = {"status": "error", "message": f"Modbus communication error: {str(e)}"}
    else:
        result = {"status": "error", "message": "Could not connect to PLC"}
    
    logger.info(f"Welding operation result: {result}")
    return result

@mcp.tool()
def winding(coil_id: str, wire_gauge: float, turns: int, tension: float) -> dict:
    """
    Perform winding operation for motor coils.
    
    Args:
        coil_id: Identifier for the coil
        wire_gauge: Diameter of wire in millimeters
        turns: Number of turns to wind
        tension: Tension to apply during winding in Newtons
        
    Returns:
        Dictionary containing operation status and details
    """
    logger.info(f"Starting winding operation for coil {coil_id}: {turns} turns of {wire_gauge}mm wire at {tension}N tension")
    
    if connect_modbus():
        try:
            # Simulate writing to PLC registers
            # Register 140: Winding command (1 = start)
            # Register 141: Wire gauge in 0.01mm
            # Register 142: Number of turns
            # Register 143: Tension in 0.1N
            modbus_client.write_register(140, 1)
            modbus_client.write_register(141, int(wire_gauge * 100))
            modbus_client.write_register(142, turns)
            modbus_client.write_register(143, int(tension * 10))
            
            # Simulate process time based on number of turns
            process_time = min(turns / 10, 5)  # Cap at 5 seconds for demo
            time.sleep(process_time)
            
            # Read status registers
            response = modbus_client.read_holding_registers(240, 2)
            if response:
                status_code = response.registers[0]
                actual_turns = response.registers[1]
                
                if status_code == 1:
                    result = {
                        "status": "success", 
                        "message": f"Winding completed for coil {coil_id}",
                        "actual_turns": actual_turns,
                        "wire_used_meters": round(actual_turns * 0.15, 2)  # Simulate wire usage
                    }
                else:
                    result = {"status": "error", "message": f"Winding operation failed, error code: {status_code}"}
            else:
                result = {"status": "error", "message": "Failed to read winding status"}
        except Exception as e:
            result = {"status": "error", "message": f"Modbus communication error: {str(e)}"}
    else:
        result = {"status": "error", "message": "Could not connect to PLC"}
    
    logger.info(f"Winding operation result: {result}")
    return result

@mcp.tool()
def inspection_result(part_id: str, inspection_type: str = "visual") -> dict:
    """
    Retrieve inspection results for a specific part.
    
    Args:
        part_id: Identifier for the part to inspect
        inspection_type: Type of inspection (visual, electrical, dimensional)
        
    Returns:
        Dictionary containing inspection results
    """
    logger.info(f"Retrieving {inspection_type} inspection results for part {part_id}")
    
    inspection_types = ["visual", "electrical", "dimensional"]
    if inspection_type not in inspection_types:
        return {
            "status": "error", 
            "message": f"Invalid inspection type. Must be one of: {', '.join(inspection_types)}"
        }
    
    if connect_modbus():
        try:
            # Simulate reading from PLC registers
            # Register 150: Inspection command (2 = read results)
            # Register 151: Inspection type (1=visual, 2=electrical, 3=dimensional)
            inspection_type_code = inspection_types.index(inspection_type) + 1
            modbus_client.write_register(150, 2)
            modbus_client.write_register(151, inspection_type_code)
            
            # Simulate process time
            time.sleep(1)
            
            # Read inspection results
            response = modbus_client.read_holding_registers(250, 4)
            if response:
                status_code = response.registers[0]
                quality_score = response.registers[1]
                defect_count = response.registers[2]
                measurement = response.registers[3] / 100.0  # Scale to get actual value
                
                if status_code == 1:
                    # Determine pass/fail based on quality score
                    passed = quality_score >= 80
                    
                    result = {
                        "status": "success",
                        "part_id": part_id,
                        "inspection_type": inspection_type,
                        "passed": passed,
                        "quality_score": quality_score,
                        "defect_count": defect_count,
                        "measurement": measurement,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                else:
                    result = {"status": "error", "message": f"Inspection failed, error code: {status_code}"}
            else:
                result = {"status": "error", "message": "Failed to read inspection results"}
        except Exception as e:
            result = {"status": "error", "message": f"Modbus communication error: {str(e)}"}
    else:
        result = {"status": "error", "message": "Could not connect to PLC"}
    
    logger.info(f"Inspection result: {result}")
    return result

@mcp.tool()
def edit_coil_turn(coil_id: str, new_turns: int) -> dict:
    """
    Edit the number of turns for an existing coil.
    
    Args:
        coil_id: Identifier for the coil to modify
        new_turns: New number of turns to set
        
    Returns:
        Dictionary containing operation status and details
    """
    logger.info(f"Editing coil {coil_id} to have {new_turns} turns")
    
    if new_turns <= 0:
        return {"status": "error", "message": "Number of turns must be positive"}
    
    if connect_modbus():
        try:
            # First read current turns
            modbus_client.write_register(160, 3)  # 3 = read coil data
            time.sleep(0.5)
            
            response = modbus_client.read_holding_registers(260, 2)
            if response:
                current_turns = response.registers[0]
                
                # Now write new turns
                modbus_client.write_register(160, 4)  # 4 = edit coil
                modbus_client.write_register(161, new_turns)
                
                time.