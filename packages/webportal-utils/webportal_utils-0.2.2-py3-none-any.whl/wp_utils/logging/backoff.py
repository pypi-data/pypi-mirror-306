import random
from abc import ABC, abstractmethod
from time import sleep
from typing import Tuple

from pydantic import BaseModel

from wp_utils.settings import utils_settings


class ExponentialBackoffConf(BaseModel):
    base_backoff: float
    maximum_backoff: float
    exp_multiplier: float
    to_catch: Tuple[Exception.__class__]

    class Config:
        arbitrary_types_allowed = True


class BackoffTimeoutError(Exception):
    pass


class Backoff(ABC):
    @abstractmethod
    def process(self, fun: callable, *args, **kwargs):
        ...


class ExponentialBackoff(Backoff):
    """
    Implements an exponential backoff strategy for retrying a function call with increasing backoff time.

    Args:
        fun (callable): The function to be retried.
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.

    Raises:
        BackoffTimeoutError: If the maximum backoff time is reached without successful execution.
    """

    def __init__(self, conf: ExponentialBackoffConf) -> None:
        self.conf = conf

    def process(self, fun, *args, **kwargs):
        backoff = self.conf.base_backoff
        random_addon = round(random.uniform(0, 0.5), 3)
        last_exc_msg = ""

        while backoff < self.conf.maximum_backoff:
            try:
                result = fun(*args, **kwargs)
            except self.conf.to_catch as exc:
                last_exc_msg = str(exc)
                backoff += random_addon
                sleep(backoff)
                backoff *= self.conf.exp_multiplier
            except Exception as error:
                raise error
            else:
                break
        else:
            raise BackoffTimeoutError(last_exc_msg)

        return result


def exp_backoff(fun):
    def wrapper(*args, **kwargs):
        conf = ExponentialBackoffConf(
            base_backoff=utils_settings.BASE_BACK0FF,
            maximum_backoff=utils_settings.MAX_BACKOFF_TIME,
            exp_multiplier=utils_settings.BACKOFF_MULTIPLIER,
            to_catch=utils_settings.EXCEPTIONS_TO_CATCH,
        )
        return ExponentialBackoff(conf).process(fun, *args, **kwargs)

    return wrapper
