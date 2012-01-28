# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tombqt/open_success.ui'
#
# Created: Mon Jan 23 23:06:38 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_success(object):
    def setupUi(self, success):
        success.setObjectName(_fromUtf8("success"))
        success.resize(480, 640)
        self.verticalLayout = QtGui.QVBoxLayout(success)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(success)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(success)
        QtCore.QMetaObject.connectSlotsByName(success)

    def retranslateUi(self, success):
        success.setWindowTitle(QtGui.QApplication.translate("success", "WizardPage", None, QtGui.QApplication.UnicodeUTF8))
        success.setTitle(QtGui.QApplication.translate("success", "Tomb opened", None, QtGui.QApplication.UnicodeUTF8))
        success.setSubTitle(QtGui.QApplication.translate("success", "success", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("success", "You successfully opened the tomb", None, QtGui.QApplication.UnicodeUTF8))

