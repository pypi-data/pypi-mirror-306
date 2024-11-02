import sys
from loguru import logger as log
from functools import partialmethod

# Invent new levels
log.level("PROGRESS", no=21, icon=" |", color="<white>")
log.level("READ", no=22, icon=" >", color="<yellow>")
log.level("WRITE", no=23, icon=" <", color="<green>")
log.level("NEW", no=24, icon=" *", color="<white>")
log.level("DONE", no=26, icon="--", color="<white>")

# Allow to call the new levels by attribute
log.__class__.progress = partialmethod(log.__class__.log, "PROGRESS")
log.__class__.read = partialmethod(log.__class__.log, "READ")
log.__class__.write = partialmethod(log.__class__.log, "WRITE")
log.__class__.new = partialmethod(log.__class__.log, "NEW")
log.__class__.done = partialmethod(log.__class__.log, "DONE")


# Change the format depending on levels
def formatter(record):
    if record["level"].name == "TRACE":
        return "<level>{level.icon} {message}</>\n"
    elif record["level"].name == "ERROR":
        return (
            "<level>{level.icon} {message} {exception} ({name}:{function}:{line})</>\n"
        )
    elif record["level"].name == "DEBUG":
        return "<level>{level.icon} {message} ({name}:{function}:{line})</>\n"
    elif record["level"].name == "INFO":
        return "<cyan>{level.icon} {message}</>\n"
    elif record["level"].name == "PROGRESS":
        return "<level>{level.icon} {message}</>\n"
    elif record["level"].name == "READ":
        return "<level>{level.icon} {message}</>\n"
    elif record["level"].name == "WRITE":
        return "<level>{level.icon} {message}</>\n"
    elif record["level"].name == "NEW":
        return "<level>{level.icon} {message}</>\n"
    elif record["level"].name == "WARNING":
        return "<level>{level.icon} {message}</>\n"
    elif record["level"].name == "SUCCESS":
        return "<level>{level.icon} {message}</>\n"
    elif record["level"].name == "DONE":
        return "<level>{level.icon} {message}</>\n"
    else:
        return (
            "<green>{time}</green> | <level>{level: <8}</level> | "
            "<cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>"
            "\n{exception}"
        )


# Apply new formatter
log.remove()
log.add(sys.stderr, format=formatter, level=0)
