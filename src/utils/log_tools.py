from loguru import logger
from loguru._file_sink import FileDateFormatter


FileDateFormatter.__format__ = lambda obj, _: obj.datetime.__format__("%Y-%m-%d")

logger.add("./logs/{time}.log", rotation="00:00", backtrace=True, diagnose=True)


def tornado_log(app, handler=None) -> None:
    handler = handler or app

    if "log_function" in app.settings:
        app.settings["log_function"](handler)
        return
    if handler.get_status() < 400:
        log_method = logger.info
    elif handler.get_status() < 500:
        log_method = logger.warning
    else:
        log_method = logger.error
    request_time = 1000.0 * handler.request.request_time()
    log_method(
        f"{handler.get_status()} {handler._request_summary()} {request_time:.2f}ms"
    )
