__author__ = 'marcoantonioalberoalbero'

from queue import Queue
import threading
from helpers.logging import Log


class Task:
    def __init__(self, env, name):
        self.name = name
        self.parallel_tasks = Queue()
        self.sequential_tasks = Queue()
        self.log = Log().setup(env=env, task_id=__name__ + '.' + name)
        self.log.info('Task initialized')

    def is_runnable(self, task):
        op = getattr(task, "run", None)
        if op and callable(op):
            return True
        return False

    def add_task(self, task, sequential=True):
        if self.is_runnable(task):
            if sequential:
                self.sequential_tasks.put(task)
            else:
                self.parallel_tasks.put(task)

    def run(self):
        self.log.info("running tasks")
        while not self.parallel_tasks.empty():
            task = self.parallel_tasks.get()
            t = threading.Thread(target=task.run)
            t.daemon = True
            t.start()
        while not self.sequential_tasks.empty():
            task = self.sequential_tasks.get()
            task.run()
