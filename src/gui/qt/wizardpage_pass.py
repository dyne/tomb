'''
This module provide some methods to enhance the password page
of the wizard. It could have been avoided, but this way make
it easier to do things from the designer.

Indeed, it's possible to use password_match(bool) signal
and check_password_match(slot) from the designer.
'''

from PyQt4.QtGui import QWizardPage
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
class WizardPage_pass(QWizardPage):
    password_match = QtCore.pyqtSignal(bool)
    def __init__(self, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)
    def _password_match(self):
        pass1 = self.findChild(QtGui.QLineEdit, _fromUtf8('lineEdit_pass')).text()
        pass2 = self.findChild(QtGui.QLineEdit, _fromUtf8('lineEdit_pass_again')).text()
        return pass1 == pass2
    def check_password_match(self):
        self.password_match.emit(not self._password_match())
        self.completeChanged.emit()
    def isComplete(self): #this will make the "Next" button disabled if password doesn't match
        return self._password_match()



