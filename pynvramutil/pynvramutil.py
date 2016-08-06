#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
pynvramutil
==============

"""

import codecs
import collections
import json
import pprint


class NvramDump(object):

    def __init__(self, fileobj):
        self.data = self.parse_nvram_dump(fileobj)

    @staticmethod
    def read_nvram_tuples(fileobj):
        """
        Args:
            fileobj (file-like object (str iterable)): obj to read str lines from
        Returns:
            tuple: (key, value)
        """
        key, value = None, None
        for l in fileobj:
            l = l.rstrip('\n')
            if '=' in l:
                if value is not None:
                    yield (key, value)
                    key, value = None, None
                key, value = l.split('=', 1)
            else:
                value = (value if value is not None else '') + '\n' + l
        if value is not None:
            yield (key, value)

    @staticmethod
    def build_nvram_dict(nvram_tuples):
        nvram_kvlist = sorted(nvram_tuples, key=lambda x: x[0])
        return collections.OrderedDict(nvram_kvlist)

    @classmethod
    def parse_nvram_dump(cls, fileobj):
        return cls.build_nvram_dict(cls.read_nvram_tuples(fileobj))

    def to_json(self, indent=2):
        return json.dumps(self.data, indent=indent)

    def to_pretty(self):
        """
        .. note:: pprint does not yet support collections.OrderedDict
        """
        return pprint.pformat(self.data)

    def __str__(self):
        return self.to_json()


def nvramshowdiff(show1, show2):
    """mainfunc

    Arguments:
        show1 (str): ...
        show2 (str): ...

    Keyword Arguments:
         (str): ...

    Returns:
        str: ...

    Yields:
        str: ...

    Raises:
        Exception: ...
    """


import sys


def main(argv=None):
    """
    Main function

    Keyword Arguments:
        argv (list): commandline arguments (e.g. sys.argv[1:])
    Returns:
        int:
    """
    import logging
    import optparse

    prs = optparse.OptionParser(
        usage="%prog : args")

    prs.add_option('-v', '--verbose',
                   dest='verbose',
                   action='store_true',)
    prs.add_option('-q', '--quiet',
                   dest='quiet',
                   action='store_true',)
    prs.add_option('-t', '--test',
                   dest='run_tests',
                   action='store_true',)

    argv = list(argv) if argv is not None else []
    (opts, args) = prs.parse_args(args=argv)
    loglevel = logging.INFO
    if opts.verbose:
        loglevel = logging.DEBUG
    elif opts.quiet:
        loglevel = logging.ERROR
    logging.basicConfig(level=loglevel)
    log = logging.getLogger()
    log.debug('argv: %r', argv)
    log.debug('opts: %r', opts)
    log.debug('args: %r', args)

    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        return unittest.main()

    EX_OK = 0
    output = nvramshowdiff(*args[:1])
    return EX_OK


if __name__ == "__main__":
    import sys
    sys.exit(main(argv=sys.argv[1:]))
