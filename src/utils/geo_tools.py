import json

from faker import Faker

from src.utils.http_tools import aio_http_get
from src.utils.log_tools import logger

f = Faker(locale="zh_CN")


async def get_addr_loc(addr: str, ak: str = "burlouFIcfbKunZjFNT7TZMt5l0VHNbA") -> dict:
    """
    地址转经纬度
    :param addr: 地址
    :param ak:
    :return: {
        'status': 0,
        'result': {
            'location': {'lng': 87.66253042457784, 'lat': 43.98003188676441},
            'precise': 1,
            'confidence': 80,
            'comprehension': 100,
            'level': '门址'
        }
    }
    """
    resp = await aio_http_get(
        url=f"http://api.map.baidu.com/geocoding/v3/?address={addr}&output=json&ak={ak}",
    )
    if resp.code < 400 and resp.body:
        resp_string = resp.body.decode()
        out = json.loads(resp_string)
        if isinstance(out, str):
            out = json.loads(out)
        return out
    else:
        logger.error(f"请求百度地图API失败:{resp.body}")
        return {}
