import argparse


def argument_definition():

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, default=5000,
                        help="port where server gets setup")

    parser.add_argument("-d", "--directory", default="/ex_files",
                        help="server's file storage directory")

    args = parser.parse_args()

    return args
