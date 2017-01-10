# -*- coding: utf8 -*-

"""

tomber - a python Tomb (the Crypto Undertaker) wrapper
To use tomber you need to install Tomb (https://github.com/dyne/Tomb)
Copyright © 2014, Federico reiven <reiven_at_gmail.com>
Licensed under BSD License.
See also LICENSE file

"""


from subprocess import Popen, PIPE
from tools import parser


def get_message(stderr, type):
    """
    Helper to return exit messages from command execution
    """
    response = []
    for line in stderr.split('\n'):
        ret = parser.parse_line(line)
        if ret and ret['type'] == type:
            if not 'swaps' in ret['content']:
                response.append(ret['content'])
    return response


def execute(cmd):
    """
    Execute given cmd. return boolean based on exit status and error string
    """
    p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    if p_status == 0:
        return True, get_message(stderr, 'success')
    else:
        return False, get_message(stderr, 'error')


def sanitize_passphrase(passphrase):
    """
    Used to avoid errors with passphrases which include spaces
    """
    return ''.join(['"', passphrase, '"'])


def tdig(tombfile, size, force=False):
    """
    Dig a tomb of given size
    """
    cmd = ' '.join(['tomb', 'dig', tombfile, '-s', str(size), '--no-color'])
    if force:
        cmd += " -f"
    return execute(cmd)


def tforge(keyfile, passphrase, force=False):
    """
    Forge a key with given passphrase
    """
    cmd = ' '.join(['tomb',
        'forge',
        keyfile,
        '--unsafe',
        '--tomb-pwd',
        sanitize_passphrase(passphrase),
        '--no-color'])
    if force:
        cmd += " -f"
    return execute(cmd)


def tlock(tombfile, keyfile, passphrase):
    """
    Lock a tomb file with given key and passphrase.
    """
    cmd = ' '.join(['tomb',
        'lock',
        tombfile,
        '-k',
        keyfile,
        '--unsafe',
        '--tomb-pwd',
        sanitize_passphrase(passphrase),
        '--no-color'])
    return execute(cmd)


def topen(tombfile, keyfile, passphrase, mountpath=False):
    """
    Open (mount) a tomb.
    Keyfile and passphrase are needed, mountpoint is optional
    """
    if not mountpath:
        mountpath = ''
    cmd = ' '.join(['tomb',
        'open',
        tombfile,
        '-k',
        keyfile,
        '--unsafe',
        '--tomb-pwd',
        sanitize_passphrase(passphrase),
        '--no-color',
        mountpath])
    return execute(cmd)


def tclose(tombfile):
    """
    Close (umount) a tomb
    """
    cmd = ' '.join(['tomb', 'close', tombfile, '--no-color'])
    return execute(cmd)


def tresize(tombfile, keyfile, passphrase, newsize):
    """
    Resize a tomb.
    Keyfile, passphrase and new size are needed.
    """
    cmd = ' '.join(['tomb',
        'resize',
        tombfile,
        '-k',
        keyfile,
        '--unsafe',
        '--tomb-pwd',
        sanitize_passphrase(passphrase),
        '-s',
        str(newsize),
        '--no-color'])
    return execute(cmd)


def tbury(keyfile, passphrase, imagefile):
    """
    Bury a key inside a jpg file
    """
    cmd = ' '.join(['tomb',
        'bury',
        '-k',
        keyfile,
        '--unsafe',
        '--tomb-pwd',
        sanitize_passphrase(passphrase),
        imagefile,
        '--no-color'])
    return execute(cmd)


def texhume(keyfile, passphrase, imagefile):
    """
    Exhume (recover) key from jpg file. Passphrase for key is needed
    """
    cmd = ' '.join(['tomb',
        'exhume',
        '-k',
        keyfile,
        '--unsafe',
        '--tomb-pwd',
        sanitize_passphrase(passphrase),
        imagefile,
        '--no-color'])
    return execute(cmd)


def tpasswd(keyfile, newpassphrase, oldpassphrase):
    """
    Change current passphrase from keyfile
    """
    cmd = ' '.join(['tomb',
        'passwd',
        '-k',
        keyfile,
        '--unsafe',
        '--tomb-pwd',
        sanitize_passphrase(newpassphrase),
        '--tomb-old-pwd',
        sanitize_passphrase(oldpassphrase),
        '--no-color'])
    return execute(cmd)


def tsetkey(oldkeyfile, tombfile, newkeyfile, newpassphrase, oldpassphrase):
    """
    Change lock key for a tomb
    The old key+passphrase and new key+passphrase are needed
    """
    cmd = ' '.join(['tomb',
        'setkey',
        '-k',
        newkeyfile,
        oldkeyfile,
        tombfile,
        '--unsafe',
        '--tomb-old-pwd',
        sanitize_passphrase(newpassphrase),
        '--tomb-pwd',
        sanitize_passphrase(oldpassphrase),
        '--no-color'])
    return execute(cmd)


def tslam():
    """
    Slam tombs, killing all programs using it
    """
    cmd = ' '.join(['tomb', 'slam'])
    return execute(cmd)
