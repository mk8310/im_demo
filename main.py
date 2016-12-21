import logging

import tornado.web
from tornado import httpserver
from tornado import ioloop
from tornado import options as tnd_options
from tornado.options import define, options

from message_queue.log_consumer import LogConsumer
from message_queue.render_consumer import RenderConsumer
from settings import settings
from urls import url_patterns

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

define("port", default=8000, help="run on the given port", type=int)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    tnd_options.parse_command_line()
    app = tornado.web.Application(handlers=url_patterns, **settings)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    io_loop = ioloop.IOLoop.instance()
    render_consumer = RenderConsumer(io_loop)
    app.rc = render_consumer
    app.rc.connect()

    log_consumer = LogConsumer(io_loop)
    app.lc = log_consumer
    app.lc.connect()

    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
