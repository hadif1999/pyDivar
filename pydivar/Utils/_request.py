from typing import Any
from httpx import AsyncClient, Response, AsyncHTTPTransport, Timeout
from httpx import RequestError
from loguru import logger


class AsyncRequest:
    def __init__(self, retries: int = 5, 
                 timeout: int = 10, BaseUrl: str = "", 
                 validate_response: bool = True, **kwargs) -> None:
        self._transport = AsyncHTTPTransport(retries=retries)
        self._timeout = Timeout(timeout, connect=timeout+5, read=timeout)
        self._BaseUrl = BaseUrl
        self._validate_response = validate_response
        
        
    def __call__(self, retries: int = 5, 
                 timeout: int = 10, BaseUrl: str = "") -> Any:
        self._transport = AsyncHTTPTransport(retries=retries)
        self._timeout = Timeout(timeout, connect=timeout+5, read=timeout)
        self._BaseUrl = BaseUrl
        
    

    async def _aget(self, _endpoint:str = '', **kwargs) -> Response:
        async with AsyncClient(transport=self._transport, 
                               timeout=self._timeout, http2=True,
                               base_url=self._BaseUrl) as client:
            res = await client.get(_endpoint, **kwargs)
            if self._validate_response: self.validate_response(res)
        return res
    
    
    async def _apost(self, _endpoint: str = '', **kwargs) -> Response:
        async with AsyncClient(transport=self._transport,
                               timeout=self._timeout, http2=True,
                               base_url=self._BaseUrl) as client:
            res = await client.post(_endpoint, **kwargs)
            if self._validate_response: self.validate_response(res)
        return res
    
    
    @staticmethod
    def validate_response(response: Response, ok_status_code: int = 200) -> None:
        status_code = response.status_code
        if status_code not in range(ok_status_code, ok_status_code + 100):
            response = response.text
            msg = f"something wrong with response status code, {status_code=}, {response=}"
            logger.error(msg)
            raise StatusCodeError(msg, status_code)
            
            
class StatusCodeError(Exception):
    def __init__(self, msg: str, code: int) -> None:
        self.msg = msg
        self.code = code
        
        
    def __str__(self) -> str:
        return self.msg
            
        