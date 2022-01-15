# ====================
# PLUGIN SDK
# v0.1
# ====================

import logging

from importlib import import_module
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

class ElasticPlugin:

    application: FastAPI = None
    router: APIRouter = None
    name: str = None
    version: str = None

    depends_on: dict = {}
    dependencies: dict = {}

    def __init__(self) -> None:
        pass

    def __load_dependencies__(self) -> None:
        logging.info("Loading dependencies for plugin %s" % self.name)
        for name, package in self.depends_on.items():
            try:
                self.dependencies[name] = import_module(package)
            except Exception as e:
                logging.error(f"Plugin {self.name} failed to load dependency {name}")
                logging.error(e)

    def __load__(self) -> None:
        pass

    def set_application(self, application: FastAPI) -> None:
        self.application = application

    def get_router(self) -> APIRouter:
        return self.router

    def get_name(self) -> str:
        return self.name

    def get_version(self) -> str:
        return self.version

    def init(self) -> None:
        self.__load_dependencies__()
        self.__load__()