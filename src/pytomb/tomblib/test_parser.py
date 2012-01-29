from tomblib.parser import *

class TestWrong:
    def test_short(self):
        '''short format is not supported anymore'''
        assert parse_line('[!] foo') is None
    def test_colors(self):
        '''parsing while using colors should fail'''
        parse = parse_line('\033[32mundertaker [W] url protocol not recognized: nonscheme')
        assert parse is None
    def test_no_spaces_in_programname(self):
        parse = parse_line('tomb open [W] url protocol not recognized: nonscheme')
        assert parse is None

class TestFound:
    def test_simple(self):
        parse = parse_line('[m][found] scheme:///and/path')
        assert parse is not None
        assert parse['type'] == 'found'
        assert parse['content'] == 'scheme:///and/path'
        assert 'scheme' in parse
        assert parse['scheme'] == 'scheme'
        assert 'path' in parse
        assert parse['path'] == '/and/path'

class TestGeneric:
    def test_simple(self):
        parse = parse_line('undertaker [W] url protocol not recognized: nonscheme')
        assert parse is not None
        assert parse['type'] == 'warning'
        assert parse['content'] == 'url protocol not recognized: nonscheme'

    def test_debug(self):
        parse = parse_line('undertaker [D] url protocol not recognized: nonscheme')
        assert parse is not None
        assert parse['type'] == 'debug'
        assert parse['content'] == 'url protocol not recognized: nonscheme'

    def test_success(self):
        parse = parse_line('undertaker (*) url protocol not recognized: nonscheme')
        assert parse is not None
        assert parse['type'] == 'success'
        assert parse['content'] == 'url protocol not recognized: nonscheme'

    def test_dash(self):
        parse = parse_line('tomb-open [W] url protocol not recognized: nonscheme')
        assert parse is not None
        assert parse['type'] == 'warning'
        assert parse['content'] == 'url protocol not recognized: nonscheme'



