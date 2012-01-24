'''
Module structure:

this contain a class, which is indeed just a collection of functions
(the methods are all static).
It's meant to behave in a way which is similar to the command line, for
    
Notes: consider moving to a more typical usage (instantiate, then use method)
to make it more configurable (ie set the tomb executable path).
'''

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
    tombexec = 'tomb'
    def _check_exec_path(self):
        '''Checks, using which, if tomb is available.
        Returns None on error, the path on success.
        '''
        try:
            path = subprocess.check_output(['which', 'tomb'])
        except subprocess.CalledProcessError:
            return None
        return path

    @classmethod
    def check(cls, command, stdout=None, stderr=None, no_color=True, ignore_swap=False):
        args = [command]
        if no_color:
            args += ['--no-color']
        if ignore_swap:
            args += ['--ignore-swap']
        try:
            subprocess.check_call([cls.tombexec, 'check'] + args, stdout=stdout, stderr=stderr)
        except subprocess.CalledProcessError:
            return False
        return True

    @classmethod
    def create(cls, tombpath, tombsize,keypath, stdout=None, stderr=None,
            no_color=True, ignore_swap=False):
        '''If keypath is None, it will be created adjacent to the tomb.
        This is unsafe, and you should NOT do it.

        Note that this will invoke pinentry

        no_color is supported as an option for short-lived retrocompatibility:
            it will be removed as soon as no-color will be integrated
        '''
        args = [tombpath, '-s', tombsize]
        if keypath is not None:
            args += ['-k', keypath]
        if no_color:
            args += ['--no-color']
        if ignore_swap:
            args += ['--ignore-swap']
        try:
            subprocess.check_call([cls.tombexec, 'create'] + args, stdout=stdout, stderr=stderr)
        except subprocess.CalledProcessError:
            return False
        return True

    @classmethod
    def open(cls, tombpath,keypath=None, no_color=True, ignore_swap=False):
        args = [tombpath]
        if keypath is not None:
            args += ['-k', keypath]
        if no_color:
            args += ['--no-color']
        if ignore_swap:
            args += ['--ignore-swap']
        try:
            subprocess.check_call([cls.tombexec, 'open'] + args)
        except subprocess.CalledProcessError:
            return False
        return True


if __name__ == '__main__':
    #Debug stuff. Also useful for an example
    print Tomb.create('/tmp/a.tomb', '10', '/tmp/akey')
