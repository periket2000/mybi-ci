__author__ = 'marcoantonioalberoalbero'

import optparse
import os.path
import sys

# Support vars.
ENDL = "\n"
usage = """
\twhere options are:
\t\t -v => show the tool's version
\t\t -u file_path => upload mode
\t\t -d download_link [destination_file_path] => download mode
"""


class Executor:
    """ Class for execute the ci engine """
    def __init__(self):
        self.parser = optparse.OptionParser(usage='usage: %prog [options]'+usage)
        self.parser.add_option('-u', '--upload', action='store_true', default=False, help='upload mode')
        self.parser.add_option('-d', '--download', action='store_true', default=False, help='download mode')
        self.parser.add_option('-v', '--version', action='store_true', default=False, help='version number')

    def run(self, args):
        (options, arguments) = self.parser.parse_args(args)

        if options.version:
            print('todo')
            sys.exit(0)
        self.parser.print_usage()
