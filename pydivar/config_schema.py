from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from typing import Optional, Any
import os
from loguru import logger

class EndpointsConfig(BaseModel):
    contact_info: str = "/v8/postcontact/web/contact_info_v2/{pid}"
    cities: str = "/v8/places/cities?level=all"
    categories: str = "/v8/postlist/w/categories"
    post_data: str = "/v8/posts-v2/web/{pid}"
    search_by_category: str = "/v8/postlist/w/search"


class GeneralConfig(BaseModel):
    base_url: str = "https://api.divar.ir"
    endpoints: EndpointsConfig = EndpointsConfig()
    timeout: int = 10
    retries: int = 3
    AUTH_TOKEN: str 
    output_path: str
    start_page: int 
    end_page: int
    category: str
    city_codes: list[str|int]
    with_phone_number_only: bool


class Config(BaseSettings):
    general: GeneralConfig
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="pydivar__",
                                      env_file=".env", env_nested_delimiter="__")
    

class ConfigManager:
    __CONFIG: Optional[Config] = None
    
    
    @staticmethod
    def read_config_file(path:str, make_IfNotExist: bool = False) -> Config:
        import pathlib
        _path = pathlib.Path(path)
        if not _path.exists() and make_IfNotExist: # creating if not exists
            with open(_path, 'a') as file: 
                os.makedirs(_path.parent, exist_ok=True)
                _config = Config()
                data: str = _config.model_dump_json()
                file.write(data)
                __class__.__CONFIG = _config
                return _config
        else: 
            with open(_path, 'r') as file:
                logger.debug(f"reading config file with {path=}")
                _config = Config.model_validate_json(file.read())
                _category = _config.general.category
                _config.general.output_path = _config.general.output_path.format(category=_category)
                path_str = _config.general.output_path
                if "xlsx" not in path_str or not pathlib.Path(path_str).parent.exists():
                    raise ValueError("output file must be in 'xlsx' file format")
                __class__.__CONFIG = _config
                return _config
            
            
    @staticmethod
    def get_config(raise_ifNone: bool = True) -> Config:
        config = __class__.__CONFIG
        if config == None and raise_ifNone:
            raise ValueError("CONFIG object is None")
        return config
            
            
    @classmethod
    def update_config(cls, config: Config) -> Config:
        cls.__CONFIG = config
        return config
            
    
    


