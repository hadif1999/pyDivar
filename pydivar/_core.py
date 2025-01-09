from pydivar.Utils._request import AsyncRequest
from pydivar.config_schema import ConfigManager

config = ConfigManager.get_config()

_request = AsyncRequest(retries=config.general.retries, timeout=config.general.timeout,
                        BaseUrl=config.general.base_url)


async def _get_posts_byCategory(page: int = 1, category: str = "ROOT", 
                                city_ids: list[int|str] = ["1"]):
    search_params = {"city_ids": [ str(id) for id in list(set(city_ids)) ],
                 "pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData",
                                    "last_post_date":"0001-01-01T00:00:00Z",
                                    "page":page,"layer_page":page,
                                    "search_uid":""},
                 "search_data":{"form_data":{"data":{"category":{"str":{"value":category}}}},
                                "server_payload":{"@type":"type.googleapis.com/widgets.SearchData.ServerPayload",
                                                  "additional_form_data":{"data":{"sort":{"str":{"value":"recommended"}}}}}}}
    posts = await _request._apost(config.general.endpoints.search_by_category,
                                  json = search_params,
                                  headers={"Authorization": config.general.AUTH_TOKEN})
    return posts.json()
    
    
async def _get_contact_info(pid: str):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8,fa;q=0.7",
        "Authorization": config.general.AUTH_TOKEN,
        "Content-Type": "application/json",
        "Origin": "https://divar.ir",
        "Referer": "https://divar.ir/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "x-render-type": "CSR",
        "x-screen-size": "432x656"
    }
    contact_info = await _request._apost(config.general.endpoints.contact_info.format(pid=pid),
                                        headers=headers)
    return contact_info
    

async def _get_post_info(pid: str):
    post_info = await _request._aget(config.general.endpoints.post_data.format(pid=pid))
    return post_info.json()



async def _get_categories():
    pass


async def _get_cities():
    pass