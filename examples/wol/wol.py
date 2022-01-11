# ====================
# WAKEONLAN PLUGIN
# v0.1
# ====================

__manifest__ = {
    "name": "wol",
    "version": "0.1",
    "description": "",
    "author": "Carlos Pomares",
    "package": "",
    "class": "WakeOnLanPlugin",
    "prefix": "/wol",
    "depends_on": {
        "wakeonlan": "wakeonlan"
    }
}

__plugin__ = __manifest__['name']
__version__ = __manifest__['version']

from pws.elastic.plugin import ElasticPlugin, APIRouter, JSONResponse
import logging

class WakeOnLanPlugin(ElasticPlugin):
    
    name = __plugin__
    version = __version__

    def __init__(self) -> None:
        self.router = APIRouter(
            tags=['HomeAutomation'],
        )
        self.depends_on = __manifest__['depends_on']

    def __load__(self) -> None:

        self.wakeonlan = self.dependencies['wakeonlan']

        @self.router.get('/wake')
        async def wakeonlan(mac: str = ""):
            logging.info(f'Sending Magic Packet to: {mac}')
            if mac == "":
                return JSONResponse(
                    content={
                        "error": "MAC Address is required"
                    },
                    status_code=400
                )
            try:
                self.wakeonlan.send_magic_packet(mac)
            except:
                logging.error(f'Error sending Magic Packet to: {mac}')
                return JSONResponse(
                    status_code=500,
                    content={
                        'error': 'Error sending Magic Packet'
                    }
                )
            return JSONResponse(
                content={
                    'result': f'Magic Packet sent to: {mac}'
                },
                status_code=200
            )