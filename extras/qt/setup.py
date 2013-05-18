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
        url = 'http://tomb.dyne.org/',
        author = 'boyska',
        author_email = 'piuttosto@logorroici.org',
        version = '0.1',
        packages = ['tombqt'],
        cmdclass = {
            'build_ui': build_ui
            },
        entry_points = {
            'gui_scripts': [
                'tomb-qt-create = tombqt.create:run_create_wizard',
                'tomb-qt-open = tombqt.open:run_open_wizard'
                ]
            },
        classifiers = [
            'Topic :: Security :: Cryptography',
            'Intended Audience :: End Users/Desktop',
            'Operating System :: POSIX :: Linux',
            'Environment :: X11 Applications :: Qt',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Development Status :: 3 - Alpha'
            ]
)




