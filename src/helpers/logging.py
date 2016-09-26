__author__ = 'marcoantonioalberoalbero'

import logging
import uuid


class Log:

    config = None

    def __init__(self):
        self.default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def setup(self, config, task_id, log_dir=None, log_file=None):
        Log.config = config
        level = (logging.DEBUG if 'debug' in config.get('global', 'log_level') else logging.INFO)
        log_format = (config.get('global', 'log_format')
                      if config.get('global', 'log_format')
                      else self.default_format)
        logger = logging.getLogger(config.get('global', 'program') + '.' + task_id)
        logger.setLevel(level)
        ld = (log_dir if log_dir else config.get('global', 'log_dir'))
        lf = (log_file if log_file else config.get('global', 'log_file'))
        fh = logging.FileHandler(ld+'/'+lf)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    @staticmethod
    def id_log(logger=None, msg=None, level=logging.INFO):
        """
        Log with a uuid for track the log of the task/command
        :param logger: logger who's going to log
        :param msg: message to log
        :param level: level to log
        :return:
        """
        if logger and msg and level == logging.INFO:
            logger.info(str(uuid.uuid1()) + " - " + msg)
        if logger and msg and level == logging.DEBUG:
            logger.debug(str(uuid.uuid1()) + " - " + msg)

    @staticmethod
    def set_log(task, l_dir=None, l_file=None, consolidate_only=True):
        """
        Adds the logger with logger_id new loggers to log with
        :param task: the task to configure the log for
        :param l_dir: log directory
        :param l_file: log file
        :param consolidate_only: if only consolidate the log or not
        :return:
        """
        if consolidate_only:
            # log to the consolidated file (here it breaks with its own logger, it's not part of the logger hierarchy)
            tid = 'consolidated.' + task.id
        else:
            # log to its own logger and to this new child logger (because it's part of the logger hierarchy)
            tid = task.id + '.child.log'
        task.log = Log().setup(config=Log.config, task_id=tid, log_dir=l_dir, log_file=l_file)
