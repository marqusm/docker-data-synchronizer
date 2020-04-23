import unittest
import os
import sqlite3
from datetime import datetime, timedelta
from app import common
from app import configuration as cfg


class TestCleaner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cfg.DATABASE_PATH = "test.db"
        cfg.MAX_DAYS_DB_ENTRY = 365
        common.create_database_if_not_exists()

    @classmethod
    def tearDownClass(cls):
        os.remove(cfg.DATABASE_PATH)

    def test_get_processed_list(self):
        conn = sqlite3.connect(cfg.DATABASE_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM items")
        c.execute("INSERT INTO items (name, size, creation_date) VALUES ('Test 1', 1., '2020-04-15 14:15:16')")
        c.execute("INSERT INTO items (name, size, creation_date) VALUES ('Test 2', 1., '2020-04-17 15:16:17')")
        conn.commit()
        conn.close()
        items = common.get_processed_list()
        self.assertEqual(["Test 1", "Test 2"], items)

    def test_add_processed_item(self):
        conn = sqlite3.connect(cfg.DATABASE_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM items")
        conn.commit()
        conn.close()
        common.add_processed_item("Test 1", 1.)
        common.add_processed_item("Test 2", 2.)
        items = common.get_processed_list()
        self.assertEqual(["Test 1", "Test 2"], items)

    def test_cleanup_processed_list(self):
        conn = sqlite3.connect(cfg.DATABASE_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM items")
        c.execute("INSERT INTO items (name, size, creation_date) VALUES ('Test 1', 1., '{}')".format(datetime.now()))
        c.execute(
            "INSERT INTO items (name, size, creation_date) VALUES ('Test 2', 1., '{}')".format(datetime.now() - timedelta(days=400)))
        c.execute(
            "INSERT INTO items (name, size, creation_date) VALUES ('Test 3', 1., '{}')".format(datetime.now() - timedelta(days=350)))
        conn.commit()
        conn.close()
        common.cleanup_processed_list()
        items = common.get_processed_list()
        self.assertEqual(["Test 1", "Test 3"], items)

    def test_get_size(self):
        size = common.get_size("../tests")
        self.assertEqual(0., size)


if __name__ == '__main__':
    unittest.main()
