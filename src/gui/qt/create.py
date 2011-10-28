import sys, os
from functools import partial

from PyQt4.QtGui import QApplication, QWizard
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_create import Ui_Wizard

parentdir = sys.path[0].split(os.sep)[:-1]
sys.path.append(os.sep.join(parentdir))
from tomblib.tomb import Tomb

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class TombCreateWizard(QWizard):
    def __init__(self, *args, **kwargs):
        QWizard.__init__(self, *args, **kwargs)
        self.ui = ui = Ui_Wizard()
        ui.setupUi(self)
        
        ui.wizardPage_tomb_location.registerField('tombpath*', ui.lineEdit_tombpath) #required field, note the *
        ui.wizardPage_key_location.setCommitPage(True)

        QtCore.QObject.connect(ui.button_tombpath, QtCore.SIGNAL(_fromUtf8('clicked()')), self.on_tomb_location_clicked)
        QtCore.QObject.connect(self, QtCore.SIGNAL(_fromUtf8('currentIdChanged(int)')), self.on_change_page)
        def check_progress_complete(*args, **kwargs):
            if self.ui.progressBar.value() == 100:
                return True
            return False
        self.ui.wizardPage_progress.isComplete = check_progress_complete
        self.finished.connect(self.on_finish)

    def _keyloc(self):
        keyloc = None
        if self.ui.radioButton_usb.isChecked():
            print 'Warning: it is not supported'
            raise NotImplementedError
        elif self.ui.radioButton_near.isChecked():
            print 'going near'
            keyloc = None
        else:
            keyloc = self.ui.lineEdit_custom.text()
            if not keyloc:
                raise ValueError
        return keyloc

    def on_tomb_location_clicked(self, *args, **kwargs):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Create Tomb', filter="*.tomb")
        self.ui.lineEdit_tombpath.setText(filename)
    def on_change_page(self, pagenumber):
        if self.currentPage() == self.ui.wizardPage_progress:
            self.create_tomb()

    def on_finish(self, finishedint):
        if self.currentPage() != self.ui.wizardPage_end:
            #there has been an error
            return

        if self.ui.checkBox_open.isChecked():
            Tomb.open(self.ui.lineEdit_tombpath.text(), self._keyloc())
    def on_thread_creation_finished(self):
        if self.thread.get_success():
            self.ui.progressBar.setValue(100)
        else:
            self.ui.progressBar.setEnabled(False)
            self.ui.label_progress.setText('Error while creating the tomb!')
            self.ui.wizardPage_progress.setFinalPage(True)
        self.ui.wizardPage_progress.completeChanged.emit()
    def create_tomb(self, *args, **kwargs):
        #TODO: report error
        keyloc = self._keyloc()
        self.thread = TombCreateThread(self.ui.lineEdit_tombpath.text(), str(self.ui.spinBox_size.value()), self._keyloc())
        self.thread.finished.connect(self.on_thread_creation_finished)
        self.thread.terminated.connect(self.on_thread_creation_finished)
        self.thread.start()

class TombCreateThread(QtCore.QThread):
    def __init__(self, tombpath, size, keypath):
        QtCore.QThread.__init__(self)
        self.tombpath = tombpath
        self.size = size
        self.keypath = keypath

    def run(self):
        self.status = Tomb.create(self.tombpath, str(self.size), self.keypath)
    
    def get_success(self):
        return self.status

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TombCreateWizard()
    window.show()
    sys.exit(app.exec_())
