import logging
from logging.config import dictConfig
from typing import Any, Dict

from .config import get_settings


def get_logging_config() -> Dict[str, Any]:
    settings = get_settings()
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": settings.log_level,
            }
        },
        "loggers": {
            "uvicorn": {"handlers": ["console"], "level": settings.log_level, "propagate": False},
            "uvicorn.error": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": settings.log_level,
        },
    }


def configure_logging() -> None:
    dictConfig(get_logging_config())
    logging.getLogger(__name__).debug("Logging configured")
