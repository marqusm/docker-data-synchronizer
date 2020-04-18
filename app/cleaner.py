import logging
import os
import shutil
import requests
import common
import configuration as cfg


def cleanup_data():
    headers = common.get_transmission_headers()
    response = requests.post(cfg.TRANSMISSION_API, headers=headers,
                             json={"method": "torrent-get",
                                   "arguments": {
                                       "fields": ["id", "name", "status", "uploadRatio", "secondsSeeding"]}})
    logging.debug("Response: " + str(response.json()))

    disk_usage = 100 - os.statvfs("/").f_bfree / os.statvfs("/").f_blocks * 100
    processed_items = common.get_processed_list()
    logging.debug("Disc usage: {:3.2f}".format(disk_usage))

    for item in response.json()["arguments"]["torrents"]:
        is_processed = item["name"] in processed_items
        is_finished = item["status"] >= 5
        upload_ratio = item["uploadRatio"]
        days_seeding = item["secondsSeeding"] / (60. * 60 * 24)
        logging.debug(
            "Torrent: {}, {:3.2f}, {:.2f}, {}".format(is_finished, upload_ratio, days_seeding, item["name"]))

        if is_processed and is_finished and disk_usage > 90.:
            logging.info("Disk usage over 90% and item is processed. Deleting. Item: " + item["name"])
            delete_transmission_item(item)
        elif is_processed and is_finished and (upload_ratio >= 1. or days_seeding > 10.):
            logging.info("Item is old and seeded enough. Deleting. Item: " + item["name"])
            delete_transmission_item(item)

    logging.debug("Cleanup data finished.")


def delete_transmission_item(item):
    headers = common.get_transmission_headers()
    loc_response = requests.post(cfg.TRANSMISSION_API, headers=headers,
                                 json={"method": "torrent-remove", "arguments": {"ids": [item["id"]]}})
    if loc_response.status_code != 200:
        logging.warning("Error while removing item from the queue. Error: {}".format(loc_response.text))
    else:
        path = os.path.join(cfg.SOURCE_PATH, item["name"])
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)


if __name__ == '__main__':
    while True:
        cleanup_data()
