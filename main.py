from pydivar.config_schema import ConfigManager
from pydivar.core import get_posts_byCategory, get_post_info
from typing import Any
import asyncio 
from loguru import logger
import pandas as pd
import os
import pathlib

## config path
config_path = "config.json"
config = ConfigManager.read_config_file(config_path, make_IfNotExist=False)
###

def get_old_fetched_posts(column: str) -> list[str|int]|None:
    output_path = config.general.output_path
    if pathlib.Path(output_path).is_file():
        titles: list[str|int] = pd.read_excel(output_path)[column].to_list()
        return titles
    

async def runner():
    fetched_posts = []
    start = config.general.start_page
    end = config.general.end_page
    cities = config.general.city_codes
    category = config.general.category
    assert end > start, "start_page must be lower than end_page"
    old_titles = get_old_fetched_posts("title")
    posts: list[dict[str, Any]] = await get_posts_byCategory(start, end, cities, category )
    logger.info(f"total number of posts to fetch: {len(posts)}")
    for post in posts:
        if old_titles and post["title"] in old_titles: 
            logger.info(f"ignoring {post['link']} as it already exists")
            continue
        post_temp: dict[str, Any] = post.copy()
        token = post["token"]
        try: 
            post_info_data: dict[str, Any]  = await get_post_info(token)
        except Exception as e: 
            if 'widget_list' in e.__str__(): 
                logger.error(f"exception {e} thrown, returning all we got, exiting")
                break
            else: 
                logger.error(f"exception {e} thrown, ignoring post {post["link"]}")
                continue
        post_temp.update(post_info_data)
        logger.debug(f"done for {post_temp["link"]}")
        fetched_posts.append(post_temp)
    logger.info(f"{len(fetched_posts)} posts fetched from total {len(posts)}")
    return fetched_posts
        
        
def main():
    result = asyncio.run(runner())
    output_path:str = config.general.output_path # xlsx file format
    df = pd.DataFrame(result)
    output_path_csv = output_path.replace("xlsx", "csv")
    df.to_csv(output_path_csv, mode='a', 
              header= not os.path.exists(output_path_csv), index=False)
    df_read = pd.read_csv(output_path_csv)
    ### cleaning data
    df_read.reset_index(drop=True, inplace=True)
    df_read.drop_duplicates(inplace=True)
    if config.general.with_phone_number_only: 
        df_read = df_read[df_read["phone"].astype("string").str.isalnum()]
        df_read.reset_index(drop=True, inplace=True)
    cols = config.general.columns
    if cols: df_read = df_read[cols]
    ########
    df_read.to_excel(output_path, index=False,
                     header=True)
    logger.success(f"result saved to {output_path}")
    
if __name__ == "__main__":
    main()