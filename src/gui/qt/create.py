import sys, os
from PyQt4.QtGui import QApplication, QWizard
from PyQt4 import QtCore
from ui_create import Ui_Wizard

parentdir = sys.path[0].split(os.sep)[:-1]
sys.path.append(os.sep.join(parentdir))
from tomblib import wrapper

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

        QtCore.QObject.connect(self, QtCore.SIGNAL(_fromUtf8('finished(int)')), self.create_tomb)

    def create_tomb(self, *args, **kwargs):
        print 'creating'
        wrapper.Tomb.create(1,2,3)
        print 'created!'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TombCreateWizard()
    window.show()
    sys.exit(app.exec_())
