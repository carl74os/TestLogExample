# coding: utf-8
import hashlib
import math
import os
import sys
import time
import argparse
import subprocess
import re
import platform
import fnmatch
from datetime import datetime

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
            raise Exception('Python interpreter ({0}) is too old. A newer version (>={1}) is needed.'.format(sys_ver, min_ver))


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
    _VERSION = '0.3.0.0 - 09.11.2022'

    # ##################################################################################################################
    def __init__(self):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

        # Set the logging to console flag
        self._log_on: bool = True

        # Store the private members
        self._log_file: str = None

        # Time measurement variables
        self._start_time: float = time.time()
        self._start_time_log: float = time.time()
        self._time_log_text: str = ''

    # ##################################################################################################################
    def setLogFile(self, log_file: str, info: str = ''):
        """
        :param log_file:    The name of the log file.
        :param info:        Additional information to be added at the beginning of the file
        :return:            None
        """
        self._log_file = log_file
        date_str: str = datetime.now().strftime('%d.%m.%Y, %H:%M:%S')
        log_str: str = r'===                            Logging ({0})                            ==='.format(date_str) + LF
        if info:
            log_str += 'INFO: ' + info + LF
        log_str += r'===========================================================================' + LF
        open(self._log_file, 'w').write(log_str)

    # ##################################################################################################################
    def setLogOn(self, flag: bool = True):
        """
        :param flag:        The flag for enabling or disabling the logging
        :return:            None
        """
        self._log_on = flag

    # ##################################################################################################################
    def logStartTime(self):
        """
        :return:        None
        """
        self._start_time_log = time.time()
        self._log('[INFO]: Time logging started.' + LF)

    # ##################################################################################################################
    def logElapsedTime(self):
        """
        :return:        None
        """
        output = '[INFO]: Time elapsed: {:.3f} s.'
        self._log(output.format((time.time() - self._start_time_log)) + LF)

    # ##################################################################################################################
    def logStopTime(self):
        """
        :return:        None
        """
        output = '[INFO]: Time logging stopped: {:.3f} s.'
        self._log(output.format((time.time() - self._start_time_log)) + LF)

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
            output = (' Done ({:.3f} s, ' + text + ')' if text else ' Done ({:.3f} s)') + LF
            self._log(output.format((time.time() - self._start_time)))
        else:
            output = (' Error ({:.3f} s, ' + text + ')' if text else ' Error ({:.3f} s)') + LF
            self._log(output.format((time.time() - self._start_time)))
            for err in errs:
                self.logErr(err)

    # ##################################################################################################################
    def log(self, text):
        """
        :param text:    Text to be logged.
        :return:        None
        """
        self._log(text + LF)

    # ##################################################################################################################
    def logInfo(self, text):
        """
        :param text:    Information text to be logged.
        :return:        None
        """
        self._log('[INFO]: ' + text + LF)

    # ##################################################################################################################
    def logErr(self, text):
        """
        :param text:    Error text to be logged.
        :return:        None
        """
        self._log('[ERROR]: ' + text + LF)

    # ##################################################################################################################
    def logWarn(self, text):
        """
        :param text:    Warning text to be logged.
        :return:        None
        """
        self._log('[WARNING]: ' + text + LF)

    # ##################################################################################################################
    def logInfoFileOnly(self, text):
        """
        :param text:    Text to be logged.
        :return:        None
        """
        # Log to file if necessary
        open(self._log_file, 'a+').write('[INFO-FILE]: ' + text + LF) if self._log_file else None

    # ##################################################################################################################
    def progress(self, count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total))) if total > 0 else 0

        percents = round(100.0 * count / float(total), 1) if total > 0 else 0
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('\033[2K\033[1G') if platform.system() != 'Windows' and self._log_on else None
        self._log('[%s] %s%s (%s/%s)  %s\r' % (bar, percents, '%', count, total, suffix), (True if total == count else False))

    # ##################################################################################################################
    def _log(self, text, log_to_file: bool = True):
        """
        :param text:    Text to be logged.
        :return:        None
        """
        # Write to standard out
        if self._log_on:
            sys.stdout.write(text)
            sys.stdout.flush()

        # Log to file if necessary
        open(self._log_file, 'a+').write(text) if self._log_file and log_to_file else None


# ######################################################################################################################
# Class for special file system functionalities
class FS(PyToolsBase):
    # General information
    _NAME = 'File System Helper'
    _DESCRIPTION = 'The class provides special file system functionality.'
    _VERSION = '0.4.0.0 - 17.03.2023'

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
            if os.path.isfile(fname) is False:
                raise Exception('The file {0} does not exist!'.format(file_name))

        return os.path.abspath(fname)

    # ##################################################################################################################
    @staticmethod
    def fileExpandAndDirExists(file_name: str, root_path: str = ''):
        fname: str = os.path.expanduser(os.path.expandvars(file_name))
        if os.path.isdir(os.path.dirname(fname)) is False:
            fname = os.path.join(root_path, fname)
            if os.path.isdir(os.path.dirname(fname)) is False:
                raise Exception('The directory {0} of the file {1} does not exist!'.format(os.path.dirname(fname), file_name))

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

    # ##################################################################################################################
    @staticmethod
    def collectAllFiles(root_path: str, recursive: bool = True, file_name_patt: str = r'.*', log: Logger = None,
                        log_prefix: str = 'Collecting files...') -> list:
        file_list: list = list()
        fn_patt: re = re.compile(file_name_patt)

        # Walk through the current folder
        for root, dirs, files in os.walk(root_path):
            _cnt: int = len(file_list)
            _total: int = _cnt + len(files)
            for file in files:
                _cnt += 1
                log.progress(_cnt, _total, log_prefix) if log else None
                file_list.append(os.path.join(root, file)) if fn_patt.match(file) else None
            if not recursive:
                break

        # Finish the progress bar
        total: int = len(file_list)
        log.progress(total, total, log_prefix + ' (Done)' + LF) if log else None

        return file_list

    # ##################################################################################################################
    @staticmethod
    def md5(file: str, chunk_size: int = 64 * 1024):
        # Create the MD5 checksum calculator
        md5 = hashlib.md5()

        # Open the file and start calculating the MD5 checksum
        with open(file, 'rb') as fh:
            while chunk := fh.read(chunk_size):
                md5.update(chunk)

        return md5.hexdigest()

    # ##################################################################################################################
    @staticmethod
    def size(file: str):
        return os.path.getsize(file)


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
        output: str = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8')
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
    _VERSION = '0.2.0.0 - 27.10.2020'

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
        return '{:.1f} {}{}'.format(val, 'Yi', suffix) if magnitude > 7 else '{:3.2f} {}{}'.format(val, UNIT[magnitude], suffix)

    # ##################################################################################################################
    @staticmethod
    def convToFix(num: int, suffix: str = 'B', unit: str = 'Ki', show_unit: bool = True) -> str:
        UNIT: list = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']
        magnitude = UNIT.index(unit)
        val = num / math.pow(1024, magnitude)
        if show_unit is True:
            return '{:.2f} {}{}'.format(val, 'Yi', suffix) if magnitude > 7 else '{:3.2f} {}{}'.format(val, UNIT[magnitude],
                                                                                                       suffix)
        else:
            return '{:.2f}'.format(val) if magnitude > 7 else '{:3.2f}'.format(val)

    # ##################################################################################################################
    @staticmethod
    def isDebuggerActive() -> bool:
        """Return if the debugger is currently active"""
        gettrace = getattr(sys, 'gettrace', lambda: None)
        return gettrace() is not None

    # ##################################################################################################################
    @staticmethod
    def validateRegEx(patt: str) -> str:
        try:
            re.compile(patt)
        except re.error:
            raise Exception('The regular expression pattern \"{0}\" is not valid.'.format(patt))

        return patt


# ######################################################################################################################
# Class for compressing and extracting files using the 7zip archiver
class SevenZipper(PyToolsBase):
    # General information
    _NAME = 'Seven Zipper'
    _DESCRIPTION = 'The class provides methods for compressing and extracting files using the 7zip archiver.'
    _VERSION = '0.1.0.0 - 05.08.2022'

    # Some constants
    DEFAULT_PROG_NAME: str = '7z.exe' if platform.system() == 'Windows' else '7z'

    # ##################################################################################################################
    def __init__(self, prog_name: str = DEFAULT_PROG_NAME, prog_path: str = ''):
        # Initialize the base class
        PyToolsBase.__init__(self, self._NAME, self._VERSION, self._DESCRIPTION)

        # Store the program name and path of the 7zip archiver
        self.name: str = prog_name
        self.path: str = prog_path

        # Find the 7zip executable and prepare its file path
        self._prog, self.path = self.__findProg__()

        # Get the 7zip version
        self.version: str = self.__getVersion__()

    # ##################################################################################################################
    def isValid(self) -> bool:
        return True if self._prog else False

    # ##################################################################################################################
    def findFiles(self, archive: str, file_filter: str) -> list:
        return self.__find__(archive, file_filter)

    # ##################################################################################################################
    def find1stFile(self, archive: str, file_filter: str) -> list:
        files: list = self.__find__(archive, file_filter)
        return files[0] if files else None

    # ##################################################################################################################
    def listFiles(self, archive: str) -> list:
        return self.__list__(archive)

    # ##################################################################################################################
    def extractFile(self, archive: str, file_path: str, to: str) -> str:
        return self.__extract__(archive, file_path, to)

    # ##################################################################################################################
    def extract1stFile(self, archive: str, file_filter: str, to: str) -> str:
        # Find the first file
        files: list = self.__find__(archive, file_filter)
        file_path: str = files[0] if files else None

        # Check whether no file found. In this case raise an exception.
        if not files:
            raise Exception(r'No file found for extracting of the given file filter "' + file_filter + '"!')

        return self.__extract__(archive, file_path, to)

    # ##################################################################################################################
    def __findProg__(self) -> str:
        prog: str = ''

        # Prepare the paths to be searched
        dirs: list = list()
        if self.path:
            dirs.append(self.path)
        else:
            if platform.system() == 'Windows':
                dirs.append(os.environ.get('PROGRAMFILES'))
                dirs.append(os.environ.get('PROGRAMFILES(X86)'))
            else:
                dirs.append(os.path.dirname(ProcessHelper.runCmd(['which', self.name])[0]))
            dirs.extend(sys.path)

        # Search for the 7zip archiver
        for dir in dirs:
            files: list = FS.collectAllFiles(root_path=dir, file_name_patt=self.name)
            if files:
                prog = files[0]
                break

        return prog, os.path.dirname(prog)

    # ##################################################################################################################
    def __getVersion__(self) -> str:
        version: str = 'Unknown'
        rx_version: re = re.compile(r'^\s*7\-Zip\s+(.*?)\s*:\s*(.*?)$')
        if self._prog:
            for line in ProcessHelper.runCmd([self._prog, '--help']):
                m = rx_version.match(line)
                if m:
                    version = m.group(1) + r' "' + m.group(2).strip() + r'"'
                    break

        return version

    # ##################################################################################################################
    def __list__(self, archive: str) -> listFiles:
        files: list = list()
        rx_file: re = re.compile(r'^\s*Path\s*=\s*(.*?)$')

        # List the content of the archive and collect all files
        for line in ProcessHelper.runCmd([self._prog, 'l', '-slt', archive]):
            m = rx_file.match(line)
            files.append(m.group(1).strip()) if m else None

        return files

    # ##################################################################################################################
    def __find__(self, archive: str, filter: str) -> listFiles:
        return fnmatch.filter(self.__list__(archive), filter)

    # ##################################################################################################################
    def __extract__(self, archive: str, file_path: str, to: str) -> str:
        _size: int = 0
        status: bool = False
        rx_size: re = re.compile(r'^\s*Size\s*:\s*([0-9]+)\s*$')

        # List the content of the archive and collect all files
        output: list = ProcessHelper.runCmd([self._prog, 'e', archive, r'-o' + to, file_path])
        for line in output:
            line = line.strip()
            if not status and line != 'Everything is Ok':
                continue
            status = True
            m = rx_size.match(line)
            if m:
                _size = int(m.group(1))
                break

        # Check whether the extraction of the file failed
        if _size == 0:
            raise Exception(r'Could not extract the file "{0}"'.format(file_path) + LF + output)

        return os.path.join(to, os.path.basename(file_path))
