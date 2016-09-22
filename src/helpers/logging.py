__author__ = 'marcoantonioalberoalbero'

import logging


class Log:

    def __init__(self):
        pass

    def setup(self, env, task_id):
        level = (logging.DEBUG if 'debug' in env.get('global', 'log_level') else logging.INFO)
        log_format = (env.get('global', 'log_format')
                      if env.get('global', 'log_format')
                      else '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(env.get('global', 'program') + '.' + task_id)
        logger.setLevel(level)
        fh = logging.FileHandler(env.get('global', 'log_file'))
        ch = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
