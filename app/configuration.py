import logging
import os

# Remote server data to be sent to. Eg: user@example.com:sync
DESTINATION_PATH = os.getenv("DESTINATION_PATH", "")
TRANSMISSION_API = os.getenv("TRANSMISSION_API", "")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)

DATABASE_PATH = "/data/data.db"
SOURCE_PATH = "/sync"
LOG_FILE_PATH = "/log/data-synchronizer.log"
TRANSMISSION_SESSION_ID_HEADER = "X-Transmission-Session-Id"
# Waking up interval
SLEEP_SEC = 300
# Force deletion of sent items once disk is low on space
MIN_FREE_DISK_GB = 10
# Delete an item when limit is reached
MAX_UPLOAD_RATIO = 2
# Delete an item when limit is reached
MAX_DAYS_SEEDING = 10
# How long to keep sent entries data in DB
MAX_DAYS_DB_ENTRY = -1
# Days in past to fetch from DB when calculating what is sent to server.
# Used to avoid new file not to be sync'd because of some old files with the same name
CONSIDERING_HISTORY_DAYS = 7


def init():
    logging.basicConfig(level=LOGGING_LEVEL,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S.%s',
                        filename=LOG_FILE_PATH,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(LOGGING_LEVEL)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
