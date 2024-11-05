# ======================================= 当不使用 mysql 和 mongoDB 时不需要安装其依赖 ===============================================================
import os
import json
import sqlite3
from datetime import datetime

# 可选导入 MySQL 和 MongoDB
try:
    import mysql.connector
except ImportError:
    mysql_connector_available = False
else:
    mysql_connector_available = True

try:
    from pymongo import MongoClient
except ImportError:
    pymongo_available = False
else:
    pymongo_available = True

# 定义存储目录和数据库路径
STORAGE_DIR = ".storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

DB_PATH = os.path.join(STORAGE_DIR, "storage.db")
JSON_PATH = os.path.join(STORAGE_DIR, "storage.json")


class Storage:
    def __init__(self, key, initial_value, storage_type="json", db_config=None, on_change_callback=None):
        self.key = key
        self.storage_type = storage_type
        self.on_change_callback = on_change_callback  # 可选回调函数

        if storage_type == "sqlite":
            self.conn = sqlite3.connect(DB_PATH)
            self._create_sqlite_tables()
            self._load_sqlite_value(initial_value)
        elif storage_type == "mysql":
            if not mysql_connector_available:
                raise ImportError("MySQL support requires `mysql-connector-python`. Install it with `pip install mysql-connector-python`.")
            self.conn = mysql.connector.connect(**db_config)
            self._create_mysql_tables()
            self._load_mysql_value(initial_value)
        elif storage_type == "mongodb":
            if not pymongo_available:
                raise ImportError("MongoDB support requires `pymongo`. Install it with `pip install pymongo`.")
            self.client = MongoClient(db_config["host"])
            self.db = self.client[db_config["database"]]
            self._load_mongodb_value(initial_value)
        else:
            self._load_json_value(initial_value)

    @property
    def value(self):
        self._counter += 1
        self._save()
        return self._value

    @value.setter
    def value(self, new_value):
        old_value = self._value
        self._save_history(old_value)
        self._value = new_value
        self._save()

        # 如果设置了回调函数，则调用回调函数
        if self.on_change_callback:
            self.on_change_callback(self.key, old_value, new_value)

    def _save_history(self, old_value):
        # 保存历史记录
        timestamp = datetime.now().isoformat()
        if self.storage_type == "sqlite":
            self.conn.execute(
                "INSERT INTO history (key, timestamp, old_value) VALUES (?, ?, ?)",
                (self.key, timestamp, old_value)
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
                "timestamp": timestamp,
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
        if self.storage_type in ["sqlite", "mysql"]:
            self.conn.close()
        elif self.storage_type == "mongodb":
            self.client.close()

    # SQLite、MySQL、MongoDB 和 JSON 的加载和保存逻辑省略（保持不变）


def useStorage(key, initial_value, storage_type="json", db_config=None, on_change_callback=None):
    """创建存储对象并支持回调函数"""
    return Storage(key, initial_value, storage_type, db_config, on_change_callback)
