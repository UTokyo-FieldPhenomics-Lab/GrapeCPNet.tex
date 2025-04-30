#!/usr/bin/python
"""
    pymergechanges: Merge commits made with changes package into text
    Copyright (C) 2018  Y. Cui

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

pymergechanges: Merge commits made with changes package into text

Requires Python version 3; Tested on Python 3.6.6

Supported commands: added, deleted, replaced, highlight
Usage: python pyMergeChanges.py [-arh] <Input File> <Output File>
<Output File> will be overwritten and must be different than <Input File>.
Options:
    -a: accept all added, deleted and replaced
    -r: reject all added, deleted and replaced
    -h: remove all highlights
If no option is given, runs interactively.

Created on Wed Dec  5 20:28:40 2018
Revised on Tue Aug 27 17:51:58 2019

"""

import sys
import re
import codecs

def parse_param(parstr):
    if all(p in parstr for p in ('a', 'r')):
        print('You cannot accept and reject at the same time.')
        sys.exit(1)
    parout = ''
    for par in parstr[1:]:
        if par == 'a':
            print('Accepting all added, deleted and replaced')
            parout += 'a'
        elif par == 'r':
            print('Rejecting all added, deleted and replaced')
            parout += 'r'
        elif par == 'h':
            print('Removing all highlights.')
            parout += 'h'
        else:
            print('Unknown parameter: ' + par)
            sys.exit(1)
    if not parout:
        parout = 'i'
    return parout

def ask1(): # accept, reject, keep, break
    if PARAMS == 'i':
        while True:
            ans = input('[a]ccept or [r]eject or [k]eep or [b]reak ? ').lower()
            if ans == 'a':
                print('Accepted.')
                break
            elif ans == 'r':
                print('Rejected.')
                break
            elif ans == 'k':
                print('Kept.')
                break
            elif ans == 'b':
                print('Alright.')
                break
    elif any(p == 'a' for p in PARAMS):
        print('Accepted.')
        ans = 'a'
    elif any(p == 'r' for p in PARAMS):
        print('Rejected.')
        ans = 'r'
    else:
        ans = 'k'
    return ans

def ask2(): # remove, keep, break
    if PARAMS == 'i':
        while True:
            ans = input('[r]emove or [k]eep or [b]reak ? ').lower()
            if ans == 'r':
                print('Removed.')
                break
            elif ans == 'k':
                print('Kept.')
                break
            elif ans == 'b':
                print('Alright.')
                break
        return ans
    elif any(p == 'h' for p in PARAMS):
        print('Removed.')
        ans = 'r'
    else:
        print('Kept.')
        ans = 'k'
    return ans

def trim_space(line, pos): # trim two consecutive white spaces
    if line[pos-1:pos+1] == '  ':
        line = line[:pos] + line[pos+1:]
    return line

# BEGIN OF SCRIPT

if len(sys.argv) not in [3, 4]:
    print(__doc__)
    sys.exit(1)

# parse input parameters
if len(sys.argv) == 3:
    print('Running in interactive mode. ')
    INPUTFILE, OUTPUTFILE = sys.argv[1:]
    PARAMS = "i"
if len(sys.argv) == 4:
    PARAMLIST, INPUTFILE, OUTPUTFILE = sys.argv[1:]
    PARAMS = parse_param(PARAMLIST)

if INPUTFILE == OUTPUTFILE:
    print('Input File and Output File must be different.')
    sys.exit(1)

RE_ADDED = re.compile(r'(\\added)(\[[^\]]*\])?\{(([^\}]?(\{[^\}]*\})?)*)\}')
RE_DELETED = re.compile(r'(\\deleted)(\[[^\]]*\])?\{(([^\}]?(\{[^\}]*\})?)*)\}')
RE_REPLACED = re.compile(r'(\\replaced)(\[[^\]]*\])?\{(([^\}]?(\{[^\}]*\})?)*)\}\{(([^\}]?(\{[^\}]*\})?)*)\}')
RE_HIGHLIGHT = re.compile(r'(\\highlight)(\[[^\]]*\])?\{(([^\}]?(\{[^\}]*\})?)*)\}')
RE_COMMENT = re.compile(r'(\\comment)(\[[^\]]*\])?\{(([^\}]?(\{[^\}]*\})?)*)\}')

codecs.open(OUTPUTFILE, mode='w', encoding='utf8').close()
with codecs.open(INPUTFILE, mode='r', encoding='utf8') as fin, \
codecs.open(OUTPUTFILE, mode='a', encoding='utf8') as fout:
    LINE_COUNT = 0
    FLAG_FAST_BREAK = False # if you want to halt merging for some reason
    for linein in fin:
        if FLAG_FAST_BREAK:
            fout.write(linein)
            continue
        LINE_COUNT += 1
        lineout = linein
        matchAdded = RE_ADDED.search(lineout)
        matchDeleted = RE_DELETED.search(lineout)
        matchReplaced = RE_REPLACED.search(lineout)
        matchHighlight = RE_HIGHLIGHT.search(lineout)
        matchComment = RE_COMMENT.search(lineout)
        flagHasCommit = matchAdded or matchDeleted or matchReplaced or matchHighlight or matchComment
        if flagHasCommit:
            print('\n******** In Line %i :\n %s' % (LINE_COUNT, lineout))
            next_pos = 0
            while matchAdded:
                if FLAG_FAST_BREAK:
                    break
                print('\n** add commit ** \n' + matchAdded.group())
                answer = ask1()
                if answer == 'a':
                    lineout = (lineout[:matchAdded.start(0)]
                               + matchAdded.group(3) + lineout[matchAdded.end(0):])
                    lineout = trim_space(lineout, matchAdded.start(0)
                                         + len(matchAdded.group(3)))
                    lineout = trim_space(lineout, matchAdded.start(0))
                elif answer == 'r':
                    lineout = (lineout[:matchAdded.start(0)] + lineout[matchAdded.end(0):])
                    lineout = trim_space(lineout, matchAdded.start(0))
                elif answer == 'k':
                    lineout = lineout
                    next_pos = matchAdded.end(0)
                elif answer == 'b':
                    FLAG_FAST_BREAK = True
                    break
                matchAdded = RE_ADDED.search(lineout, next_pos) # redo matching for updated text

            next_pos = 0
            matchDeleted = RE_DELETED.search(lineout, next_pos)  # redo matching for (potentially) updated text
            while matchDeleted:
                if FLAG_FAST_BREAK:
                    break
                print('\n** delete commit ** \n' + matchDeleted.group())
                answer = ask1()
                if answer == 'a':
                    lineout = (lineout[:matchDeleted.start(0)] + lineout[matchDeleted.end(0):])
                    lineout = trim_space(lineout, matchDeleted.start(0))
                elif answer == 'r':
                    lineout = (lineout[:matchDeleted.start(0)] + matchDeleted.group(3)
                               + lineout[matchDeleted.end(0):])
                elif answer == 'k':
                    lineout = lineout
                    next_pos = matchDeleted.end(0)
                elif answer == 'b':
                    FLAG_FAST_BREAK = True
                    break
                matchDeleted = RE_DELETED.search(lineout, next_pos)

            next_pos = 0
            matchReplaced = RE_REPLACED.search(lineout, next_pos)  # redo matching for (potentially) updated text
            while matchReplaced:
                if FLAG_FAST_BREAK:
                    break
                print('\n** replace commit ** \n' + matchReplaced.group())
                answer = ask1()
                if answer == 'a':
                    lineout = (lineout[:matchReplaced.start(0)]
                               + matchReplaced.group(3) + lineout[matchReplaced.end(0):])
                    lineout = trim_space(lineout, matchReplaced.start(0)
                                         + len(matchReplaced.group(3)))
                    lineout = trim_space(lineout, matchReplaced.start(0))
                elif answer == 'r':
                    lineout = (lineout[:matchReplaced.start(0)]
                               + matchReplaced.group(6) + lineout[matchReplaced.end(0):])
                    lineout = trim_space(lineout, matchReplaced.start(0)
                                         + len(matchReplaced.group(6)))
                    lineout = trim_space(lineout, matchReplaced.start(0))
                elif answer == 'k':
                    lineout = lineout
                    next_pos = matchReplaced.end(0)
                elif answer == 'b':
                    FLAG_FAST_BREAK = True
                    break
                matchReplaced = RE_REPLACED.search(lineout, next_pos)

            next_pos = 0
            matchHighlight = RE_HIGHLIGHT.search(lineout, next_pos)  # redo matching for (potentially) updated text
            while matchHighlight:
                if FLAG_FAST_BREAK:
                    break
                print('\n** highlight commit ** \n' + matchHighlight.group())
                answer = ask2()
                if answer == 'r':
                    lineout = (lineout[:matchHighlight.start(0)]
                               + matchHighlight.group(3) + lineout[matchHighlight.end(0):])
                    lineout = trim_space(lineout, matchHighlight.start(0)
                                         + len(matchHighlight.group(3)))
                    lineout = trim_space(lineout, matchHighlight.start(0))
                elif answer == 'k':
                    lineout = lineout
                    next_pos = matchHighlight.end(0)
                elif answer == 'b':
                    FLAG_FAST_BREAK = True
                    break
                matchHighlight = RE_HIGHLIGHT.search(lineout, next_pos)

            next_pos = 0
            matchComment = RE_COMMENT.search(lineout, next_pos)  # redo matching for (potentially) updated text
            while matchComment:
                if FLAG_FAST_BREAK:
                    break
                print('\n** comment commit ** \n' + matchComment.group())
                answer = ask2()
                if answer == 'r':
                    lineout = (lineout[:matchComment.start(0)] + lineout[matchComment.end(0):])
                    lineout = trim_space(lineout, matchComment.start(0))
                elif answer == 'k':
                    lineout = lineout
                    next_pos = matchComment.end(0)
                elif answer == 'b':
                    FLAG_FAST_BREAK = True
                    break
                matchComment = RE_COMMENT.search(lineout, next_pos)

            if lineout.isspace():
                print('\nResult is empty line and not stored.')
            else:
                print('\nResult: \n' + lineout + '\n')
                fout.write(lineout)

        else:
            fout.write(linein)
#
# END OF SCRIPT
