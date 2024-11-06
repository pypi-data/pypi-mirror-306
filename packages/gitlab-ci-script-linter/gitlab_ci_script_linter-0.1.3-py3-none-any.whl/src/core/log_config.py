"""Logging configuration."""

import logging
import logging.config

LOG_LEVEL: str = "DEBUG"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "%(levelname)s %(asctime)s - %(name)s - %(message)s"
        },
        "f": {
            "format": "%(levelname)s %(asctime)s - %(name)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
