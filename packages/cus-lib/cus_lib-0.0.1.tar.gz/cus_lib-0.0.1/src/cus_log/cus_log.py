import logging


def setup_logger(log_filename="debug.cus_log", log_level=logging.DEBUG):
    log_format = "%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(
                log_filename,
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger()

