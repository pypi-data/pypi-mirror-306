import sqlite3
from datetime import datetime
import os

# 定义存储数据库的路径
STORAGE_DIR = ".storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

DB_PATH = os.path.join(STORAGE_DIR, "storage.db")

class Storage:
    def __init__(self, key, initial_value):
        self.key = key
        self.conn = sqlite3.connect(DB_PATH)
        self._create_tables()
        self._load_or_initialize_value(initial_value)

    def _create_tables(self):
        """创建数据库表用于存储变量和历史记录。"""
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

    def _load_or_initialize_value(self, initial_value):
        """从数据库加载变量值，如果不存在则初始化。"""
        row = self.conn.execute(
            "SELECT value, counter FROM storage WHERE key = ?",
            (self.key,)
        ).fetchone()

        if row:
            self._value, self._counter = row
        else:
            self._value = initial_value
            self._counter = 0
            self._save_to_storage()

    def _save_to_storage(self):
        """将变量的当前值和访问计数保存到数据库。"""
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO storage (key, value, counter) VALUES (?, ?, ?)",
                (self.key, self._value, self._counter)
            )

    def _save_history(self, old_value):
        """将历史记录保存到数据库。"""
        with self.conn:
            self.conn.execute(
                "INSERT INTO history (key, timestamp, old_value) VALUES (?, ?, ?)",
                (self.key, datetime.now().isoformat(), old_value)
            )

    @property
    def value(self):
        """访问变量值时，计数 +1 并返回值。"""
        self._counter += 1
        self._save_to_storage()
        return self._value

    @value.setter
    def value(self, new_value):
        """设置新值时，将旧值保存到历史记录。"""
        self._save_history(self._value)
        self._value = new_value
        self._save_to_storage()

    @property
    def history(self):
        """返回该变量的历史记录。"""
        rows = self.conn.execute(
            "SELECT timestamp, old_value FROM history WHERE key = ? ORDER BY timestamp",
            (self.key,)
        ).fetchall()
        return [{"timestamp": row[0], "old_value": row[1]} for row in rows]

    @property
    def counter(self):
        """返回该变量的访问次数。"""
        return self._counter

    def close(self):
        """关闭数据库连接。"""
        self.conn.close()

def useStorage(key, initial_value):
    return Storage(key, initial_value)
