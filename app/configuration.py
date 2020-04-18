import logging
import os

DESTINATION_PATH = os.environ["DESTINATION_PATH"]
TRANSMISSION_API = os.environ["TRANSMISSION_API"]

DATA_PATH = "/data/data.dat"
SOURCE_PATH = "/sync"
LOG_FILE_PATH = "/log/data-synchronizer.log"
LOG_LEVEL = logging.DEBUG
TRANSMISSION_SESSION_ID_HEADER = "X-Transmission-Session-Id"
SLEEP_SEC = 300

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
