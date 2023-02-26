from argument_definition import argument_definition
from routes import routes

from aiohttp import web
import os


def server_setup(port):
    HOST, PORT = "localhost", port

    app = web.Application()
    app.router.add_routes(routes)
    web.run_app(app, port=PORT, host=HOST, reuse_address=True)


def main():
    args = argument_definition()

    server_setup(args.port)


if __name__ == "__main__":
    main()
