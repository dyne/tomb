import os
import unittest
from tomber import *
from random import randrange
from shutil import rmtree, copyfile


class tomberTester(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.pid = str(os.getpid())
        self.tombfile = '.'.join([self.pid, 'tomb'])
        self.keyfile = '.'.join([self.pid, 'key'])
        self.keyfile2 = '.'.join([self.pid, '2ndkey'])
        self.exhumedkey = '.'.join([self.pid, 'exhumed'])
        self.mountpath = './tmptomb'
        os.mkdir(self.mountpath)
        # generate a passphrase with spaces
        self.passphrase = str(randrange(2 ** 64)).replace("", " ")[1:-1]
        self.passphrase2 = str(randrange(2 ** 64))
        self.imagefile = '.'.join([self.pid, 'jpg'])
        copyfile(
            '/'.join([os.path.dirname(os.path.abspath(__file__)), 'test.jpg']),
            self.imagefile)

    @classmethod
    def tearDownClass(self):
        os.unlink(self.tombfile)
        os.unlink(self.keyfile)
        os.unlink(self.keyfile2)
        os.unlink(self.imagefile)
        os.unlink(self.exhumedkey)
        rmtree(self.mountpath, ignore_errors=True)

    def test_01_dig(self):
        """ Dig a tomb of 10mb"""
        self.assertTrue(tdig(self.tombfile, 10)[0])

    def test_02_forge(self):
        """ Forge a keyfile and set a passphrase """
        self.assertTrue(tforge(self.keyfile, self.passphrase)[0])

    def test_03_lock(self):
        """ Lock created tomb with forged keyfile """
        self.assertTrue(tlock(self.tombfile, self.keyfile, self.passphrase)[0])

    def test_04_open(self):
        """ Open the created tomb with forged keyfile and passhrase """
        self.assertTrue(topen(
                self.tombfile, self.keyfile, self.passphrase, self.mountpath
                )[0]
            )

    def test_05_close(self):
        """ Close the created tomb """
        self.assertTrue(tclose(self.tombfile.split('.')[0])[0])

    def test_06_resize(self):
        """ Resize created tomb to 12mb """
        self.assertTrue(tresize(
                self.tombfile, self.keyfile, self.passphrase, 12
                )[0]
            )

    def test_07_passwd(self):
        """ Change password in keyfile """
        self.assertTrue(tpasswd(
                self.keyfile, self.passphrase2, self.passphrase
                )[0]
            )

    def test_08_bury(self):
        """ Bury keyfile in a image file """
        self.assertTrue(tbury(
                self.keyfile, self.passphrase2, self.imagefile
                )[0]
            )

    def test_09_exhume(self):
        """ Exhume a key from an image """
        self.assertTrue(texhume(
                self.exhumedkey, self.passphrase2, self.imagefile
                )[0]
            )

    def test_10_setkey(self):
        """ Forge a new key and and set different keyfile to created tomb """
        tforge(self.keyfile2, self.passphrase)
        self.assertTrue(tsetkey(
                self.keyfile,
                self.tombfile,
                self.keyfile2,
                self.passphrase2,
                self.passphrase
                )[0]
            )

    def test_11_slam(self):
        """ Slam open tombs """
        topen(self.tombfile, self.keyfile2, self.passphrase, self.mountpath)
        self.assertTrue(tslam()[0])

if __name__ == '__main__':
    unittest.main()
