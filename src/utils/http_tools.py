from functools import partial
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse

from src.utils.log_tools import logger

http_client = AsyncHTTPClient(max_clients=500)


@logger.catch
async def aio_request(**kwargs) -> HTTPResponse:
    """
    异步发起http请求
    :param kwargs:
    :return:
    """
    kwargs.update(
        dict(
            request_timeout=5,
            connect_timeout=5,
            validate_cert=False,
            allow_nonstandard_methods=True,
        )
    )
    logger.debug(f"【发起http请求】{kwargs}")
    req = HTTPRequest(**kwargs)
    rsp = await http_client.fetch(req)
    logger.debug(
        f"【http请求结束】status({rsp.code} {rsp.reason}), cost {rsp.request_time * 1000:.2f}ms"
    )
    return rsp


aio_http_get = partial(aio_request, method="GET")
aio_http_post = partial(aio_request, method="POST")
aio_http_put = partial(aio_request, method="PUT")
aio_http_delete = partial(aio_request, method="DELETE")
aio_http_head = partial(aio_request, method="HEAD")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    ret = loop.run_until_complete(aio_http_get(url="https://baidu.com"))
