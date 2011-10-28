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

    def on_tomb_location_clicked(self, *args, **kwargs):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Create Tomb', filter="*.tomb")
        self.ui.lineEdit_tombpath.setText(filename)
    def on_change_page(self, pagenumber):
        if self.currentPage() == self.ui.wizardPage_progress:
            self.create_tomb()
    def create_tomb(self, *args, **kwargs):
        #FIXME: this will lock up the GUI
        #FIXME: no support for other keypath than "next to tomb"
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

        self.thread = TombCreateThread(self.ui.lineEdit_tombpath.text(), str(self.ui.spinBox_size.value()), keyloc)
        self.thread.finished.connect(partial(self.ui.progressBar.setValue, 100))
        self.thread.terminated.connect(partial(self.ui.progressBar.setValue, 100))
        self.thread.start()

class TombCreateThread(QtCore.QThread):
    def __init__(self, tombpath, size, keypath):
        QtCore.QThread.__init__(self)
        self.tombpath = tombpath
        self.size = size
        self.keypath = keypath

    def run(self):
        Tomb.create(self.tombpath, str(self.size), self.keypath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TombCreateWizard()
    window.show()
    sys.exit(app.exec_())
