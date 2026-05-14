from dataclasses import dataclass
from typing import Callable

class EventEmitter:
    def __init__(self): self._listeners = {}
    def on(self, event, cb): self._listeners.setdefault(event, []).append(cb)
    def emit(self, event, *args):
        for cb in self._listeners.get(event, []): cb(*args)

@dataclass
class Task: title: str; priority: int

class TaskModel(EventEmitter):
    def __init__(self):
        super().__init__()
        self.tasks = []
    def add(self, title, p):
        t = Task(title, p)
        self.tasks.append(t)
        self.emit("added", t)

class TaskView:
    def render(self, tasks):
        print("\n--- Список завдань ---")
        for i, t in enumerate(tasks): print(f"{i}. {t.title} (Пріоритет: {t.priority})")

class TaskController:
    def __init__(self, model, view):
        self.model, self.view = model, view
        self.model.on("added", lambda t: print(f"Нове завдання: {t.title}"))
    def add_task(self, title, p): self.model.add(title, p)
    def refresh(self): self.view.render(self.model.tasks)

def main():
    m, v = TaskModel(), TaskView()
    c = TaskController(m, v)
    c.add_task("Закрити лабу", 1)
    c.refresh()

if __name__ == "__main__": main()
