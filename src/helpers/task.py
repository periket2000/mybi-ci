__author__ = 'marcoantonioalberoalbero'

from queue import Queue
import threading
from helpers.logging import Log


class Task:

    def __init__(self, env, name):
        self.name = name
        self.log = Log().setup(env=env, task_id=__name__ + '.' + name)
        self.log.info('Task initialized')

    def test(self):
        self.log.info('Test')