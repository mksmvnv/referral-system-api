import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)s %(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s]",
    datefmt="%d-%m-%Y %H:%M:%S",
)

info_handler = logging.FileHandler("logs/info.log")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(error_handler)
