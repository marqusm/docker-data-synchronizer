import time
import synchronizer
import cleaner
import common
import configuration as cfg

if __name__ == '__main__':
    common.create_data_file_if_not_exists()
    while True:
        cleaner.cleanup_data()
        synchronizer.synchronize()
        time.sleep(cfg.SLEEP_SEC)
