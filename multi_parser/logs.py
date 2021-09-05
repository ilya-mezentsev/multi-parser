import sys
import logging


__all__ = [
    'configure_logging',
]


def configure_logging(logging_level: str) -> None:
    assert logging_level in _supported_logging_levels, 'Invalid logging level'

    formatter = logging.Formatter(
        fmt='[{levelname[0]} {asctime} {module}:{lineno}] {message}',
        datefmt='%y%m%d %H:%M:%S %z',
        style='{'
    )

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)

    logger.setLevel(_supported_logging_levels.get(
        logging_level,
        logging.WARNING,
    ))


_supported_logging_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
}
