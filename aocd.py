# Forked from https://github.com/wimglenn/advent-of-code-data , stripped down
# for my use.
#
# MIT License
# 
# Copyright (c) 2016 wim glenn
#               2017 Conrad Meyer <cemeyer+github@uw.edu>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import errno
import os
import sys

import requests


__version__ = '0.0.1'

URI = 'http://adventofcode.com/{year}/day/{day}/input'
MEMO_FNAME = "input.txt"
MODULE_PATH = os.path.dirname(__file__)
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


class AocdError(Exception):
    pass


# The assumption here is I use a separate directory per day.  The input gets
# dumped in input.txt in that day's directory.
memo = None
try:
    with open(MEMO_FNAME) as _f:
        memo = _f.read()
except (OSError, IOError) as err:
    if err.errno != errno.ENOENT:
        raise

def dump_memo():
    with open(MEMO_FNAME, 'w') as f:
        f.write(memo)
        f.flush()


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_data(year, day, session=None):
    """
    Get data for day (1-25) and year (> 2015)
    User's session cookie is needed (puzzle inputs differ by user)
    """
    global memo

    if session is None:
        session = open(MODULE_PATH + "/session.id").read().strip()

    uri = URI.format(year=year, day=day)

    if memo is None:
        response = requests.get(uri,
            cookies={'session': session}, headers={'User-Agent': USER_AGENT},
        )
        if response.status_code != 200:
            eprint(response.status_code)
            eprint(response.content)
            raise AocdError('Unexpected response')
        memo = response.text
        dump_memo()

    return memo.strip()
