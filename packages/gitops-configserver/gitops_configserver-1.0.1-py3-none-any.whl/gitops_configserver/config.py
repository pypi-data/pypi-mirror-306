from os import getenv, path
from datetime import datetime
import logging
import logging.config
from gitops_configserver.utils import file_exists, load_yaml, create_dir


def setup_logger():
    if file_exists(Config.LOGGER_CONFIG_FILE):
        config = load_yaml(Config.LOGGER_CONFIG_FILE)
        logging.config.dictConfig(config)
    else:
        create_dir("logs")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=datetime.now().strftime("logs/logs_%Y_%m_%d_%H_%M.log"),
            filemode="w",
        )
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(name)-12s: %(levelname)-8s %(message)s"
        )
        console.setFormatter(formatter)
        logging.getLogger("").addHandler(console)
    logger = logging.getLogger(__name__)
    logger.info("Started")


class Config:
    LOGS_VERBOSE = True

    LOGGER_CONFIG_FILE = getenv(
        "GITOPS_CONFIGSERVER__LOGGER_CONFIG_FILE",
        path.join("resources", "logger.yaml"),
    )
    CONFIG_DIR = getenv("GITOPS_CONFIGSERVER__CONFIG_DIR")
    TARGET_DIR = getenv("GITOPS_CONFIGSERVER__TARGET_DIR", "target")

    HOST = getenv("GITOPS_CONFIGSERVER__HOST", "0.0.0.0")
    PORT = getenv("GITOPS_CONFIGSERVER__PORT", "8002")

    GH_PAT = getenv("GH_PAT")
