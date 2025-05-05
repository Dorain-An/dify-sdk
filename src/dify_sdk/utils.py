import logging
import logging.config
from types import TracebackType
from typing import Mapping, Optional, TypeAlias, Union

from .config import settings

_SysExcInfoType: TypeAlias = Union[
    tuple[type[BaseException], BaseException, Optional[TracebackType]],
    tuple[None, None, None],
]
_ExcInfoType: TypeAlias = Union[None, bool, _SysExcInfoType, BaseException]
LOGGING_CONF = {
    "version": 1,
    'disable_existing_loggers': False,
    "formatters": {
        "default_fmt": {"format": "[%(asctime)s][%(levelname)s] [%(funcName)s]: %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default_fmt",
        },
    },
    "loggers": {
        "": {"level": "INFO", "handlers": ["console"], "propagate": 0},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
logging.config.dictConfig(LOGGING_CONF)

logger = logging.getLogger("dify-sdk")


def info(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None
):
    if not settings.DIFY_LOGGER_ON:
        return
    logger.info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
