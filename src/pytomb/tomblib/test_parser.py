from tomblib.parser import *

class TestWrong:
    def test_wrong_tag(self):
        assert parse_line(' [a] foo') is None
    def test_no_space(self):
        assert parse_line(' [!]foo') is None

class TestError:
    def test_simple(self):
        parse =  parse_line('[!] foo')
        assert parse is not None
        assert parse['type'] == 'error'
        assert parse['content'] == 'foo'
    def test_preceding(self):
        parse =  parse_line(' [!] foo')
        assert parse is not None
        assert parse['type'] == 'error'
        assert parse['content'] == 'foo'
    def test_following(self):
        parse = parse_line('[!]shdad foo')
        assert parse is not None
        assert parse['type'] == 'error'
        assert parse['content'] == 'foo'
    def test_mul_words(self):
        parse = parse_line('[!] shdad foo')
        assert parse is not None
        assert parse['type'] == 'error'
        assert parse['content'] == 'shdad foo'
