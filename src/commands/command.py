__author__ = 'marcoantonioalberoalbero'

import os
import subprocess
import datetime
from helpers.logging import Log


class Command:
    def __init__(self, config, name):
        self.name = name
        self.config = config
        self.command = None
        self.result = None
        self.env = dict(os.environ)
        self.id = __name__ + '.' + name
        self.start_time = datetime.datetime.now()
        self.log_file = self.id+'-'+self.start_time.strftime("%Y-%m-%d_%H:%M:%S")+'.log'
        # log to its own file
        self.log = Log().setup(config=config, task_id=self.id, log_file=self.log_file)

    def set_command(self, command):
        self.command = command

    def add_env_var(self, key, value):
        self.env[key] = value

    def run(self):
        Log.id_log(self.log, "running command " + self.command)
        self.result = subprocess.Popen(self.command,
                                       shell=True,
                                       env=self.env,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       universal_newlines=True)

        # Poll process for new output until finished
        while True:
            line = self.result.stdout.readline()
            return_code = self.result.poll()
            if isinstance(return_code, int) and not line:
                break
            Log.id_log(self.log, line)
        return return_code
