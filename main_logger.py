import logging
from config import config

logging.basicConfig(filename='debug.log')
logger = logging.getLogger("main")

if config.debug:
    logger.setLevel(level=logging.DEBUG)
else:
    logger.setLevel(level=logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
