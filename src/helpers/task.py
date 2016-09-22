__author__ = 'marcoantonioalberoalbero'

from queue import Queue
import threading
from helpers.logging import Log


class Task:

    def __init__(self, env, name):
        self.name = name
        self.log = Log.setup(env, __name__)
        self.log.info('Task ' + self.name + ' initialized')

    def test(self):
        self.log('Test')