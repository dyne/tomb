# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tombqt/open_tombfile.ui'
#
# Created: Tue Jan 24 00:49:10 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_tombfile(object):
    def setupUi(self, tombfile):
        tombfile.setObjectName(_fromUtf8("tombfile"))
        tombfile.resize(480, 640)
        self.verticalLayout_2 = QtGui.QVBoxLayout(tombfile)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 276, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(tombfile)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tomb_line = QtGui.QLineEdit(tombfile)
        self.tomb_line.setObjectName(_fromUtf8("tomb_line"))
        self.horizontalLayout.addWidget(self.tomb_line)
        self.tomb_browse = QtGui.QPushButton(tombfile)
        self.tomb_browse.setObjectName(_fromUtf8("tomb_browse"))
        self.horizontalLayout.addWidget(self.tomb_browse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 276, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.retranslateUi(tombfile)
        QtCore.QMetaObject.connectSlotsByName(tombfile)

    def retranslateUi(self, tombfile):
        tombfile.setWindowTitle(QtGui.QApplication.translate("tombfile", "WizardPage", None, QtGui.QApplication.UnicodeUTF8))
        tombfile.setTitle(QtGui.QApplication.translate("tombfile", "Choose tomb", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("tombfile", "Choose a tomb file on your filesystem", None, QtGui.QApplication.UnicodeUTF8))
        self.tomb_line.setPlaceholderText(QtGui.QApplication.translate("tombfile", "/path/to/your.tomb", None, QtGui.QApplication.UnicodeUTF8))
        self.tomb_browse.setText(QtGui.QApplication.translate("tombfile", "Browse", None, QtGui.QApplication.UnicodeUTF8))

