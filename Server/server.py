import asyncio
import tornado.web
import json
from .utils import MainHandler, PingHandler, StatusHandler, StartupHandler, TestHandler

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ping", PingHandler),
        (r"/status", StatusHandler),
        (r"/test", TestHandler),
        (r"/start", StartupHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

def start():
    asyncio.run(main())