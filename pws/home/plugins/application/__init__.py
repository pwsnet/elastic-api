__manifest__ = {
    "name": "application",
    "version": "0.1",
    "description": "Basic plugin for PWS Home API",
    "author": "Carlos Pomares",
    "package": "pws.home.plugins.application",
    "class": "ApplicationPlugin",
    "prefix": "",
    "depends_on": []
}

from .application import ApplicationPlugin