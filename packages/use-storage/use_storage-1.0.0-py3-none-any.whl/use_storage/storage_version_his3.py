import json
import os
from datetime import datetime

# 定义存储目录
STORAGE_DIR = ".storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

class Storage:
    def __init__(self, key, initial_value, filename="storage.json"):
        self.key = key
        self.filename = os.path.join(STORAGE_DIR, filename)
        self.history_file = os.path.join(STORAGE_DIR, f"{key}_history.json")
        self.counter_file = os.path.join(STORAGE_DIR, f"{key}_counter.json")
        self._load_storage(initial_value)
        self._load_counter()

    def _load_storage(self, initial_value):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        if self.key not in data:
            data[self.key] = initial_value
            self._save_storage(data)

        self._value = data[self.key]

    def _load_counter(self):
        # 初始化访问计数为0
        if os.path.exists(self.counter_file):
            with open(self.counter_file, 'r') as f:
                self._counter = json.load(f).get('count', 0)
        else:
            self._counter = 0
            self._save_counter()

    def _save_storage(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def _save_history(self, old_value):
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                history = json.load(f)

        history.append({
            "timestamp": datetime.now().isoformat(),
            "old_value": old_value
        })

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=4)

    def _save_counter(self):
        with open(self.counter_file, 'w') as f:
            json.dump({'count': self._counter}, f, indent=4)

    @property
    def value(self):
        # 每次访问时增加计数
        self._counter += 1
        self._save_counter()
        return self._value

    @value.setter
    def value(self, new_value):
        # 保存当前值到历史记录
        self._save_history(self._value)

        # 更新值并保存到存储
        self._value = new_value
        with open(self.filename, 'r') as f:
            data = json.load(f)

        data[self.key] = new_value
        self._save_storage(data)

def useStorage(key, initial_value):
    return Storage(key, initial_value)
