from typing import Literal
from mtrest.Utils._request import AsyncRequest
from mtrest.Utils.utils import log_exec_time
from mtrest.config_schema import ConfigManager

_req_conf = ConfigManager.get_config().general

@log_exec_time
async def get_myIP_ipify(ver: Literal[4, 6] = 4):
    """get my current ip by ipify

    Args:
        ver (Literal[4, 6], optional): _description_. Defaults to 4.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """    
    url_v4 = "https://api.ipify.org"
    url_v6 = "https://api6.ipify.org"
    match ver:
        case 4: req = AsyncRequest(BaseUrl=url_v4, retries=_req_conf.retries,
                                   timeout=_req_conf.timeout)
        case 6: req = AsyncRequest(BaseUrl=url_v6, retries=_req_conf.retries,
                                   timeout=_req_conf.timeout)
        case _: raise ValueError("ip version can be 4 or 6")
    res = await req._aget()
    ip = res.text.strip()
    return ip 


@log_exec_time
async def get_IP_location(ip_addr: str):
    """get ip location by ip-api.com

    Args:
        ip_addr (str): ip address

    Returns:
        dict
    """    
    base_url = "http://ip-api.com/json/"
    req = AsyncRequest(BaseUrl=base_url, retries=_req_conf.retries,
                       timeout=_req_conf.timeout)
    res = await req._aget(ip_addr)
    return res.json()


@log_exec_time
async def randomPhoneNumber_for_region(region_code: str):
    from faker import Faker
    phone_base = Faker().basic_phone_number()
    from phonenumbers.phonenumberutil import country_code_for_region
    prefix = country_code_for_region(region_code)
    phone_number = f"+{prefix}{phone_base}"
    return phone_number
    
