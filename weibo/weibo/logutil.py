import logging.config
import os

class Logging:
    log_instance = None

    @staticmethod
    def init_log_conf():
        conf = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'logging.cfg')
        Logging.log_instance = logging.config.fileConfig(conf)

    @staticmethod
    def get_logger(name=""):
        if Logging.log_instance is None:
            Logging.init_log_conf()
        Logging.log_instance = logging.getLogger(name)
        return Logging.log_instance


if __name__ == "__main__":
    logger = Logging.get_logger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

    logHello = Logging.get_logger("logger_dev")
    logHello.info("Hello world!")
