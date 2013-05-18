from setuptools import setup

setup(
        name = 'TombLib',
        url = 'http://tomb.dyne.org/',
        author = 'boyska',
        author_email = 'piuttosto@logorroici.org',
        version = '1.1',
        packages = ['tomblib'],

        test_suite = 'nose.collector',
        classifiers = [
            'Topic :: Security :: Cryptography',
            'Intended Audience :: Developers',
            'Operating System :: POSIX :: Linux',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Development Status :: 3 - Alpha'
        ]
)


