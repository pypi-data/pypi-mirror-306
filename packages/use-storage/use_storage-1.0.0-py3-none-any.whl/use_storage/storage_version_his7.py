import os
import json
import sqlite3
from datetime import datetime

# 定义存储目录
STORAGE_DIR = ".storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

DB_PATH = os.path.join(STORAGE_DIR, "storage.db")
JSON_PATH = os.path.join(STORAGE_DIR, "storage.json")

class Storage:
    def __init__(self, key, initial_value, storage_type="json"):
        self.key = key
        self.storage_type = storage_type

        if storage_type == "sqlite":
            self.conn = sqlite3.connect(DB_PATH)
            self._create_sqlite_tables()
            self._load_sqlite_value(initial_value)
        else:
            self._load_json_value(initial_value)

    def _create_sqlite_tables(self):
        """创建SQLite数据库表"""
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
        """从SQLite数据库加载变量值"""
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

    def _load_json_value(self, initial_value):
        """从JSON文件加载变量值"""
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

    def _save_sqlite(self):
        """保存值和计数到SQLite"""
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO storage (key, value, counter) VALUES (?, ?, ?)",
                (self.key, self._value, self._counter)
            )

    def _save_json(self):
        """保存值和计数到JSON文件"""
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        data[self.key] = {
            'value': self._value,
            'counter': self._counter
        }

        with open(JSON_PATH, 'w') as f:
            json.dump(data, f, indent=4)

    def _save_history(self, old_value):
        """保存历史记录"""
        history = self.history

        history.append({
            "timestamp": datetime.now().isoformat(),
            "old_value": old_value
        })

        if self.storage_type == "sqlite":
            with self.conn:
                self.conn.execute(
                    "INSERT INTO history (key, timestamp, old_value) VALUES (?, ?, ?)",
                    (self.key, datetime.now().isoformat(), old_value)
                )
        else:
            history_file = os.path.join(STORAGE_DIR, f"{self.key}_history.json")
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=4)

    @property
    def value(self):
        """访问变量值并增加计数"""
        self._counter += 1
        if self.storage_type == "sqlite":
            self._save_sqlite()
        else:
            self._save_json()
        return self._value

    @value.setter
    def value(self, new_value):
        """设置新值并保存历史记录"""
        self._save_history(self._value)
        self._value = new_value
        if self.storage_type == "sqlite":
            self._save_sqlite()
        else:
            self._save_json()

    @property
    def history(self):
        """返回变量的历史记录"""
        if self.storage_type == "sqlite":
            rows = self.conn.execute(
                "SELECT timestamp, old_value FROM history WHERE key = ? ORDER BY timestamp",
                (self.key,)
            ).fetchall()
            return [{"timestamp": row[0], "old_value": row[1]} for row in rows]
        else:
            history_file = os.path.join(STORAGE_DIR, f"{self.key}_history.json")
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    return json.load(f)
            return []

    @property
    def counter(self):
        """返回访问次数"""
        return self._counter

    def close(self):
        """关闭数据库连接"""
        if self.storage_type == "sqlite":
            self.conn.close()

def useStorage(key, initial_value, storage_type="json"):
    """根据存储类型创建存储对象"""
    return Storage(key, initial_value, storage_type)
