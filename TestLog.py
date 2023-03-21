# coding: utf-8
import shutil
import time
import signal

from PyTools import PythonChecker, Logger, PyToolsBase

MIN_PYTHON_VERSION = (3, 8)
NAME = 'Test Log Example'
DESCRIPTION = 'This is an example which divides the terminal screen into a body and tail part and logs to these parts.'
VERSION = '0.1.0.0 - 21.03.2023'
NONE_TOKEN = 'N/A'

LF = '\n'

# Global logger variable
logger_g: Logger = Logger()


# ######################################################################################################################
# Class of the defines
class Defines:
    # Keys
    KEY_ITEMS: str = 'list_log_files'


# ######################################################################################################################
# Class for logging information, warnings and errors
class Logger_(PyToolsBase):
    # General information
    _NAME = 'Logger'
    _DESCRIPTION = 'The class provides method for logging information, warnings and errors to the console.'
    _VERSION = '0.1.0.0 - 18.12.2020'

    # ##################################################################################################################
    def __init__(self, tail_size: int, border_char: str = '-'):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

        # Initialize the protected variables
        self._tail_size: int = tail_size
        self._border_char: str = border_char
        self.__setUp__()

        # Register the terminal resize signal
        signal.signal(signal.SIGWINCH, self.__termResizedHdlr__)

        # Clear the screen
        self.clearScr()

    # ######################################################################################################################
    def clearScr(self):
        self.__setUp__()
        self.__scrollPageDown__(1)
        self.__moveCur__(self._border_pos_y, 1)
        logger_g.log('\033[2K' + self._border)
        for idx in range(self._tail_size):
            self.logTail(idx, '')

    # ######################################################################################################################
    def log(self, text: str):
        # Check whether end of body window has been reached.
        if len(self._body) >= self._body_size:
            # Remove the first line of the body and scroll one line up
            self._body.pop(0)
            self.__moveCur__(self._scr_size_y, 1)

            # Append the given text
            self._body.append(text)

            # Move the cursor to the top of the window and display the body, border and tailer
            self.__moveCur__(self._body_pos_y, self._body_pos_x)
            logger_g.log('\n'.join(['\033[2K' + line for line in self._body]))
            logger_g.log('\033[2K' + self._border)
            logger_g.log('\n'.join(['\033[2K' + line for line in self._tail]))
        else:
            # Append the given text
            self._body.append(text)
            
            # Move the cursor to the top of the window and display the body
            self.__moveCur__(self._body_pos_y, self._body_pos_x)
            logger_g.log('\n'.join(['\033[2K' + line for line in self._body]))

    # ######################################################################################################################
    def logTail(self, idx: int, text):
        # Check whether the tail index is in range. In this case log the tailer
        if self._tail_size > idx:
            self._tail[idx] = text
            self.__moveCur__(self._tail_pos_y + idx, 1)
            logger_g.log('\033[2K' + text)

    # ##################################################################################################################
    def progress(self, idx, count, total, suffix=''):
        # Prepare the progress bar
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total))) if total > 0 else 0

        percents = round(100.0 * count / float(total), 1) if total > 0 else 0
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        # Log to tailer
        self.logTail(idx, '[%s] %s%s  %s' % (bar, percents, '%', suffix))

    # ######################################################################################################################
    def __setUp__(self):
        # Initialize the protected variables
        (self._scr_size_x, self._scr_size_y) = shutil.get_terminal_size((80, 20))
        self._body: list = list()
        (self._body_pos_x, self._body_pos_y) = (1, 1)
        self._body_size: int = self._scr_size_y - self._tail_size - 1
        self._tail = [''] * self._tail_size
        (self._tail_pos_x, self._tail_pos_y) = (1, (self._scr_size_y - self._tail_size - 1))
        self._border: str = self._scr_size_x * self._border_char
        self._border_pos_y = self._scr_size_y - self._tail_size - 2

    # ######################################################################################################################
    def __termResizedHdlr__(self, signum, frame):
        # Reinitialize the logger
        self.__setUp__()

    # ######################################################################################################################
    def __scrollPageDown__(self, nb_pages: int):
        print('\033[%dT' % (self._scr_size_y * nb_pages))

    # ######################################################################################################################
    @staticmethod
    def __moveCur__(row, column):
        print("\033[%d;%dH" % (row, column))


logger1_g: Logger_ = Logger_(3)

# ######################################################################################################################

# Main method, entry point
if __name__ == "__main__":
    # Check interpreter
    PythonChecker().check(MIN_PYTHON_VERSION)

    for idx in range(1000):
        logger1_g.log('{0} BODY'.format(idx))
        logger1_g.progress(0, idx, 1000, 'Performing...')
        logger1_g.logTail(1, 'Index: {0}'.format(idx))
        logger1_g.logTail(2, 'Index * 3: {0}'.format(3 * idx))
        time.sleep(0.05)
