import logging

logger = logging.getLogger("gunicorn.error")
logger.setLevel(logging.INFO)

fh = logging.FileHandler("log/app.log")
logger.addHandler(fh)
