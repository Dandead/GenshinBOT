import asyncio
import logging.config
from src.bot import bot


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(filename)s:%(funcName)s:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        # "json": {
        #     "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
        #     "format": """
        #             asctime: %(asctime)s
        #             created: %(created)f
        #             filename: %(filename)s
        #             funcName: %(funcName)s
        #             levelname: %(levelname)s
        #             levelno: %(levelno)s
        #             lineno: %(lineno)d
        #             message: %(message)s
        #             module: %(module)s
        #             msec: %(msecs)d
        #             name: %(name)s
        #             pathname: %(pathname)s
        #             process: %(process)d
        #             processName: %(processName)s
        #             relativeCreated: %(relativeCreated)d
        #             thread: %(thread)d
        #             threadName: %(threadName)s
        #             exc_info: %(exc_info)s
        #         """,
        #     "datefmt": "%Y-%m-%d %H:%M:%S"
        # },
    },
    "handlers": {
        "databases": {
            "formatter": "default",
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "log/databases.log",
            "backupCount": 3
        },
        "bot": {
            "formatter": "default",
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "log/bot.log",
            "backupCount": 3
        },
        "errors": {
            "formatter": "detailed",
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "log/errors.log",
            "backupCount": 2
        },
    },
    "loggers": {
        "databases": {
            "level": "INFO",
            "handlers": [
                "databases"
            ]
        },
        "handlers": {
            "level": "INFO",
            "handlers": [
                "bot"
            ]
        },
        "parser": {
            "level": "INFO",
            "handlers": [
                "bot"
            ]
        },
        "user": {
            "level": "INFO",
            "handlers": [
                "bot"
            ]
        },
    },
    "root": {
        "handlers": [
            "errors"
        ]
    },
}


if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_CONFIG)
    try:
        asyncio.run(bot.main())
    except (KeyboardInterrupt, SystemExit):
        pass # logger.error("Bot stopped!")

