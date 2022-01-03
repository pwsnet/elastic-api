import importlib
import logging
import pathlib
import os, sys

from datetime import datetime
from fastapi import FastAPI

class API(FastAPI):

    detected_plugins: dict = {}
    installed_plugins: dict = {}

    def __init_logging__(self):
        # Create Logging directory
        pathlib.Path('/var/log/pws').mkdir(parents=True, exist_ok=True)
        # Create Logging file
        log_file = f'/var/log/pws/monitor_{datetime.utcnow().strftime("%Y-%m-%d")}.log'
        pathlib.Path(log_file).touch()
        # Setup Logging
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.DEBUG if self.debug else logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=log_file,
            filemode='a',
        )

    def __load_default__(self):
        # List default plugin directory to detect the plugins
        for plugin in os.listdir(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../',
            'plugins'
        )):
            if plugin not in ["__init__.py", "__pycache__"]:
                logging.debug(f"Loading plugin: {plugin}")                
                try:
                    module = importlib.import_module(
                        f"pws.home.plugins.{plugin}.{plugin}"
                    )
                    manifest = module.__manifest__
                    logging.debug(f"Plugin manifest: {manifest}")
                    self.installed_plugins[plugin] = {
                        'manisfest': manifest,
                        'module': getattr(module, manifest["class"])()
                    }
                    logging.debug("Loaded plugin: %s", plugin)
                except Exception as e:
                    logging.error(f'Error loading plugin: {plugin}')
                    logging.error(e)

    def __load_plugins__(self):
        plugins_path = self.extra['extra']['plugins_directory']
        if plugins_path is None:
            logging.debug("No plugins directory specified")
            return
        if not isinstance(plugins_path, str):
            logging.debug("Invalid plugins directory specified")
            return
        if not os.path.exists(plugins_path):
            logging.error("Plugins directory does not exist")
            return
        for plugin in os.listdir(plugins_path):
            logging.debug(f"Loading plugin: {plugin}")                
            try:
                # Append the plugin directory to the sys path
                sys.path.append(
                    os.path.abspath(os.path.join(
                        plugins_path,
                        plugin
                    ))
                )
                module = importlib.import_module(
                    f"{plugin}"
                )
                manifest = module.__manifest__
                logging.debug(f"Plugin manifest: {manifest}")
                self.installed_plugins[plugin] = {
                    'manisfest': manifest,
                    'module': getattr(module, manifest["class"])()
                }
                logging.debug("Installed plugin: %s", self.installed_plugins[plugin])
                logging.debug("Loaded plugin: %s", plugin)
            except Exception as e:
                logging.error(f'Error loading plugin: {plugin}')
                logging.error(e)

    def __include_plugins__(self):
        for name, plugin in self.installed_plugins.items():
            logging.debug(f"Including plugin: {name}")
            manifest = plugin['manisfest']
            module = plugin['module']
            module.init()
            self.include_router(
                module.get_router(),
                prefix=manifest['prefix']
            )

    def setup(self) -> None:
        # Load default plugins
        self.__init_logging__()
        self.__load_default__()
        self.__load_plugins__()
        self.__include_plugins__()
        super().setup()