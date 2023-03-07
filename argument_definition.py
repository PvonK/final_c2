import argparse


def argument_definition():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ip", default="127.0.0.1",
                        help="ip where server is setup")

    parser.add_argument("-p", "--port", type=int, default=5000,
                        help="port where server is setup")

    parser.add_argument("-d", "--directory", default="/ex_files",
                        help="server's file storage directory")

    parser.add_argument("-f", "--fresh", action="store_true",
                        help="clean server storage if it exists")

    args = parser.parse_args()

    return args
