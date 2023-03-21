# coding: utf-8
import shutil
import time

from PyTools import PythonChecker, Logger

MIN_PYTHON_VERSION = (3, 8)
NAME = 'Unit Test Executor'
DESCRIPTION = 'Executes unit tests and presents a summary at the end (Python >=3.8).'
VERSION = '0.1.0.0 - 18.03.2023'
NONE_TOKEN = 'N/A'

LF = '\n'

# Global logger variable
logger_g = Logger()


# ######################################################################################################################
# Class of the defines
class Defines:
    # Keys
    KEY_ITEMS: str = 'list_log_files'


# ######################################################################################################################
def clearScr():
    print('\033[2J')


# ######################################################################################################################
def scrollPageDown(nb_pages: int):
    (size_x, size_y) = shutil.get_terminal_size((80, 20))
    print('\033[%dT' % (size_y * nb_pages))


# ######################################################################################################################
def scrollLineDown(nb_lines: int):
    print('\033[%dE' % nb_lines)


# ######################################################################################################################
def clearCurrLine():
    print('\033[2K')


# ######################################################################################################################
def moveCur(row, column):
    print("\033[%d;%dH" % (row, column))


# ######################################################################################################################
def updateLogWin(body: list, tail: list):
    startTime: float = time.time()
    end_offset: int = 3

    # Calculate section positions
    (size_x, size_y) = shutil.get_terminal_size((80, 20))
    body_size: int = size_y - (1 + len(tail) + end_offset)
    body_pos_x: int = 0
    body_pos_y: int = 0
    tail_pos_x: int = 0
    tail_pos_y: int = body_size

    # Prepare the section border string
    sec_border: str = size_x * '-'

    # Log body
    body_idx: int = len(body) - body_size
    if body_idx <= 0:
        body_idx = 0
    else:
        moveCur(size_y, 0)
    moveCur(body_pos_y, body_pos_x)
    logger_g.log('\n'.join(['\033[2K' + line for line in body[body_idx:]]))

    # Log tailer
    moveCur(tail_pos_y, tail_pos_x)
    logger_g.log('\033[2K' + sec_border)
    logger_g.log('\n'.join(['\033[2K' + line for line in tail]))
    logger_g.log('Duration: {:6f}'.format(time.time() - startTime))


# ######################################################################################################################

# Main method, entry point
if __name__ == "__main__":
    # Check interpreter
    PythonChecker().check(MIN_PYTHON_VERSION)

    # Scroll one page down to clear the screen
    scrollPageDown(1)

    body: list = list()
    tail: list = ['', '', '']
    for idx in range(100):
        updateLogWin(body, tail)
        body.append('{0} BODY'.format(idx))
        tail.pop(0)
        tail.append('{0} TAIL'.format(idx))
        time.sleep(0.05)

