import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ft = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s: %(message)s'
        )
ch = logging.StreamHandler()
ch.setFormatter(ft)
logger.addHandler(ch)
