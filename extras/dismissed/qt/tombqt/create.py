import sys, os

from PyQt4.QtGui import QApplication, QWizard
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_create import Ui_Wizard

if __name__ == '__main__':
    parentdir = sys.path[0].split(os.sep)[:-1]
    sys.path.append(os.sep.join(parentdir))
from tomblib.tomb import Tomb
from worker import TombCreateThread

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class TombCreateWizard(QWizard):
    def __init__(self, *args, **kwargs):
        QWizard.__init__(self, *args, **kwargs)
        self.ui = ui = Ui_Wizard()
        ui.setupUi(self)
        #instance attributes:
        self.ignore_swap = False
        self._tomb_check = False #ugly; it's used by check_progress_complete

        ui.wizardPage_tomb_location.registerField('tombpath*',
                ui.lineEdit_tombpath) #required field, note the *
        ui.wizardPage_key_location.setCommitPage(True)

        QtCore.QObject.connect(ui.button_tombpath,
                QtCore.SIGNAL(_fromUtf8('clicked()')),
                self.on_tomb_location_clicked)
        QtCore.QObject.connect(self,
                QtCore.SIGNAL(_fromUtf8('currentIdChanged(int)')),
                self.on_change_page)
        QtCore.QObject.connect(ui.radioButton_swapoff,
                QtCore.SIGNAL(_fromUtf8('toggled(bool)')),
                ui.wizardPage_check.completeChanged)
        QtCore.QObject.connect(ui.radioButton_ignore,
                QtCore.SIGNAL(_fromUtf8('toggled(bool)')),
                ui.wizardPage_check.completeChanged)
        def check_progress_complete(*args, **kwargs):
            if self.ui.progressBar.value() == 100:
                return True
            return False
        def check_is_solved():
            if self._tomb_check:
                return True
            if self.ui.radioButton_swapoff.isChecked() or \
                    self.ui.radioButton_ignore.isChecked():
                return True
            return False
        self.ui.wizardPage_progress.isComplete = check_progress_complete
        self.ui.wizardPage_check.isComplete = check_is_solved
        self.ui.groupBox_swap.setVisible(False)
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
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Create Tomb',
                filter="Tomb(*.tomb)")
        self.ui.lineEdit_tombpath.setText(filename)
    def on_change_page(self, pagenumber):
        if self.currentPage() == self.ui.wizardPage_progress:
            self.create_tomb()
        if self.currentPage() == self.ui.wizardPage_check:
            self.check_requisite()

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
    def create_tomb(self):
        self.thread = TombCreateThread(self.ui.lineEdit_tombpath.text(),
                str(self.ui.spinBox_size.value()), self._keyloc(),
                no_color=False, ignore_swap=self.ui.radioButton_ignore.isChecked())
        self.thread.finished.connect(self.on_thread_creation_finished)
        self.thread.terminated.connect(self.on_thread_creation_finished)
        self.thread.line_received.connect(self.ui.textBrowser_log.append)
        def err_append_to_log(text):
            self.ui.textBrowser_log.append('Error: <strong>' + text +
                    '</strong>')
        self.thread.error_received.connect(err_append_to_log)
        self.thread.start()
    def check_requisite(self):
        self._tomb_check = check = Tomb.check('create', no_color=False)
        self.ui.wizardPage_check.completeChanged.emit()
        if check:
            self.ui.label_check.setText('Everything seems fine!')
            return
        self.ui.label_check.setText('Some error occurred')
        if Tomb.check('create', no_color=False, ignore_swap=True): # swap is the only error
            self.ui.groupBox_swap.setVisible(True)
            #TODO: support swapoff
            #TODO: calculate the amount of ram available vs swap used
            self.ui.radioButton_swapoff.setEnabled(False)
            self.ui.label_swapoff.setEnabled(False)


def run_create_wizard():
    app = QApplication(sys.argv)
    window = TombCreateWizard()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_create_wizard()

