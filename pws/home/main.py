# ====================
# PWS Home API (Raw interface)
# ====================

from argparse import ArgumentParser
from pws.home import __version__
from .domain import API
from . import __version__
from uvicorn import run

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
        default="0.0.0.0",
        help="Host to listen on"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port to listen on"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    args = parser.parse_args()

    app = API(
        debug=args.debug,
        title="PWS Home API",
        description="Home Automation API for Python",
        version=__version__,
        extra={
            "plugins_directory": args.plugins
        }
    )

    run(app, host=args.host, port=args.port)
