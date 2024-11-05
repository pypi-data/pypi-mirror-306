# ================== 基于 version_2 但是加了默认值逻辑 '' ===================
import json
import os
from datetime import datetime

# 定义存储目录
STORAGE_DIR = ".storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

class Storage:
    def __init__(self, key, initial_value='', filename="storage.json"):
        self.key = key
        self.filename = os.path.join(STORAGE_DIR, filename)
        self.history_file = os.path.join(STORAGE_DIR, f"{key}_history.json")
        self._load_storage(initial_value)

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

    @property
    def value(self):
        return self._value

# (54|57) 67 77 87 **
# (26|32) **

    @value.setter
    def value(self, new_value):
        # Save the current value to history before updating
        self._save_history(self._value)

        # Update the value in memory and save to storage
        self._value = new_value
        with open(self.filename, 'r') as f:
            data = json.load(f)

        data[self.key] = new_value
        self._save_storage(data)

def useStorage(key, initial_value):
    return Storage(key, initial_value)
