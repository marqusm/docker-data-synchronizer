import logging
import os
import subprocess
from app import common
from app import configuration as cfg


def synchronize():
    logging.info("Sync starting...")
    processed_list = common.get_processed_list()
    to_process_list = calculate_to_process_list(cfg.SOURCE_PATH, processed_list)
    if len(to_process_list) == 0:
        logging.info("There is nothing to sync")
    else:
        execute_data_sync(to_process_list)
    logging.info("Sync completed")


def calculate_to_process_list(path, processed_items):
    folder_list = os.listdir(path)
    return [item for item in folder_list if item not in processed_items]


def execute_data_sync(to_process_items):
    ps_command = "ps -a | grep rsync"
    rsync_command = "rsync -Pha -e ssh {}/{} {}"
    output = subprocess.check_output(ps_command, shell=True)
    logging.debug("Ps output: " + output.decode("utf-8") + str(output.decode("utf-8").count('\n')))
    if output.decode("utf-8").count("\n") > 2:
        logging.debug("Rsync command already in progress. Skipping the sync")
    else:
        for item in to_process_items:
            logging.debug("Rsync starting: " + rsync_command.format(cfg.SOURCE_PATH, item, cfg.DESTINATION_PATH))
        #     p = subprocess.Popen(rsync_command.format(SOURCE_PATH, item), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                          shell=True)
        #     for line in iter(p.stdout.readline, b''):
        #         logging.info(line.decode("utf-8"))
        #     p.stdout.close()
        #     p.wait()
            path = os.path.join(cfg.SOURCE_PATH, item)
            size = common.get_size(path)
            common.add_processed_item(item, size)
            logging.debug("Rsync finished for item: {}".format(item))
    logging.debug("Rsync command completed")


if __name__ == '__main__':
    while True:
        synchronize()
