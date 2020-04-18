import requests
import configuration as cfg


def get_transmission_headers():
    response = requests.post(cfg.TRANSMISSION_API, data={"method": "session-stats"})
    session_id = response.headers[cfg.TRANSMISSION_SESSION_ID_HEADER]
    return {cfg.TRANSMISSION_SESSION_ID_HEADER: session_id}


def get_processed_list():
    file = open(cfg.DATA_PATH, 'r')
    with file as f:
        lines = f.read().splitlines()
    file.close()
    return lines


def create_data_file_if_not_exists():
    file = open(cfg.DATA_PATH, 'a+')
    file.close()
