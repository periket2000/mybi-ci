__author__ = 'marcoantonioalberoalbero'

from queue import Queue
import threading
import datetime
from helpers.logging import Log


class Task:
    def __init__(self, config, name):
        self.name = name
        self.config = config
        self.parallel_tasks = Queue()
        self.sequential_tasks = Queue()
        self.id = __name__ + '.' + name
        self.start_time = datetime.datetime.now()
        self.log_file = self.id+'-'+self.start_time.strftime("%Y-%m-%d_%H:%M:%S")+'.log'
        # log to its own file
        self.log = Log().setup(config=config, task_id=self.id, log_file=self.log_file)

    def is_runnable(self, task):
        op = getattr(task, "run", None)
        if op and callable(op):
            return True
        return False

    def set_log(self, l_dir=None, l_file=None, consolidate=True):
        if consolidate:
            # log to the consolidated file (here it breaks with its own logger, it's not part of the logger hierarchy)
            tid = 'consolidated.' + self.id
        else:
            # log to its own logger and to this new child logger (because it's part of the logger hierarchy)
            tid = self.id + '.child.log'
        self.log = Log().setup(config=self.config, task_id=tid, log_dir=l_dir, log_file=l_file)

    def add_task(self, task, sequential=True):
        if self.is_runnable(task):
            if sequential:
                self.sequential_tasks.put(task)
            else:
                self.parallel_tasks.put(task)

    def run(self):
        self.log.info("running task " + self.name)
        while not self.parallel_tasks.empty():
            task = self.parallel_tasks.get()
            t = threading.Thread(target=task.run)
            t.daemon = True
            t.start()
        while not self.sequential_tasks.empty():
            task = self.sequential_tasks.get()
            task.run()
