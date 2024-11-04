#!/usr/bin/env python

"""
This is the main module that stores the functions that are used when
`cadorchestrator` is run from the terminal.
"""

import sys
import json
import argparse
import uvicorn

from cadorchestrator.generate import generate
from cadorchestrator.settings import Settings

def main(input_args=None):
    """This is what runs if you run `cadorchestrator` from the terminal
    `input_args` can be used to run main from inside python, else sys.argv[1:]
    is used.
    """

    parser = argparse.ArgumentParser(description="Run CadOrchestrator",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--headless",
                        action='store_true',
                        help="Serve on 0.0.0.0")

    subparsers = parser.add_subparsers(help="Possible commands listed below",
                                       metavar="<command>",
                                       dest="command")

    serve_parser = subparsers.add_parser(name="serve",
                                         help="Start server for interactive configuration")


    serve_parser.add_argument("--production",
                              action='store_true',
                              help = "Serve on 0.0.0.0")

    gen_parser = subparsers.add_parser(name="generate",
                                       help="Generate documentation for input configuration")

    gen_parser.add_argument("config",
                            help = "The configuration string")
    args = parser.parse_args(args=input_args)

    if args.command == "serve":
        host = "0.0.0.0" if args.production else "127.0.0.1"
        uvicorn.run("cadorchestrator.server.server:app", host=host, port=8000)
    elif args.command == "generate":
        settings = Settings()
        config = json.loads(args.config)
        generate(config, settings)
    else:
        print(f"Invalid command {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
