'''
Module structure:

this contain a class, which is indeed just a collection of functions
(the methods are all static).
It's meant to behave in a way which is similar to the command line, for
    
Notes: consider moving to a more typical usage (instantiate, then use method)
to make it more configurable (ie set the tomb executable path).
'''

import os
import subprocess

class Tomb(object):
    '''
    This is just a collection of static methods, so you should NOT instantiate

    The methods are meant to resemble the command line interface as much as
    possible

    There is no support to things like threading, multiprocessing, whatever.
    If you want to interact asynchronously with tomb, just do it in a separate
    layer.
    '''
    #TODO: support setting a "pipe" to pass out/err on
    def _check_exec_path(self):
        '''Checks, using which, if tomb is available.
        Returns None on error, the path on success.
        '''
        try:
            path=subprocess.check_output(['which', 'tomb'])
        except subprocess.CalledProcessError:
            return None
        return path

    @staticmethod
    def create(tombpath,tombsize,keypath):
        '''If keypath is None, it will be created adjacent to the tomb.
        This is unsafe, and you should NOT do it.

        Note that this will invoke pinentry
        '''
        args = [tombpath, '-s', tombsize]
        if keypath is not None:
            args += ['-k', keypath]
        try:
            subprocess.check_call(['tomb', 'create'] + args)
        except subprocess.CalledProcessError:
            return False
        return True

    @staticmethod
    def open(tombpath,keypath=None):
        raise NotImplementedError


if __name__ == '__main__':
    #Debug stuff. Also useful for an example
    print Tomb.create('/tmp/a.tomb', '10', '/tmp/akey')
