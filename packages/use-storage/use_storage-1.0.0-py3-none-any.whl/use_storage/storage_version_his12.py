# ================================================================== 添加全文检索支持 =========================================================================================================
import os
import json
import sqlite3
from collections import defaultdict
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
    def __init__(self, key, initial_value, storage_type="json", db_config=None):
        self.key = key
        self.storage_type = storage_type

        if storage_type == "sqlite":
            self.conn = sqlite3.connect(DB_PATH)
            self._create_sqlite_tables()
            self._load_sqlite_value(initial_value)
        elif storage_type == "mysql":
            if not mysql_connector_available:
                raise ImportError("Install `mysql-connector-python` for MySQL support.")
            self.conn = mysql.connector.connect(**db_config)
            self._create_mysql_tables()
            self._load_mysql_value(initial_value)
        elif storage_type == "mongodb":
            if not pymongo_available:
                raise ImportError("Install `pymongo` for MongoDB support.")
            self.client = MongoClient(db_config["host"])
            self.db = self.client[db_config["database"]]
            self._load_mongodb_value(initial_value)
        else:
            self._load_json_value(initial_value)

    # SQLite 全文搜索逻辑
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
                CREATE VIRTUAL TABLE IF NOT EXISTS storage_fts USING fts5(
                    key, value
                )
            ''')

    def search_sqlite(self, query):
        cursor = self.conn.execute(
            "SELECT key, value FROM storage_fts WHERE value MATCH ?",
            (query,)
        )
        return cursor.fetchall()

    # MySQL 全文搜索逻辑
    def _create_mysql_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage (
                `key` VARCHAR(255) PRIMARY KEY,
                `value` TEXT,
                `counter` INT DEFAULT 0,
                FULLTEXT(value)
            )
        ''')
        cursor.close()

    def search_mysql(self, query):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT key, value FROM storage WHERE MATCH(value) AGAINST (%s IN NATURAL LANGUAGE MODE)",
            (query,)
        )
        results = cursor.fetchall()
        cursor.close()
        return results

    # MongoDB 全文搜索逻辑
    def search_mongodb(self, query):
        results = self.db.storage.find({"$text": {"$search": query}})
        return [(doc["key"], doc["value"]) for doc in results]

    # JSON 全文搜索逻辑
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

    def search_json(self, query):
        if not os.path.exists(JSON_PATH):
            return []

        with open(JSON_PATH, 'r') as f:
            data = json.load(f)

        results = [
            (key, info['value'])
            for key, info in data.items()
            if query.lower() in info['value'].lower()
        ]
        return results

    def search(self, query):
        """根据存储类型执行搜索。"""
        if self.storage_type == "sqlite":
            return self.search_sqlite(query)
        elif self.storage_type == "mysql":
            return self.search_mysql(query)
        elif self.storage_type == "mongodb":
            return self.search_mongodb(query)
        else:
            return self.search_json(query)

    def close(self):
        if self.storage_type in ["sqlite", "mysql"]:
            self.conn.close()
        elif self.storage_type == "mongodb":
            self.client.close()


def useStorage(key, initial_value, storage_type="json", db_config=None):
    """创建存储对象。"""
    return Storage(key, initial_value, storage_type, db_config)
