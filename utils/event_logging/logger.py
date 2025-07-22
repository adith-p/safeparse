import logging
from collections import  deque
from rich import print
logger = logging.getLogger("safeparse")
logger.setLevel(logging.INFO)  # You can change the level

# File handler: logs to 'event.log'
file_handler = logging.FileHandler("event.log")
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(message)s'))

# Avoid duplicated handlers
if not logger.handlers:
    logger.addHandler(file_handler)


def print_log():
    with open("event.log", "r") as log:
        log_items = deque(log,maxlen=20)

    for items in log_items:
        print(items)

