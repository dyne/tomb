'''
Utilities to analyze tomb output
'''
import re

#found: [m] followed by some ID (usually "found") inside square brackets, then
#something else, then a space, then the content
_found_regex = re.compile(r'^\[m\]\[([^]]+)\] +(([^:]+)://(.+))$')
#generic: programname, then some identifiers in square (or round) brackets,
#then maybe something else, then a space, then the context
_generic_regex = re.compile(r'^[a-z-]+ [[(]([^]]+)[\])] +(.+)$')
types = {'E': 'error', 'W': 'warning', 'D': 'debug', '*': 'success'}


def parse_line(line):
    '''Analyze a single line.
    Return None if no standard format is detected, a dict otherwise.
    The fields 'type' and 'content' are always in the dict; 'content' may be
    empty
    'type' can be 'error', 'progress'
    '''

    match = _found_regex.match(line)
    if match:
        return {'type': types.get(match.group(1)) or match.group(1),
                'content': match.group(2), 'scheme': match.group(3),
                'path': match.group(4)}
    match = _generic_regex.search(line)
    if match:
        return {'type': types.get(match.group(1)) or match.group(1),
                'content': match.group(2)}

    return None
