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

# Oddly the Pypy Fedora ships is broken and doesn't look in site-packages?
# Requests seems to work fine under pypy, anyway.
if sys.subversion[0] == "PyPy":
    sys.path.append("/usr/lib/python2.7/site-packages")
import requests


__version__ = '0.0.1'

URI = 'http://adventofcode.com/{year}/day/{day}/input'
URI_REFER = 'http://adventofcode.com/{year}/day/{day}'
URI_SUBMIT = 'http://adventofcode.com/{year}/day/{day}/answer'
MEMO_FNAME = "input.txt"
MODULE_PATH = os.path.dirname(__file__)
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


class AocdError(Exception):
    pass


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_session():
    return open(MODULE_PATH + "/session.id").read().strip()


class Data(object):
    def __init__(self, year, day, session=None):
        self.year = year
        self.day = day
        self.session = session
        if session is None:
            self.session = get_session()

        self.memo = None
        # The assumption here is I use a separate directory per day.  The input gets
        # dumped in input.txt in that day's directory.
        try:
            with open(MEMO_FNAME) as f:
                self.memo = f.read()
        except (OSError, IOError) as err:
            if err.errno != errno.ENOENT:
                raise


    def dump_memo(self):
        with open(MEMO_FNAME, 'w') as f:
            f.write(self.memo)
            f.flush()


    def get_data(self):
        """
        Get data for day (1-25) and year (> 2015)
        User's session cookie is needed (puzzle inputs differ by user)
        """

        uri = URI.format(year=self.year, day=self.day)

        if self.memo is None:
            response = requests.get(uri,
                cookies={'session': self.session},
                headers={'User-Agent': USER_AGENT},
            )
            if response.status_code != 200:
                if response.status_code == 404:
                    eprint("404:", response.content)
                    raise AocdError("Puzzle isn't published yet")
                else:
                    eprint(response.status_code)
                    eprint(response.content)
                    raise AocdError('Unexpected response')
            self.memo = response.text
            self.dump_memo()

        return self.memo.strip()


    def solve(self, part, answer):
        """
        part is 1 or 2

        answer is a string
        """
        uri = URI_SUBMIT.format(year=self.year, day=self.day)
        urir = URI_REFER.format(year=self.year, day=self.day)
        response = requests.post(uri,
            data = {'level': part, 'answer': answer},
            cookies={'session': self.session},
            headers={'User-Agent': USER_AGENT, 'Referer': urir},
        )

        if response.status_code != 200:
            eprint("Submission status", response.status_code)
            eprint(response.content)
            raise AocdError('Unexpected response')

        content = response.content
        if "That's the right answer!" in content:
            print("Correct answer")
        elif "That's not the right answer" in content:
            print("Wrong answer: your answer is", content.split("your answer is ")[1].split(".", 1)[0])
        else:
            print("Unexpected response:")
            print(content)

