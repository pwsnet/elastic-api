__manifest__ = {
    "name": "application",
    "version": "0.1",
    "description": "Basic plugin for PWS Home API",
    "author": "Carlos Pomares",
    "package": "pws.elastic.plugins.application",
    "class": "ApplicationPlugin",
    "prefix": "",
    "depends_on": []
}

__plugin__ = __manifest__['name']
__version__ = __manifest__['version']

from pws.elastic.plugin import ElasticPlugin, APIRouter, JSONResponse
from datetime import datetime

class ApplicationPlugin(ElasticPlugin):

    name = __plugin__
    version = __version__

    def __init__(self) -> None:
        self.router = APIRouter(
            tags=['Public'],
        )
 
    def __load__(self) -> None:
        
        # Ping
        # ====================

        @self.router.get('/ping')
        def ping():
            return JSONResponse(
                content={
                    'status': 'ok',
                },
                status_code=200
            )
    
        # Greet
        # ====================

        @self.router.get('/greet')
        def greet():
            return JSONResponse(
                content={
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": "Hello, world!"
                },
                status_code=200
            )