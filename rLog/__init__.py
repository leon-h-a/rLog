import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ft = logging.Formatter(
    "%(asctime)s -> %(levelname)s"
    "\t[%(filename)s][L%(lineno)d]: %(message)s"
)
ch = logging.StreamHandler()
ch.setFormatter(ft)
logger.addHandler(ch)
