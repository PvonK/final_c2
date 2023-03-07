from argument_definition import argument_definition
from routes import getRoutes

from aiohttp import web
import os


def server_setup(port, directory):
    HOST, PORT = "127.0.0.1", port

    app = web.Application()
    app.router.add_routes(getRoutes(directory))
    web.run_app(app, port=PORT, host=HOST, reuse_address=True)


def main():
    args = argument_definition()

    newpath = os.path.dirname(__file__)+"/"+args.directory

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    server_setup(args.port, "/" + args.directory + "/")


if __name__ == "__main__":
    main()
