from typing import Callable, TypeVar, Awaitable, Any
from functools import wraps
from loguru import logger
import time
import asyncio
from urllib.parse import urlencode, urljoin


Function = TypeVar('Function', bound=Callable[..., Awaitable[Any] | Any])

def log_exec_time(func: Function) -> Function:
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = await func(*args, **kwargs)  # Await the async function
        t2 = time.perf_counter()
        exec_time = t2 - t1
        msg = f"Execution time for {func.__name__}: {exec_time:.4f} seconds"
        logger.debug(msg)
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)  # Call the sync function
        t2 = time.perf_counter()
        exec_time = t2 - t1
        msg = f"Execution time for {func.__name__}: {exec_time:.4f} seconds "
        logger.debug(msg)
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper  # Return async wrapper for async functions
    else:
        return sync_wrapper  # Return sync wrapper for sync functions
    

def read_proxy_db_json(path: str = "data/proxies/proxy.json"):
    import json
    with open(path, 'r') as file:
        proxy_db: dict[str, Any] = json.loads(file.read())
    if "active" not in proxy_db or proxy_db["active"]=={}: return None
    return proxy_db["active"]


def get_ip_from_proxy(proxy: str):
    if '@' in proxy:
        ip = proxy.split('@')[1].split(':')[0]
    else:
        ip = proxy.split(':')[0]
    return ip


def add_query_params(base_url, params):
    """
    Add query parameters to a base URL if params is a valid dictionary.

    Args:
        base_url (str): The base URL.
        params (dict): A dictionary of query parameters to append. Ignored if not a dictionary.

    Returns:
        str: The complete URL with query parameters, or the base URL if params is invalid.
    """
    if not isinstance(params, dict):  # Check if params is a dictionary
        return base_url

    # Convert dictionary to query string
    query_string = urlencode(params)

    # Return base URL with query parameters
    if query_string:
        return f"{base_url}?{query_string}" if '?' not in base_url else f"{base_url}&{query_string}"
    return base_url

    
    

        