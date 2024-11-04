from os import getenv, path
import logging
import logging.config
import yaml


def file_exists(fname):
    return path.isfile(fname)


def setup_logger():
    if file_exists(Config.LOGGER_CONFIG_FILE):
        with open(Config.LOGGER_CONFIG_FILE, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(filename="myapp.log", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Started")


class Config:
    LOGGER_CONFIG_FILE = getenv(
        "GITOPS_MT__LOGGER_CONFIG_FILE", path.join("resources", "logger.yaml")
    )
    CONFIG_DIR = getenv("GITOPS_MT__CONFIG_DIR")
    LOGS_VERBOSE = True
