import importlib
import logging
from types import ModuleType
from typing import Any, List

import environ
from pysolr import SolrError

env = environ.Env()
USER_SETTINGS_PATH = env.str("MICROSERVICE_SETTINGS", default="settings")
settings_paths = [
    USER_SETTINGS_PATH,
    "config.settings.base",
    "app.settings",
    "settings",
    "application.settings",
]
DEFAULTS = {
    "LOGGING_MIXIN_DECORATE": [],
    "CROP_LOG": True,
    "MAX_LOG_ARG_LENGTH": 25000,
    "SERVICE_NAME": "",
    "BLOCK_RECORD_TIMEOUT": 600,
    "SOLR_LOGS_URL": "http://127.0.0.1:8983/solr/logs",
    "SOLR_LOGS_MAX_LENGTH": 25000,
    "BASE_BACK0FF": 1,
    "MAX_BACKOFF_TIME": 60,
    "BACKOFF_MULTIPLIER": 1.25,
    "EXCEPTIONS_TO_CATCH": (SolrError,),
}


def get_settings(settings_paths: List[str]) -> ModuleType:
    for path in settings_paths:
        try:
            return importlib.import_module(path)
        except ModuleNotFoundError:
            continue
    else:
        raise AttributeError("Service settings path is not correct: %s" % USER_SETTINGS_PATH)


class UtilsSettings:
    def __init__(self, user_settings=None, defaults=None) -> None:
        self._user_settings = user_settings or USER_SETTINGS
        self._defaults = defaults or DEFAULTS

    def __getattr__(self, attr: str) -> Any:
        try:
            value = getattr(self._user_settings, attr)
        except AttributeError:
            value = self._defaults[attr]
        setattr(self, attr, value)

        return value


USER_SETTINGS = get_settings(settings_paths)
utils_settings = UtilsSettings()

pysolr_logger = logging.getLogger("pysolr")
pysolr_logger.addHandler(logging.StreamHandler())
pysolr_logger.setLevel(logging.INFO)
pysolr_logger.propagate = False
