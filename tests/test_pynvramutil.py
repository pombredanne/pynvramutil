#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pynvramutil
----------------------------------

Tests for `pynvramutil` module.
"""


import codecs
import collections
import os.path
import json
import types
import unittest

import pynvramutil
pynvramutil


class Test_pynvramutil(unittest.TestCase):

    def setUp(self):
        self.conf = collections.OrderedDict()
        self.conf['data_path'] = (
            os.path.normpath(os.path.join(
                os.path.dirname(__file__),
                '..', 'data', '.local',)))

        self.conf['file_path'] = (
            os.path.join(
                self.conf['data_path'],
                'wzr1750dhp-nvram_settings.2.txt'
            ))

    def test_read_nvram_tuples(self):
        from pynvramutil.pynvramutil import NvramDump
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
        # raise Exception()  # force debug print

    def test_Nvram(self):
        from pynvramutil.pynvramutil import NvramDump
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
            print(('nvramdump.to_pretty', '... ->'))
            print(pretty_output)

            str_output = str(nvramdump)
            self.assertGreater(len(str_output), 10)
            print(('nvramdump.to_str', '... ->'))
            print(str_output)

            self.assertTrue(str_output == json_output)

        # raise Exception()  # force debug print

    def test_nvramshowdiff(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
