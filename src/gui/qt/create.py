import sys, os
from PyQt4.QtGui import QApplication, QWizard
from PyQt4 import QtCore
from ui_create import Ui_Wizard

parentdir = sys.path[0].split(os.sep)[:-1]
sys.path.append(os.sep.join(parentdir))
from tomblib import wrapper

app = QApplication(sys.argv)
window = QWizard()
ui = Ui_Wizard()
ui.setupUi(window)

def create_tomb(*args, **kwargs):
    print 'creating'
    wrapper.Tomb.create(1,2,3)
    print 'created!'

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
QtCore.QObject.connect(window, QtCore.SIGNAL(_fromUtf8('finished(int)')), create_tomb)

window.show()
sys.exit(app.exec_())


