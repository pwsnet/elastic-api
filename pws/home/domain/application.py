import importlib
import logging
import os, sys

from fastapi import FastAPI

class API(FastAPI):

    detected_plugins: dict = {}
    installed_plugins: dict = {}

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
                    init = importlib.import_module(
                        f"pws.home.plugins.{plugin}.__init__"
                    )
                    manifest = init.__manifest__
                    logging.debug(f"Plugin manifest: {manifest}")
                    module = importlib.import_module(f'{manifest["package"]}')    
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
        self.__load_default__()
        self.__load_plugins__()
        self.__include_plugins__()
        super().setup()