import logging
from copy import deepcopy
from logging import LogRecord
from typing import Any, Dict

from wp_utils.settings import utils_settings


class CropLogger(logging.Logger):
    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ) -> LogRecord:
        if utils_settings.CROP_LOG:
            args = self._crop_args(list(args))
            extra = self.__crop_item(extra) if extra else None
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

    def _crop_args(self, args: list) -> tuple:
        for index, arg in enumerate(args):
            args[index] = self.__crop_item(arg)
        return tuple(args)

    def __crop_item(self, value):
        if isinstance(value, dict):
            value = self.__crop_dict(value)
        elif isinstance(value, str):
            value = value[: utils_settings.MAX_LOG_ARG_LENGTH]
        elif not isinstance(value, (int, float)):
            value = str(value)[: utils_settings.MAX_LOG_ARG_LENGTH]
        return value

    def __crop_dict(self, message) -> dict:
        updated_message = deepcopy(message)
        for key, value in message.items():
            updated_message[key] = self.__crop_item(value)
        return updated_message


class ExtendedLogger(CropLogger):
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs = self._ensure_status_code(kwargs, 200)
        return super().info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs = self._ensure_status_code(kwargs, 200)
        return super().warning(msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs = self._ensure_status_code(kwargs, 200)
        return super().debug(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs = self._ensure_status_code(kwargs, 400)
        return super().error(msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, exc_info=True, **kwargs: Any) -> None:
        kwargs = self._ensure_status_code(kwargs, 500)
        return super().exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs = self._ensure_status_code(kwargs, 500)
        return super().critical(msg, *args, **kwargs)

    def _ensure_status_code(self, kwargs: Dict[str, Any], status_code: int) -> Dict[str, Any]:
        extra = kwargs.get("extra", {})
        if isinstance(extra, dict):
            extra.setdefault("status_code", status_code)
        kwargs["extra"] = extra
        return kwargs
