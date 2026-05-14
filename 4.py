import json
from abc import ABC, abstractmethod
from datetime import datetime

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class JSONFormatter(ABC):
    def format(self, level, message):
        return json.dumps({"level": level, "msg": message, "time": str(datetime.now())})

class Logger(metaclass=SingletonMeta):
    def __init__(self): self.history = []
    def log(self, msg): 
        formatted = f"[{datetime.now()}] {msg}"
        self.history.append(formatted)
        print(formatted)

def main():
    l1, l2 = Logger(), Logger()
    print(f"Це один об'єкт? {l1 is l2}")
    l1.log("Тест Singleton")

if __name__ == "__main__": main()
