from fastmcp import FastMCP
from pymodbus.client import ModbusTcpClient
import math
import requests
import subprocess
import platform
import aiohttp
import asyncio
import time
import logging
import base64

# 🔧 Set Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Option
mcp = FastMCP("PLC Controller")
PLC_IP = "192.168.0.79"
PLC_PORT = 502
AAS_Server_IP = "http://192.168.0.160:8081/submodels/"
REGISTRY_URL = "http://192.168.0.160:8081/shells"

def is_ping_successful(output: str) -> bool:
    output = output.lower()
    logger.info(output)
    return (
        "받음 = 1" in output or
        "0% 손실" in output
    ) and not (
        "연결할 수 없습니다" in output or
        "요청 시간이 만료되었습니다" in output
    )

def encode_manufacturing_process_url(process_name: str) -> str:
    url = f"https://iacf.kyungnam.ac.kr/ids/sm/1/0/{process_name}/ManufacturingProcess"
    encoded = base64.b64encode(url.encode("utf-8")).decode("utf-8")
    return encoded

@mcp.tool(description="Gets the features that correspond to the entered process.")
def get_submodels(value: str):
    logger.info(f"[get_submodels] Input: {value}")
    try:
        encoded_Process = encode_manufacturing_process_url(value)
        search_url = AAS_Server_IP + encoded_Process
        response = requests.get(search_url)
        logger.info(f"[get_submodels] Response code: {response.status_code}")
        return response.json()
    except Exception as e:
        logger.error(f"[get_submodels] Error: {e}", exc_info=True)
        return {"error": str(e)}

@mcp.tool(description="Start AFPM manufacturing Process")
def start_manufacturing(value: int):
    logger.info("[start_manufacturing] Starting process...")
    try:
        client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
        client.connect()
        client.write_coil(address=30978, value=True, slave=1)
        time.sleep(2)
        client.write_coil(address=30978, value=False, slave=1)
        client.close()
        logger.info("[start_manufacturing] Manufacturing started successfully.")
        return {"status": "Start Manufacturing Successfully"}
    except Exception as e:
        logger.error(f"[start_manufacturing] Error: {e}", exc_info=True)
        return {"error": str(e)}

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "1", ip],
            capture_output=True,
            encoding="cp949",
        )
        return is_ping_successful(result.stdout)
    except Exception as e:
        logger.error(f"[ping_host] Error pinging {ip}: {e}", exc_info=True)
        return False


@mcp.tool(description="Check which AAS processes are available (ping + MCP test)")
async def check_available_processes(_: dict = {}):
    logger.info("[Step 1] Extracting ID and IP Address details for registered process equipment!")
    try:
        response = requests.get(REGISTRY_URL)
        aas_list = response.json()["result"]
        logger.info(f"[Step 1] {len(aas_list)} AAS entries retrieved.")
    except Exception as e:
        logger.error("[Step 1] ❌ Failed to fetch AAS registry.", exc_info=True)
        return {
            "status": "error",
            "message": "Failed to fetch AAS list from registry.",
            "available": [],
            "unavailable": []
        }

    available = []
    unavailable = []

    logger.info("[Step 2] Proceed with probing individual process equipment")
    for aas in aas_list:
        if isinstance(aas, str):
            continue

        aas_name = aas.get("idShort", "Unnamed AAS")
        specific_ids = aas.get("assetInformation", {}).get("specificAssetIds", [])

        ip = next((s["value"] for s in specific_ids if s["name"] == "ip"), None)
        port = next((s["value"] for s in specific_ids if s["name"] == "port"), "9000")

        if not ip:
            logger.warning(f"[{aas_name}] ❌ Missing IP address.")
            unavailable.append({
                "aas_name": aas_name,
                "ip": None,
                "port": None,
                "status": "no_ip"
            })
            continue

        logger.debug(f"[{aas_name}] Pinging {ip}...")
        if not ping_host(ip):
            logger.warning(f"[{aas_name}] ❌ Ping failed ({ip})")
            unavailable.append({
                "aas_name": aas_name,
                "ip": ip,
                "port": port,
                "status": "ping_failed"
            })
            continue

        logger.info(f"[{aas_name}] ✅ Ping success ({ip}:{port})")
        available.append({
            "aas_name": aas_name,
            "ip": ip,
            "port": port,
            "status": "available"
        })

    result = {
        "status": "ok",
        "available": available,
        "unavailable": unavailable
    }

    logger.info("[Step 3] ✅ AAS process availability check completed.")
    return result


@mcp.tool(description="Set Coil Turn input value name is only turn")
def set_coil_turn(value: int):
    logger.info(f"[set_coil_turn] Setting turn: {value}")
    try:
        client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
        client.connect()
        client.write_register(address=10000, value=value, slave=1)
        client.close()
        logger.info(f"[set_coil_turn] Coil set to: {value}")
        return {"status": f"set Turn coil: {value}"}
    except Exception as e:
        logger.error(f"[set_coil_turn] Error: {e}", exc_info=True)
        return {"error": str(e)}

@mcp.tool(description="Enter target torque and return matching coil turn.")
def calculate_required_turns_make_afpm(
    value: int,
    radius_outer=0.25,
    radius_inner=0.05,
    B_g=1.2,
    current=15.0,
    k_winding=0.95
):
    logger.info(f"[calculate_required_turns] Calculating for torque: {value}")
    try:
        radius_avg = (radius_outer + radius_inner) / 2
        area = radius_outer**2 - radius_inner**2
        denominator = (2/3) * math.pi * k_winding * current * B_g * area * radius_avg

        if denominator == 0:
            raise ValueError("Denominator cannot be zero")

        N_turns = value / denominator
        logger.info(f"[calculate_required_turns] Turns needed: {N_turns}")
        return round(N_turns)
    except Exception as e:
        logger.error(f"[calculate_required_turns] Error: {e}", exc_info=True)
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("🚀 MCP Server starting...")
    mcp.run(transport="streamable-http", host="192.168.0.79", port=9000)