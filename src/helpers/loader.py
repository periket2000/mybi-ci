__author__ = 'marcoantonioalberoalbero'
from helpers.task import Task
from commands.command import Command
import helpers


class Loader:

    env = helpers.env.read_config()

    @staticmethod
    def load(json):
        if "cmd" in json:
            result = Loader.load_command(json)
        else:
            result = Loader.load_task(json)
        return result

    @staticmethod
    def load_task(json):
        task = Task(Loader.env, json["id"])
        if "parallel_tasks" in json:
            for t in json["parallel_tasks"]:
                if Loader.is_command(t):
                    task.add_task(Loader.load_command(t), sequential=False)
                else:
                    task.add_task(Loader.load_task(t), sequential=False)
        if "sequential_tasks" in json:
            for t in json["sequential_tasks"]:
                if Loader.is_command(t):
                    task.add_task(Loader.load_command(t))
                else:
                    task.add_task(Loader.load_task(t))
        return task

    @staticmethod
    def load_command(json):
        cmd = Command(Loader.env, json["id"])
        if "env" in json:
            for entry in json["env"]:
                for k in entry.keys():
                    cmd.add_env_var(k, entry[k])
        if "cmd" in json:
            cmd.set_command(json["cmd"])
        return cmd

    @staticmethod
    def is_command(json):
        if "cmd" in json:
            return True
        else:
            return False