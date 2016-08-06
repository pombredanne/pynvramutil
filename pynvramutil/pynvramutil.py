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
            fileobj (__iter__)): obj to read str lines from
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


class OrderedDefaultDict(collections.OrderedDict):
    def __init__(self, default_factory=None, *a, **kw):
        collections.OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __missing__(self, key):
        self[key] = value = self.default_factory()
        return value


def compare_nvramdump(*args):
    """

    Arguments:
        args (tuple): two or more dumps to layer and compare

    Returns:
        OrderedDefaultDict: comparison dict


    {
        "dumps": [nd1, nd2],
        "data": {
            "key1": {
                "values": {
                    "dump1"
                }
        }
    }
    """

    data = OrderedDefaultDict(default_factory=OrderedDefaultDict)
    data['dumps'] = list(args)
    for dump in data['dumps']:
        for key in dump:
            attrs = data['data'][key].setdefault('dumpswiththisattr', [])
            attrs.append(dump)
            values = data[key].setdefault('sdfsdf', [])
            values

    # sorted_keys_odict = collections.OrderedDict.fromkeys(
    #     sorted(itertools.chain(d1.keys(), d2.keys())))


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


import codecs
import types
import unittest

import collections
import json


class Test_nvramshowdiff(unittest.TestCase):

    def setUp(self):
        self.conf = collections.OrderedDict()
        self.conf['file_path'] = './wzr1750dhp-nvram_settings.2.txt'

    def test_read_nvram_tuples(self):
        file_path = self.conf['file_path']
        with codecs.open(file_path, 'r', 'utf8') as f:
            nvram_kviter = NvramDump.read_nvram_tuples(f)
            self.assertTrue(hasattr(nvram_kviter, '__iter__'))
            self.assertTrue(isinstance(nvram_kviter, types.GeneratorType))
            nvram_kvlist = sorted(nvram_kviter, key=lambda x: x[0])
            nvram_dict = collections.OrderedDict(nvram_kvlist)
            self.assertGreater(len(nvram_dict), 10)
            json_output = json.dumps(nvram_dict, indent=2)
            print(json_output)
            self.assertGreater(len(json_output), 10)
        #raise Exception()  # force debug print

    def test_Nvram(self):
        file_path = self.conf['file_path']
        with codecs.open(file_path, 'r', 'utf8') as f:
            nvramdump = NvramDump(f)
            self.assertTrue(nvramdump.data)
            print(('nvramdump.data', nvramdump.data))

            json_output = nvramdump.to_json(indent=2)
            self.assertGreater(len(json_output), 10)
            print(('nvramdump.to_json', json_output))

            pretty_output = nvramdump.to_pretty()
            self.assertGreater(len(pretty_output), 10)
            print(('nvramdump.to_pretty','... ->'))
            print(pretty_output)

            str_output = str(nvramdump)
            self.assertGreater(len(str_output), 10)
            print(('nvramdump.to_str','... ->'))
            print(str_output)

            self.assertTrue(str_output == json_output)

        #raise Exception()  # force debug print

    def test_nvramshowdiff(self):
        pass

    def tearDown(self):
        pass


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
