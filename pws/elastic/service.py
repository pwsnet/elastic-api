from pws.elastic import __version__
from pws.elastic.args import ElasticArguments, create_parser
from pws.elastic.applications import API
from pws.elastic import __version__

from uvicorn import run
import logging

if __name__ == '__main__':
    
    parser = create_parser()
    args = ElasticArguments(parser)
    
    app = API(
        debug=args.debug,
        title="Elastic API",
        description="Elastic API for Python",
        openapi_prefix=f"{args.prefix}",
        extra={
            "plugins_directory": args.plugins
        }
    )

    logging.info(f'Elastic API')
    logging.info(f'Running on {args.host}:{args.port}')
    logging.info(f'Plugins directory: {args.plugins}')
    logging.info(f'Debug mode: {args.debug}')

    run(app, host=args.host, port=args.port)