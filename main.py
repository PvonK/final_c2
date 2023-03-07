from argument_definition import argument_definition
from routes import getRoutes
import shutil

from aiohttp import web
import os


def server_setup(ip, port, directory):
    HOST, PORT = ip, port

    app = web.Application()
    app.router.add_routes(getRoutes(directory))
    try:
        web.run_app(app, port=PORT, host=HOST, reuse_address=True)
    except OSError:
        print("Server could not start")

def main():
    args = argument_definition()

    newpath = os.path.dirname(__file__)+"/"+args.directory

    if os.path.exists(newpath) and args.fresh:
        shutil.rmtree(newpath)


    if not os.path.exists(newpath):
        os.makedirs(newpath)

    server_setup(args.ip, args.port, "/" + args.directory + "/")


if __name__ == "__main__":
    main()
