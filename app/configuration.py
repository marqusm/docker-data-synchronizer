import logging
import os

DESTINATION_PATH = os.getenv("DESTINATION_PATH", "")
TRANSMISSION_API = os.getenv("TRANSMISSION_API", "")

DATABASE_PATH = "/data/state.db"
SOURCE_PATH = "/sync"
LOG_FILE_PATH = "/log/data-synchronizer.log"
LOG_LEVEL = logging.DEBUG
TRANSMISSION_SESSION_ID_HEADER = "X-Transmission-Session-Id"
SLEEP_SEC = 300
MIN_FREE_DISK_GB = 10
MAX_UPLOAD_RATIO = 2
MAX_DAYS_SEEDING = 10
MAX_DAYS_DB_ENTRY = -1


def init():
    logging.basicConfig(level=LOG_LEVEL,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S.%s',
                        filename=LOG_FILE_PATH,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
