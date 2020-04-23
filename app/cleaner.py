import logging
import requests
import common
import configuration as cfg
import sys


def cleanup_data():
    logging.info("Cleanup data starting...")
    headers = common.get_transmission_headers()
    response = requests.post(cfg.TRANSMISSION_API, headers=headers,
                             json={"method": "torrent-get",
                                   "arguments": {
                                       "fields": ["id", "name", "status", "uploadRatio", "secondsSeeding", "doneDate"]}})
    logging.debug("Response: " + str(response.json()))

    processed_items = common.get_processed_list()
    logging.debug("Free disk space: {:3.2f}GB".format(get_free_space_in_gb()))

    is_any_item_removed = False
    items = response.json()["arguments"]["torrents"]
    items = sorted(items, key=lambda i: i["doneDate"] if i["doneDate"] != 0 else sys.maxsize)
    for item in items:
        free_disk_space = get_free_space_in_gb()
        is_processed = item["name"] in processed_items
        is_finished = item["status"] >= 5
        upload_ratio = item["uploadRatio"]
        days_seeding = item["secondsSeeding"] / (60. * 60 * 24)
        logging.debug(
            "Transmission item: Is Finished={}, Upload Ratio={:3.2f}, Days Seeding={:.2f}, Name={}".format(is_finished, upload_ratio,
                                                                                                           days_seeding, item["name"]))

        if is_processed and is_finished and free_disk_space < 10.:
            logging.info("Item is processed and free disk space is under 10GB. Deleting item: {}".format(item["name"]))
            delete_transmission_item(item)
            is_any_item_removed = True
        elif is_processed and is_finished and (upload_ratio >= 1. or days_seeding > 10.):
            logging.info("Item is processed, old enough and seeded enough. Deleting item: {}".format(item["name"]))
            delete_transmission_item(item)
            is_any_item_removed = True

    if not is_any_item_removed:
        logging.info("There is nothing to clean")
    logging.info("Cleanup data finished")


def delete_transmission_item(item):
    headers = common.get_transmission_headers()
    loc_response = requests.post(cfg.TRANSMISSION_API, headers=headers,
                                 json={"method": "torrent-remove", "arguments": {"ids": [item["id"]], "delete-local-data": True}})
    if loc_response.status_code == 200:
        logging.debug("Item removed from the queue: {}".format(item["name"]))
    else:
        logging.warning("Error while removing item from the queue. Error: {}".format(loc_response.text))


def get_free_space_in_gb():
    headers = common.get_transmission_headers()
    response = requests.post(cfg.TRANSMISSION_API, headers=headers, json={"method": "free-space", "arguments": {"path": "/"}})
    return response.json()["arguments"]["size-bytes"] / 1024 ** 3


if __name__ == '__main__':
    while True:
        cleanup_data()
