import argparse


def argument_definition():

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, default=5000,
                        help="port where server gets setup")

    args = parser.parse_args()

    return args
