import asyncio
import logging

logger = logging.getLogger(__name__)


def sync_tool_wrapper(async_func, param_name=None):
    def wrapper(input):
        try:
            logger.info(f"Calling tool: {async_func.__name__}")
            logger.debug(f"Input received: {input}, param_name: {param_name}")

            # Handle input if param_name exists.
            if param_name:
                # Convert to int only if it looks like a number.
                if isinstance(input, str) and input.isdigit():
                    val = int(input)
                    logger.debug(f"Converted input to int: {val}")
                else:
                    val = input
                result = asyncio.run(async_func(val))
            else:
                result = asyncio.run(async_func())

            return result
        except Exception as e:
            logger.error(f"Error in tool '{async_func.__name__}': {e}", exc_info=True)
            return f"❌ Exception: {e}"

    return wrapper

