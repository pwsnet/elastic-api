from argparse import ArgumentParser

import os

parser_args = [
    {
        "name_or_flags": "--plugins",
        "type": str,
        "help": "Path to plugins directory",
        "required": False,
    },
    {
        "name_or_flags": "--host",
        "type": str,
        "help": "Host to listen on",
        "required": False,
    },
    {
        "name_or_flags": "--port",
        "type": int,
        "help": "Port to listen on",
        "required": False,
    },
    {
        "name_or_flags": "--debug",
        "action": "store_true",
        "help": "Enable debug mode",
        "required": False,
    }
]

api_args = [
    {
        "name": "host",
        "os_env": "ELASTIC_HOST",
        "type": str,
        "default": "0.0.0.0"
    },
    {
        "name": "port",
        "os_env": "ELASTIC_PORT",
        "type": int,
        "default": "3000"
    },
    {
        "name": "plugins",
        "os_env": "ELASTIC_PLUGINS",
        "type": str,
        "default": None
    },
    {
        "name": "prefix",
        "os_env": "ELASTIC_PREFIX",
        "type": str,
        "default": ""
    }
]

def create_parser(**kwargs) -> ArgumentParser:
    parser = ArgumentParser(**kwargs)
    for arg in parser_args:
        name = arg["name_or_flags"]
        # Arg data without name
        arg_data = {k: v for k, v in arg.items() if k != "name_or_flags"}
        parser.add_argument(name, **arg_data)
    return parser

class ElasticArguments(dict):

    host = "0.0.0.0"
    port = 3000
    plugins = None
    debug = False
    
    prefix = ""

    def __init__(self, parser: ArgumentParser):
        self.parse(parser)

    def parse(self, parser: ArgumentParser) -> None:
        args = parser.parse_args()

        # Parse ArgumentParser args
        for argv in parser_args:
            key: str = argv["name_or_flags"].lstrip("--")
            value = eval(f"args.{argv['name_or_flags'].lstrip('--')}")
            if isinstance(value, bool if "type" not in argv else argv["type"]):
                self.__setattr__(key.lower(),value)
    
        # Parser Environment Variables
        for argv in api_args:
            key: str = argv["name"]
            value = argv["default"]
            if argv["os_env"] in os.environ:
                value = argv["type"](os.environ[argv["os_env"]])
                self.__setattr__(key.lower(),value)