from pydivar.config_schema import ConfigManager
from pydivar.core import get_posts_byCategory, get_post_info
from typing import Any
import asyncio 
from loguru import logger
import pandas as pd
import os

## config path
config_path = "config.json"
config = ConfigManager.read_config_file(config_path, make_IfNotExist=False)
###


async def runner():
    all_posts = []
    start = config.general.start_page
    end = config.general.end_page
    cities = config.general.city_codes
    category = config.general.category
    assert end > start, "start_page must be lower than end_page"
    posts: list[dict[str, Any]] = await get_posts_byCategory(start, end, cities, category )
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
    result = asyncio.run(runner())
    output_path = config.general.output_path
    df = pd.DataFrame(result)
    df.to_excel(output_path, mode='a', header= not os.path.exists(output_path))
    df_read = pd.read_excel(output_path)
    df_read.drop_duplicates(inplace=True)
    df_read.to_excel(output_path, mode='a', header= not os.path.exists(output_path))
    logger.success(f"result saved to {output_path}")
    
if __name__ == "__main__":
    main()