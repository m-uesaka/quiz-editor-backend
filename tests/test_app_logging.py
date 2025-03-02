import logging
import os


class TestLogger:
    @staticmethod
    def test_exists() -> None:
        logger = logging.getLogger("gunicorn.error")
        assert logger is not None

    @staticmethod
    def test_level() -> None:
        logger = logging.getLogger("gunicorn.error")
        assert logger.level == logging.INFO


def test_file_handler_exists():
    logger = logging.getLogger("gunicorn.error")
    handlers = logger.handlers
    file_handler_exists = any(
        isinstance(handler, logging.FileHandler) for handler in handlers
    )
    assert file_handler_exists


class TestLogFile:
    @staticmethod
    def test_creation() -> None:
        log_file_path = "log/app.log"
        if os.path.exists(log_file_path):
            os.remove(log_file_path)

        logger = logging.getLogger("gunicorn.error")
        logger.info("Test log entry")

        assert os.path.exists(log_file_path)

    @staticmethod
    def test_content() -> None:
        log_file_path = "log/app.log"
        if os.path.exists(log_file_path):
            os.remove(log_file_path)

        logger = logging.getLogger("gunicorn.error")
        test_message = "Test log entry"
        logger.info(test_message)

        with open(log_file_path, "r") as log_file:
            log_content = log_file.read()

        assert test_message in log_content
