__author__ = 'marcoantonioalberoalbero'

import logging


class Log:

    def __init__(self):
        self.default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def setup(self, config, task_id, log_dir=None, log_file=None):
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
