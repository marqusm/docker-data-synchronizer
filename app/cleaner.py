import logging
import os
import requests
import common
import configuration as cfg


def cleanup_data():
    logging.info("Cleanup data starting...")
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
        logging.debug("Torrent item: Is Finished={}, Upload Ratio={:3.2f}, Days Seeding={:.2f}, Name={}".format(is_finished, upload_ratio,
                                                                                                                days_seeding, item["name"]))

        if is_processed and is_finished and disk_usage > 90.:
            logging.info("Disk usage over 90% and item is processed. Deleting item: {}".format(item["name"]))
            delete_transmission_item(item)
        elif is_processed and is_finished and (upload_ratio >= 1. or days_seeding > 10.):
            logging.info("Item is old enough and seeded enough. Deleting item: {}".format(item["name"]))
            delete_transmission_item(item)

    logging.info("Cleanup data finished")


def delete_transmission_item(item):
    headers = common.get_transmission_headers()
    loc_response = requests.post(cfg.TRANSMISSION_API, headers=headers,
                                 json={"method": "torrent-remove", "arguments": {"ids": [item["id"]], "delete-local-data": True}})
    if loc_response.status_code == 200:
        logging.debug("Item removed from the queue: {}".format(item["name"]))
    else:
        logging.warning("Error while removing item from the queue. Error: {}".format(loc_response.text))


if __name__ == '__main__':
    while True:
        cleanup_data()
