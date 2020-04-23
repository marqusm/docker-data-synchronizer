import time
import app.synchronizer as synchronizer
import app.cleaner as cleaner
import app.common as common
import app.configuration as cfg

if __name__ == '__main__':
    cfg.init()
    common.create_database_if_not_exists()
    while True:
        cleaner.cleanup_data()
        synchronizer.synchronize()
        time.sleep(cfg.SLEEP_SEC)
