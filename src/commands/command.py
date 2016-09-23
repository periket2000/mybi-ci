__author__ = 'marcoantonioalberoalbero'

import os, subprocess
from helpers.logging import Log


class Command:
    def __init__(self, env, name):
        self.name = name
        self.command = None
        self.result = None
        self.env = dict(os.environ)
        self.log = Log().setup(env=env, task_id=__name__ + '.' + name)
        self.log.info('Command initialized')

    def set_command(self, command):
        self.command = command

    def add_env_var(self, key, value):
        self.env[key] = value

    def run(self):
        self.log.info("running command " + self.command)
        self.result = subprocess.Popen(self.command,
                                       shell=True,
                                       env=self.env,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       universal_newlines=True)

        # Poll process for new output until finished
        while True:
            return_code = self.result.poll()
            if isinstance(return_code, int):
                break
            line = self.result.stdout.readline()
            self.log.info(line)
        return return_code
