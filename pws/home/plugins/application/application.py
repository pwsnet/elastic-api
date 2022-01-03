# ====================
# APPLICATION PLUGIN
# v0.1
#
# GOALS: Common public methods for all plugins.
#
# ====================

__plugin__ = "application"
__version__ = '0.1'

from pws.home.plugin import HomePlugin, APIRouter, JSONResponse
from datetime import datetime

class ApplicationPlugin(HomePlugin):

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

        # Metadata
        # ====================

        @self.router.get('/version')
        def version():
            return JSONResponse(
                content={
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": __version__
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