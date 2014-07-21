import sys

from PyQt4 import QtCore, QtGui

from ui_open_tombfile import Ui_tombfile
from ui_open_keymethod import Ui_keymethod
from ui_open_success import Ui_success

from tomblib.tomb import Tomb
from tomblib.undertaker import Undertaker

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class TombfilePage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args)
        self.ui = Ui_tombfile()
        self.ui.setupUi(self)
        if 'tombfile' in kwargs and kwargs['tombfile'] is not None:
            self.ui.tomb_line.setText(kwargs['tombfile'])
        self.ui.tomb_browse.clicked.connect(self.on_tomb_location_clicked)
    def on_tomb_location_clicked(self, *args, **kwargs):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Select Tomb',
                filter="Tomb (*.tomb)")
        self.ui.tomb_line.setText(filename)

class MethodPage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)
        self.ui = Ui_keymethod()
        self.ui.setupUi(self)
        self.group = group = QtGui.QButtonGroup()
        for radio in self.children():
            if type(radio) == QtGui.QRadioButton:
                group.addButton(radio)

    def initializePage(self):
        self.found = Undertaker.check( str('near://' + self.wizard().get_tombfile()) ) or []
        box = self.ui.radio_layout

        for key in self.found:
            radio = QtGui.QRadioButton('Automatically found: ' + key, parent=self)
            radio.setChecked(True)
            radio.setProperty('path', key)
            box.insertWidget(0, radio)
            self.group.addButton(radio)


    def nextId(self):
        '''Virtual method reimplemented to decide next page'''
        if self.ui.fs.isChecked():
            keyfile = QtGui.QFileDialog.getOpenFileName(self.wizard(), 'Key file',
                    filter="Tomb keys (*.tomb.key);;Buried keys (*.jpeg)")
            if keyfile:
                #TODO: check if this really is a success :)
                if Tomb.open(self.wizard().get_tombfile(), keyfile): #bugs when wrong password
                    return TombOpenWizard.SUCCESS_PAGE
                #else: #TODO: should alert the user that we failed
            return TombOpenWizard.METHOD_PAGE
        if self.ui.usb.isChecked():
            return TombOpenWizard.USB_PAGE
        print self.group.checkedButton().property('path').toPyObject()
        return TombOpenWizard.SUCCESS_PAGE

class SuccessPage(QtGui.QWizardPage):
    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)
        self.ui = Ui_success()
        self.ui.setupUi(self)

class TombOpenWizard(QtGui.QWizard):
    TOMBFILE_PAGE=1
    METHOD_PAGE=2
    SUCCESS_PAGE=99
    USB_PAGE=20
    def __init__(self, *args, **kwargs):
        QtGui.QWizard.__init__(self, *args)
        self.setPage(TombOpenWizard.TOMBFILE_PAGE,
                TombfilePage(self, tombfile = kwargs['tombfile']
                    if 'tombfile' in kwargs else None))
        self.setPage(TombOpenWizard.METHOD_PAGE, MethodPage(self))
        self.setPage(TombOpenWizard.SUCCESS_PAGE, SuccessPage(self))
        if 'tombfile' in kwargs and kwargs['tombfile'] is not None:
            self.setStartId(TombOpenWizard.METHOD_PAGE)

    def get_tombfile(self):
        page = self.page(TombOpenWizard.TOMBFILE_PAGE)
        return page.ui.tomb_line.text()

        

def run_open_wizard():
    app = QtGui.QApplication(sys.argv)
    window = TombOpenWizard(tombfile=sys.argv[1] if len(sys.argv) > 1 else None)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    Undertaker.undertakerexec = '/home/davide/coding/projects/tomb/src/undertaker'
    run_open_wizard()






