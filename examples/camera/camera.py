# ====================
# CAMERA PLUGIN
# v0.1
# ====================

__manifest__ = {
    "name": "camera",
    "version": "0.1",
    "description": "",
    "author": "Carlos Pomares",
    "package": "",
    "class": "CameraPlugin",
    "prefix": "",
    "depends_on": {
        "cv2": "cv2"
    }
}

__plugin__ = __manifest__['name']
__version__ = __manifest__['version']

from pws.elastic.plugin import ElasticPlugin, APIRouter, JSONResponse
from fastapi.responses import StreamingResponse

import logging

class CameraPlugin(ElasticPlugin):
    
    name = __plugin__
    version = __version__

    def __init__(self) -> None:
        self.router = APIRouter(
            tags=['Camera'],
        )
        self.depends_on = __manifest__['depends_on']

    def streamer(self):
        if self.camera is None:
            self.camera = self.cv2.VideoCapture(0)
        # TODO: Stop this loop when the client disconnects
        while True:
            # Capture frame-by-frame
            _, frame = self.camera.read()
            (flag, encodedImage) = self.cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')
            

    def __load__(self) -> None:

        self.camera = None
        self.cv2 = self.dependencies['cv2']

        @self.router.get("/video")
        async def video_feed():
            try:
                return StreamingResponse(self.streamer(), media_type="multipart/x-mixed-replace;boundary=frame")
            except Exception as e:
                # Get type of exception
                logging.error(type(e))
                logging.error("Stopped streaming")
                self.camera.release()
                self.camera = None
        
        @self.router.get("/stop")
        async def stop_stream():
            try:
                self.camera.release()
            except:
                logging.error("Camera not running")
                return JSONResponse(
                    {"error": "Camera not running"},
                    status_code=500
                )
            self.camera = None
            return JSONResponse(
                {
                    "status": "Stopped streaming"
                },
                status_code=200
            )