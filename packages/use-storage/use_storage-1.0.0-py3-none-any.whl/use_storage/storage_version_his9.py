# ======================== 添加了 mysql 和 mongoDB 支持
import os
import json
import sqlite3
from datetime import datetime
import mysql.connector
from pymongo import MongoClient

# 定义存储目录和数据库路径
STORAGE_DIR = ".storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

DB_PATH = os.path.join(STORAGE_DIR, "storage.db")
JSON_PATH = os.path.join(STORAGE_DIR, "storage.json")


class Storage:
    def __init__(self, key, initial_value, storage_type="json", db_config=None):
        self.key = key
        self.storage_type = storage_type

        # 根据存储类型选择不同的初始化方式
        if storage_type == "sqlite":
            self.conn = sqlite3.connect(DB_PATH)
            self._create_sqlite_tables()
            self._load_sqlite_value(initial_value)
        elif storage_type == "mysql":
            self.conn = mysql.connector.connect(**db_config)
            self._create_mysql_tables()
            self._load_mysql_value(initial_value)
        elif storage_type == "mongodb":
            self.client = MongoClient(db_config["host"])
            self.db = self.client[db_config["database"]]
            self._load_mongodb_value(initial_value)
        else:
            self._load_json_value(initial_value)

    # SQLite 相关逻辑
    def _create_sqlite_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS storage (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    counter INTEGER DEFAULT 0
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    key TEXT,
                    timestamp TEXT,
                    old_value TEXT
                )
            ''')

    def _load_sqlite_value(self, initial_value):
        row = self.conn.execute(
            "SELECT value, counter FROM storage WHERE key = ?",
            (self.key,)
        ).fetchone()

        if row:
            self._value, self._counter = row
        else:
            self._value = initial_value
            self._counter = 0
            self._save_sqlite()

    def _save_sqlite(self):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO storage (key, value, counter) VALUES (?, ?, ?)",
                (self.key, self._value, self._counter)
            )

    # MySQL 相关逻辑
    def _create_mysql_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage (
                `key` VARCHAR(255) PRIMARY KEY,
                `value` TEXT,
                `counter` INT DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                `key` VARCHAR(255),
                `timestamp` DATETIME,
                `old_value` TEXT
            )
        ''')
        cursor.close()

    def _load_mysql_value(self, initial_value):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value, counter FROM storage WHERE `key` = %s", (self.key,))
        row = cursor.fetchone()

        if row:
            self._value, self._counter = row
        else:
            self._value = initial_value
            self._counter = 0
            self._save_mysql()
        cursor.close()

    def _save_mysql(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "REPLACE INTO storage (`key`, `value`, `counter`) VALUES (%s, %s, %s)",
            (self.key, self._value, self._counter)
        )
        self.conn.commit()
        cursor.close()

    # MongoDB 相关逻辑
    def _load_mongodb_value(self, initial_value):
        document = self.db.storage.find_one({"key": self.key})
        if document:
            self._value = document["value"]
            self._counter = document["counter"]
        else:
            self._value = initial_value
            self._counter = 0
            self._save_mongodb()

    def _save_mongodb(self):
        self.db.storage.update_one(
            {"key": self.key},
            {"$set": {"value": self._value, "counter": self._counter}},
            upsert=True
        )

    # JSON 相关逻辑
    def _load_json_value(self, initial_value):
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        if self.key in data:
            self._value = data[self.key]['value']
            self._counter = data[self.key]['counter']
        else:
            self._value = initial_value
            self._counter = 0
            self._save_json()

    def _save_json(self):
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        data[self.key] = {'value': self._value, 'counter': self._counter}

        with open(JSON_PATH, 'w') as f:
            json.dump(data, f, indent=4)

    @property
    def value(self):
        self._counter += 1
        self._save()
        return self._value

    @value.setter
    def value(self, new_value):
        self._save_history(self._value)
        self._value = new_value
        self._save()

    @property
    def counter(self):
        return self._counter

    def _save_history(self, old_value):
        # 保存历史记录
        if self.storage_type == "sqlite":
            self.conn.execute(
                "INSERT INTO history (key, timestamp, old_value) VALUES (?, ?, ?)",
                (self.key, datetime.now().isoformat(), old_value)
            )
        elif self.storage_type == "mysql":
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO history (`key`, `timestamp`, `old_value`) VALUES (%s, %s, %s)",
                (self.key, datetime.now(), old_value)
            )
            self.conn.commit()
            cursor.close()
        elif self.storage_type == "mongodb":
            self.db.history.insert_one({
                "key": self.key,
                "timestamp": datetime.now().isoformat(),
                "old_value": old_value
            })

    def _save(self):
        if self.storage_type == "sqlite":
            self._save_sqlite()
        elif self.storage_type == "mysql":
            self._save_mysql()
        elif self.storage_type == "mongodb":
            self._save_mongodb()
        else:
            self._save_json()

    def close(self):
        if self.storage_type == "sqlite" or self.storage_type == "mysql":
            self.conn.close()
        elif self.storage_type == "mongodb":
            self.client.close()


def useStorage(key, initial_value, storage_type="json", db_config=None):
    return Storage(key, initial_value, storage_type, db_config)
