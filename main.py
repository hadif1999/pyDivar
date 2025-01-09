from pydivar.config_schema import ConfigManager
from pydivar.core import get_posts_byCategory, get_post_info
from typing import Any
import asyncio 
from loguru import logger
import pandas as pd

## config path
config_path = "config.json"
config = ConfigManager.read_config_file(config_path, make_IfNotExist=False)
###


async def run():
    all_posts = []
    posts: list[dict[str, Any]] = await get_posts_byCategory(1, 2)
    for post in posts:
        post_temp: dict[str, Any] = post.copy()
        token = post["token"]
        try: 
            post_info_data: dict[str, Any]  = await get_post_info(token)
        except Exception as e: 
            logger.error(f"exception {e} thrown, returning all we could get, exiting")
            break
        post_temp.update(post_info_data)
        logger.debug(f"done for {post_temp["link"]}")
        all_posts.append(post_temp)
    return all_posts
        
        
def main():
    result = asyncio.run(run())
    df = pd.DataFrame(result)
    df.to_csv("output.csv")
    # logger.info(result)
    
if __name__ == "__main__":
    main()