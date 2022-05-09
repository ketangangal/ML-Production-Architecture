import os
from datetime import datetime
from from_root import from_root


class CustomLogger:

    def __init__(self, log_file_name):
        """
        :param log_file_name: name of the logfile
        """
        self.logfile = os.path.join(from_root(), "logging", log_file_name + str('.txt'))
        self.current_date = str(datetime.now())

    def info(self, message):
        """
        :arg message: message to write in the log file
        """
        try:
            with open(self.logfile, 'a+') as logs:
                logs.write(f'INFO [{self.current_date}]: {message}.\n')

        except Exception as e:
            with open(self.logfile, 'w') as logs:
                logs.write(f'INFO [{self.current_date}]: {message}.\n')

    def error(self, message):
        """
        :arg message: message to write in the log file
        """
        try:
            with open(self.logfile, 'a+') as logs:
                logs.write(f'ERROR [{self.current_date}]: {message}.\n')

        except Exception as e:
            with open(self.logfile, 'w') as logs:
                logs.write(f'ERROR [{self.current_date}]: {message}.\n')
