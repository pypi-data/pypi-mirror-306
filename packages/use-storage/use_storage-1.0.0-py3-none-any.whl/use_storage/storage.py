import json
import os
from datetime import datetime

# 定义存储目录
STORAGE_DIR = ".usestorage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

class Storage:
    def __init__(self, key, initial_value=''):
        self.key = key
        self.filename = os.path.join(STORAGE_DIR, f"{key}.json")
        self.history_file = os.path.join(STORAGE_DIR, f"{key}_history.json")
        self._load_storage(initial_value)

    def _load_storage(self, initial_value):
        """加载存储，如果文件不存在则使用初始值并创建文件"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
        else:
            data = {"value": initial_value}
            self._save_storage(data)

        self._value = data["value"]

    def _save_storage(self, data):
        """保存数据到对应的 JSON 文件"""
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def _save_history(self, old_value):
        """保存历史记录"""
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
        """获取当前值"""
        return self._value

    @value.setter
    def value(self, new_value):
        """更新值并保存历史记录"""
        # 保存旧值到历史记录
        self._save_history(self._value)

        # 更新当前值并保存到文件
        self._value = new_value
        self._save_storage({"value": new_value})

def useStorage(key, initial_value=''):
    """创建并返回一个 Storage 实例"""
    return Storage(key, initial_value)
