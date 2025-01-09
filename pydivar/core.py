from httpx import Response
import json
from loguru import logger
from typing import Any, Annotated


async def get_posts_byCategory(start_page:int = 1, end_page:int = 5, 
                         city_codes:list[int|str] = ["1"], category: str = "ROOT")-> list[dict[str, Any]]:
    from pydivar._core import _get_posts_byCategory
    all_posts_data = []
    for page_num in range(start_page, end_page):
        posts = await _get_posts_byCategory(page_num, category, city_codes)
        for widget in posts["list_widgets"]:
            post = widget['data']
            token, title = post["token"], post["title"]
            district_per = post["action"]["payload"]["web_info"]["district_persian"]
            city_per = post["action"]["payload"]["web_info"]["city_persian"]
            link = f"https://divar.ir/v/{title}/{token}"
            all_posts_data.append({"token": token, "title": title,
                                   "link": link, "city_persian": city_per,
                                   "district_persian": district_per})
    return all_posts_data


def _get_section(section_name: str, post_detail: dict)-> dict|None:
    selected_section = None
    for section in post_detail["sections"]:
        if section["section_name"] == section_name:
            selected_section = section
            return selected_section
    return selected_section


def _get_images(_post_detail: dict):
    image_section = _get_section("IMAGE", _post_detail)
    if not image_section: return None
    images = [item["image"]["url"] 
    for item in image_section["widgets"][0]["data"]["items"]]
    return images


def _get_categories(_post_detail: dict):
    section_type = "BREADCRUMB"
    breadcrump_section = _get_section(section_type, _post_detail)
    if not breadcrump_section: return None 
    for widget in breadcrump_section["widgets"]:
        if widget['widget_type'] == section_type:
            items = widget["data"].get('parent_items')
            categories = [{"fa": item["title"], 
            "eng":item["action"]["payload"]['search_data']["form_data"]["data"]["category"]["str"]["value"]}
            for item in items]
            return categories    


def _get_descriptions(_post_detail: dict):
    section_name = "DESCRIPTION"
    description_section = _get_section(section_name, _post_detail)
    widgets = description_section["widgets"]
    titles = [widget["data"]["text"] for widget in widgets 
              if widget['widget_type'] == 'TITLE_ROW']
    descriptions = [widget["data"]["text"] for widget in widgets 
                    if widget['widget_type'] == 'DESCRIPTION_ROW']
    data = dict(zip(titles, descriptions))
    logger.debug(data)
    return data



def _get_features_data(_post_detail: dict):
    section_name = 'LIST_DATA'
    features_section = _get_section(section_name, _post_detail)
    if not features_section: return None
    widgets: list = features_section["widgets"]
    all_features = {"features_group": []} # holds all features
    for widget in widgets:
        match widget["widget_type"]: 
            case 'GROUP_INFO_ROW':
                items = widget["data"]["items"]
                features = {item["title"]:item["value"] for item in items}
                all_features.update(features)
            case 'UNEXPANDABLE_ROW':
                item: dict = widget["data"]
                all_features.update({item["title"]: item.get("value")})
            case 'GROUP_FEATURE_ROW':
                data = widget["data"]
                if "action" in data: # if more details page exists 
                    sub_widgets: list = data["action"]["payload"]['modal_page']["widget_list"]
                    for sub_widget in sub_widgets:
                        match sub_widget["widget_type"]:
                            case 'UNEXPANDABLE_ROW':
                                sub_data: dict = sub_widget["data"]
                                all_features.update({sub_data["title"]: sub_data.get("value")})
                            case 'FEATURE_ROW':
                                sub_data: dict = sub_widget["data"]
                                all_features["features_group"].append(sub_data.get("title"))    
                else: 
                    items = data["items"]        
                    all_features["features_group"]+=[item["title"] for item in items]
                    all_features["features_group"] = list(set(all_features["features_group"]))
    return all_features  


def _decode_response(response: Response) -> dict:
    encode_type = response.headers.get("Content-Encoding")
    match encode_type:
        case 'br':
            import brotli
            decompressed_data = brotli.decompress(response.content).decode("utf-8")
        case 'gzip':
            import gzip
            decompressed_data = gzip.decompress(response.content).decode("utf-8")
        case "deflate":
            import zlib
            decompressed_data = zlib.decompress(response.content).decode("utf-8")
        case _:
            logger.error(f"encoding type {encode_type} not found")
            raise ValueError(f"encoding type {encode_type} not found")
    try:
        json_data = json.loads(decompressed_data)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
    return json_data


async def get_contact_info(pid:str, throw_exception: bool = False):
    from pydivar._core import _get_contact_info
    response = await _get_contact_info(pid)
    try: 
        json_response = _decode_response(response)
    except Exception as e:
        logger.error(f"exception {e} thrown")
        if throw_exception: raise e
        json_response = response.json()
    return json_response


async def get_phone_number(pid:str, throw_exception: bool = False):
    contact_info = await get_contact_info(pid, throw_exception)
    for widget in contact_info["widget_list"]:
        if "CALL_PHONE" in json.dumps(widget):
            phone_number = widget["data"]["action"]["payload"]["phone_number"]
            return phone_number
        else: 
            phone_number = widget["data"]["value"]
            return phone_number


async def get_post_info(token: str)-> dict[str, Any]:
    from pydivar._core import _get_post_info
    post_detail = await _get_post_info(token)
    post_seo_detail = post_detail["seo"]["post_seo_schema"]
    geo_data = post_seo_detail.get("geo")
    if geo_data: 
        lat = post_seo_detail.get("latitude")
        long = post_seo_detail.get("longitude") 
    else: lat=long=None
    price = post_detail["webengage"]["price"]
    images = _get_images(post_detail)
    categories = _get_categories(post_detail)
    descs = _get_descriptions(post_detail)
    features = _get_features_data(post_detail)
    phone = await get_phone_number(token)
    post_data = {"lat":lat, "long":long, "price":price, "images": images, 
                 "categories":categories, "descriptions": descs,
                 "features": features, "phone": phone}
    return post_data
    


    