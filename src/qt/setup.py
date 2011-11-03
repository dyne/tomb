import os
import glob
from setuptools import setup
from StringIO import StringIO

from distutils import log
from distutils.core import Command
from distutils.dep_util import newer

class build_ui(Command):
# Stolen from picard
    description = "build Qt UI files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from PyQt4 import uic
        for uifile in glob.glob("tombqt/*.ui"):
            pyfile = "ui_%s.py" % os.path.splitext(os.path.basename(uifile))[0]
            pyfile = os.path.join('tombqt', pyfile)
            if newer(uifile, pyfile):
                log.info("compiling %s -> %s", uifile, pyfile)
                tmp = StringIO()
                uic.compileUi(uifile, tmp)
                source = tmp.getvalue()
                f = open(pyfile, "w")
                f.write(source)
                f.close()

setup(
        name = 'TombQt',
        version = '0.1',
        packages = ['tombqt'],
        cmdclass = {
            'build_ui': build_ui
            }
)




