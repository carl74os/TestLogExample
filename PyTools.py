# coding: utf-8
import math
import os
import sys
import time
import argparse
import subprocess

LF = '\n'


# ######################################################################################################################
# The base class of the python tools
class PyToolsBase:
    # ##################################################################################################################
    def __init__(self, name, version, desc):
        self._tool_name = name
        self._tool_version = version
        self._tool_desc = desc

    # ##################################################################################################################
    def logDesc(self):
        sys.stdout.write(self._tool_name + ' (' + self._tool_version + ') - ' + self._tool_desc + LF)


# ######################################################################################################################
# Class for formatting the command line argument output
class PythonChecker(PyToolsBase):
    # General information
    _NAME = 'Python Interpreter Checker'
    _DESCRIPTION = 'The class provides a checker method to verify the installed Python version.'
    _VERSION = '0.1.0.0 - 18.12.2020'

    # ##################################################################################################################
    def __init__(self):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

    # ##################################################################################################################
    @staticmethod
    def check(min_version=(3, 6)):
        if sys.version_info < min_version:
            sys_ver = '{0}.{1}'.format(sys.version_info.major, sys.version_info.minor)
            min_ver = '{0}.{1}'.format(min_version[0], min_version[1])
            raise Exception(
                'Python interpreter ({0}) is too old. A newer version (>={1}) is needed.'.format(sys_ver, min_ver))


# ######################################################################################################################
# Class for formatting the command line argument output
class SmartFormatter(argparse.HelpFormatter):
    # ##################################################################################################################
    # noinspection PyShadowingNames
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


# ######################################################################################################################
# Class for logging information, warnings and errors
class Logger(PyToolsBase):
    # General information
    _NAME = 'Logger'
    _DESCRIPTION = 'The class provides method for logging information, warnings and errors to the console.'
    _VERSION = '0.1.0.0 - 18.12.2020'

    # ##################################################################################################################
    def __init__(self):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

        # Time measurement variable
        self._start_time = time.time()

    # ##################################################################################################################
    def logInfoStart(self, text, dots=True):
        """
        :param text:    Start information text to be logged.
        :param dots:    True contains dots at the end else no dots.
        :return:        None
        """
        self._start_time = time.time()
        self._log('[INFO]: ' + text + ('...' if dots else ''))

    # ##################################################################################################################
    def logInfoEnd(self, text=None, errs=None):
        """
        :param text:    End information text to be logged.
        :param errs:    Errors to be logged if any
        :return:        None
        """
        if errs is None or len(errs) == 0:
            output = ' Done ({:.3f} s, ' + text + ')\n' if text else ' Done ({:.3f} s)\n'
            self._log(output.format((time.time() - self._start_time)))
        else:
            output = ' Error ({:.3f} s, ' + text + ')\n' if text else ' Error ({:.3f} s)\n'
            self._log(output.format((time.time() - self._start_time)))
            for err in errs:
                self.logErr(err)

    # ##################################################################################################################
    def log(self, text):
        """
        :param text:    Text to be logged.
        :return:        None
        """
        self._log(text + '\n')

    # ##################################################################################################################
    def logInfo(self, text):
        """
        :param text:    Information text to be logged.
        :return:        None
        """
        self._log('[INFO]: ' + text + '\n')

    # ##################################################################################################################
    def logErr(self, text):
        """
        :param text:    Error text to be logged.
        :return:        None
        """
        self._log('[ERROR]: ' + text + '\n')

    # ##################################################################################################################
    def logWarn(self, text):
        """
        :param text:    Warning text to be logged.
        :return:        None
        """
        self._log('[WARNING]: ' + text + '\n')

    # ##################################################################################################################
    def progress(self, count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total))) if total > 0 else 0

        percents = round(100.0 * count / float(total), 1) if total > 0 else 0
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('\033[2K\033[1G')
        self._log('[%s] %s%s  %s\r' % (bar, percents, '%', suffix))

    # ##################################################################################################################
    @staticmethod
    def _log(text):
        """
        :param text:    Text to be logged.
        :return:        None
        """
        sys.stdout.write(text)
        sys.stdout.flush()


# ######################################################################################################################
# Class for special file system functionalities
class FS(PyToolsBase):
    # General information
    _NAME = 'File System Helper'
    _DESCRIPTION = 'The class provides special file system functionality.'
    _VERSION = '0.2.0.0 - 26.02.2021'

    # ##################################################################################################################
    def __init__(self):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

    # ##################################################################################################################
    @staticmethod
    def expand(name: str):
        return os.path.expanduser(os.path.expandvars(name))

    # ##################################################################################################################
    @staticmethod
    def fileExpandAndExists(file_name: str, root_path: str = ''):
        fname: str = os.path.expanduser(os.path.expandvars(file_name))
        if os.path.isfile(fname) is False:
            fname = os.path.join(root_path, file_name)
            if os.path.isfile(file_name) is False:
                raise Exception('The file {0} does not exist!'.format(file_name))

        return os.path.abspath(fname)

    # ##################################################################################################################
    @staticmethod
    def fileExpandAndDirExists(file_name: str, root_path: str = ''):
        fname: str = os.path.expanduser(os.path.expandvars(file_name))
        if os.path.isdir(os.path.dirname(fname)) is False:
            fname = os.path.join(root_path, fname)
            if os.path.isdir(os.path.dirname(fname)) is False:
                raise Exception(
                    'The directory {0} of the file {1} does not exist!'.format(os.path.dirname(fname), file_name))

        return os.path.abspath(fname)

    # ##################################################################################################################
    @staticmethod
    def pathExpandAndExists(path_name: str, root_path: str = ''):
        dname: str = os.path.expanduser(os.path.expandvars(path_name))
        if os.path.isdir(dname) is False:
            dname = os.path.join(root_path, dname)
            if os.path.isdir(dname) is False:
                raise Exception('The directory {0} does not exist!'.format(path_name))

        return os.path.abspath(dname)


# ######################################################################################################################
# Class for system process functionalities
class ProcessHelper(PyToolsBase):
    # General information
    _NAME = 'System Process Helper'
    _DESCRIPTION = 'The class provides system process functionality.'
    _VERSION = '0.1.0.0 - 08.12.2021'

    # ##################################################################################################################
    def __init__(self):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

    # ######################################################################################################################
    @staticmethod
    def runCmd(cmd):
        # Perform the command
        output: str = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode(
            'utf-8')
        return output.split(LF) if output and output.strip() else list()

    # ######################################################################################################################
    @staticmethod
    def runCmdPipe(cmd):
        # Perform the command
        output: str = subprocess.check_output(cmd, shell=True).decode('utf-8')
        return output.split(LF) if output and output.strip() else list()


# ######################################################################################################################
# Class for simple supporting functionalities
class SimpleSupporter(PyToolsBase):
    # General information
    _NAME = 'Simple Supporter'
    _DESCRIPTION = 'The class provides simple supporting functionalities.'
    _VERSION = '0.1.0.0 - 09.12.2021'

    # ##################################################################################################################
    def __init__(self):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

    # ##################################################################################################################
    @staticmethod
    def convTo(num: int, suffix: str = 'B') -> str:
        UNIT: list = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']
        magnitude = int(math.floor(math.log(num, 1024)))
        val = num / math.pow(1024, magnitude)
        return '{:.1f} {}{}'.format(val, 'Yi', suffix) if magnitude > 7 else '{:3.2f} {}{}'.format(val, UNIT[magnitude],
                                                                                                   suffix)

    # ##################################################################################################################
    @staticmethod
    def convToFix(num: int, suffix: str = 'B', unit: str = 'Ki', show_unit: bool = True) -> str:
        UNIT: list = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']
        magnitude = UNIT.index(unit)
        val = num / math.pow(1024, magnitude)
        if show_unit is True:
            return '{:.2f} {}{}'.format(val, 'Yi', suffix) if magnitude > 7 else '{:3.2f} {}{}'.format(val,
                                                                                                       UNIT[magnitude],
                                                                                                       suffix)
        else:
            return '{:.2f}'.format(val) if magnitude > 7 else '{:3.2f}'.format(val)

    # ##################################################################################################################
    @staticmethod
    def isDebuggerActive() -> bool:
        """Return if the debugger is currently active"""
        gettrace = getattr(sys, 'gettrace', lambda: None)
        return gettrace() is not None
