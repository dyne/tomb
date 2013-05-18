import sys,os
import time
from tempfile import NamedTemporaryFile

from PyQt4 import QtCore

parentdir = sys.path[0].split(os.sep)[:-1]
sys.path.append(os.sep.join(parentdir))
from tomblib.tomb import Tomb
from tomblib.parser import parse_line

class TombCreateThread(QtCore.QThread):
    line_received = QtCore.pyqtSignal(QtCore.QString)
    error_received = QtCore.pyqtSignal(QtCore.QString)
    def __init__(self, tombpath, size, keypath, **opts):
        QtCore.QThread.__init__(self)
        self.tombpath = tombpath
        self.size = size
        self.keypath = keypath
        self.opts = opts

        self.err_thread = TombOutputThread()
        self.err_thread.line_received.connect(self.line_received)
        self.err_thread.error_received.connect(self.error_received)

    def run(self):
        self.err_thread.start()
        self.status = Tomb.create(str(self.tombpath), str(self.size),
                self.keypath, stderr=self.err_thread.buffer, **self.opts)
#        self.err_thread.terminate()
    
    def get_success(self):
        return self.status

class TombOutputThread(QtCore.QThread):
    line_received = QtCore.pyqtSignal(QtCore.QString)
    error_received = QtCore.pyqtSignal(QtCore.QString)
    progressed = QtCore.pyqtSignal(int) #value in percent

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.buffer = NamedTemporaryFile()

    def run(self):
        while True:
            where = self.buffer.tell()
            line = self.buffer.readline()
            if not line:
                time.sleep(1)
                self.buffer.seek(where)
            else:
                #ansi color escapes messes this up, but it'ok anyway
                self.line_received.emit(line)
                self.parse_line(line)

    def parse_line(self, line):
        #This could be simplified, and s/search/match, if --no-color supported
        #see #59
        #TODO: this should be moved to tomblib.parse
        parsed = parse_line(line)
        if parsed and parsed['type'] == 'error':
            self.error_received.emit(parsed.content)
