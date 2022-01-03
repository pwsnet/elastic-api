# ====================
# PWS Home API (Raw interface)
# ====================

from argparse import ArgumentParser
from pws.home import __version__
from .domain import API
from . import __version__
from uvicorn import run

import logging
import os

if __name__ == '__main__':
    
    parser = ArgumentParser(description='PWS Home API', prog='pws-home', epilog='PWS Home API')

    parser.add_argument(
        '--plugins',
        type=str,
        help='Path to plugins directory'
    )

    parser.add_argument(
        "--host",
        type=str,
        help="Host to listen on"
    )

    parser.add_argument(
        "--port",
        type=int,
        help="Port to listen on"
    )

    parser.add_argument(
        '--root',
        type=str,
        help='Root path to server'
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    args = parser.parse_args()

    host = "0.0.0.0" if args.host is None else args.host
    port = 3000 if args.port is None else args.port
    root = '' if args.port is None else args.root

    if args.host is None and os.getenv("HOST") is not None:
        host = os.getenv("HOST")
    
    if args.port is None and os.getenv("PORT") is not None:
        port = int(os.getenv("PORT"))
    
    if args.root is None and os.getenv("ROOT") is not None:
        root = os.getenv("ROOT")

    app = API(
        debug=args.debug,
        title="PWS Home API",
        description="Home Automation API for Python",
        version=__version__,
        root_path=root,
        extra={
            "plugins_directory": args.plugins
        }
    )

    logging.info(f'PWS Home API v{__version__}')
    logging.info(f'Running on {host}:{port}')
    logging.info(f'Plugins directory: {args.plugins}')
    logging.info(f'Debug mode: {args.debug}')

    run(app, host=host, port=port)