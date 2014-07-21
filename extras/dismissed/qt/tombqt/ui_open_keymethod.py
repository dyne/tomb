# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tombqt/open_keymethod.ui'
#
# Created: Sat Jan 28 03:36:11 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_keymethod(object):
    def setupUi(self, keymethod):
        keymethod.setObjectName(_fromUtf8("keymethod"))
        keymethod.resize(480, 640)
        self.verticalLayout = QtGui.QVBoxLayout(keymethod)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 265, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.radio_layout = QtGui.QVBoxLayout()
        self.radio_layout.setObjectName(_fromUtf8("radio_layout"))
        self.fs = QtGui.QRadioButton(keymethod)
        self.fs.setObjectName(_fromUtf8("fs"))
        self.radio_layout.addWidget(self.fs)
        self.usb = QtGui.QRadioButton(keymethod)
        self.usb.setEnabled(False)
        self.usb.setObjectName(_fromUtf8("usb"))
        self.radio_layout.addWidget(self.usb)
        self.bluetooth = QtGui.QRadioButton(keymethod)
        self.bluetooth.setEnabled(False)
        self.bluetooth.setObjectName(_fromUtf8("bluetooth"))
        self.radio_layout.addWidget(self.bluetooth)
        self.verticalLayout.addLayout(self.radio_layout)
        spacerItem1 = QtGui.QSpacerItem(20, 265, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(keymethod)
        QtCore.QMetaObject.connectSlotsByName(keymethod)

    def retranslateUi(self, keymethod):
        keymethod.setWindowTitle(QtGui.QApplication.translate("keymethod", "WizardPage", None, QtGui.QApplication.UnicodeUTF8))
        keymethod.setTitle(QtGui.QApplication.translate("keymethod", "Choose key", None, QtGui.QApplication.UnicodeUTF8))
        self.fs.setText(QtGui.QApplication.translate("keymethod", "Filesystem", None, QtGui.QApplication.UnicodeUTF8))
        self.usb.setText(QtGui.QApplication.translate("keymethod", "USB drive", None, QtGui.QApplication.UnicodeUTF8))
        self.bluetooth.setText(QtGui.QApplication.translate("keymethod", "Retrieve via bluetooth (advanced)", None, QtGui.QApplication.UnicodeUTF8))

