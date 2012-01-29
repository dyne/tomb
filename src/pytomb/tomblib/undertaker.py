import subprocess
from tempfile import NamedTemporaryFile

import parser

class Undertaker(object):
    '''
    This is similar to Tomb class, and provides a wrapper on undertaker.

    TODO:
    * methods for automagical scan
    * output parsing, giving meaningful output

    Due to the non-interactive nature of undertaker, it's simpler than Tomb
    '''
    undertakerexec = 'undertaker'
    @classmethod
    def check(cls, paths):
        '''Will check if there are keys available there, as in --path

        paths can be a string (one address), or a list of
        '''
        #TODO: more solid check: something like
        if type(paths) is not str:
            out = []
            for p in paths:
                try:
                    res = cls.check(p)
                except:
                    continue
                else:
                    if res:
                        out.extend(res)
            return out

        buf = NamedTemporaryFile()
        try:
            subprocess.check_call([cls.undertakerexec, paths, '--batch',
                '--path'], stderr=buf)
        except subprocess.CalledProcessError as exc:
            return False

        out = []
        buf.seek(0)
        for line in buf:
            ret = parser.parse_line(line)
            if ret and ret['type'] == 'found':
                out.append(ret['content'])
        return out


    @classmethod
    def get(cls, paths):
        '''
        Similar to check, but truly get the key content.
        If paths is iterable, stop at the first successful path
        '''
        if type(paths) is not str:
            for p in paths:
                try:
                    res = cls.get(p)
                except:
                    continue
                else:
                    if res:
                        return res
        buf = NamedTemporaryFile()
        try:
            subprocess.check_call([cls.undertakerexec, paths, '--batch'],
                    stdout=buf)
        except subprocess.CalledProcessError:
            return False
        buf.seek(0)
        return buf.read()


if __name__ == '__main__':
    Undertaker.undertakerexec = '/home/davide/coding/projects/tomb/src/undertaker'
    print Undertaker.get('near:///home/davide/Desktop/testing.tomb')
