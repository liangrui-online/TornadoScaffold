import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

import config
from src.utils.log_tools import logger, tornado_log
from src.views.url import routes


def make_app(debug: bool):
    assert isinstance(routes, (list, tuple)), "urls must be list or tuple"
    app = tornado.web.Application(routes, debug=debug)
    app.log_request = tornado_log
    return app


@logger.catch
def run_service():
    debug_mode = config.debug
    port = config.port

    if debug_mode is False:
        logger.debug = lambda *args, **kwargs: None

    app = make_app(debug=debug_mode)
    app.listen(port)
    logger.info(f"Start server at {port}")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run_service()
