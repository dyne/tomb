'''
Utilities to analyze tomb output
'''
import re

_err_regex = re.compile(r'\[!\][^ ]* +(.+)$')
def parse_line(line):
    '''Analyze a single line.
    Return None if no standard format is detected, a dict otherwise.
    The fields 'type' and 'content' are always in the dict; 'content' may be
    empty
    'type' can be 'error', 'progress'
    '''

    match = _err_regex.search(line)
    if match:
        return { 'type': 'error', 'content': match.group(1) }
    return None


