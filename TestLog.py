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
def clearCurrLine():
    print('\033[2K')


# ######################################################################################################################
def moveCur(row, column):
    print("\033[%d;%dH" % (row, column))


# ######################################################################################################################
def updateLogWin(head: list, body: list, tail: list):
    startTime: float = time.time()
    end_offset: int = 3

    # Calculate section positions
    (size_x, size_y) = shutil.get_terminal_size((80, 20))
    head_size: int = len(head) + 1 + 1
    body_size: int = size_y - (1 + len(tail) + end_offset)
    head_pos_x: int = 0
    head_pos_y: int = 0
    body_pos_x: int = 0
    body_pos_y: int = head_size
    full: bool = False
    tail_pos_x: int = 0
    tail_pos_y: int = body_size

    # Prepare the section border string
    sec_border: str = size_x * '-'

    # Clear the screen
    # clearScr()

    # Set cursor position to the top of the screen
    moveCur(0, 0)

    # Log header
    moveCur(head_pos_y, head_pos_x)
    logger_g.log('\n'.join(['\033[2K' + line for line in head]))
    logger_g.log('\033[2K' + sec_border)

    # Log body
    moveCur(body_pos_y, body_pos_x)
    body_idx: int = len(body) - (body_size - head_size)
    logger_g.log('\n'.join(['\033[2K' + line for line in (body if body_idx < 0 else body[body_idx:])]))

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

    head: list = ['', '']
    body: list = list()
    tail: list = ['', '', '']
    for idx in range(100):
        updateLogWin(head, body, tail)
        head.pop(0)
        head.append('{0} HEAD'.format(idx))
        body.append('{0} BODY'.format(idx))
        tail.pop(0)
        tail.append('{0} TAIL'.format(idx))
        time.sleep(0.2)
