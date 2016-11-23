"""
Tests for TGN Tcl wrapper - the default wrapper.

@author yoram@ignissoft.com
"""

import sys
from os import path
import unittest
import logging
from ConfigParser import SafeConfigParser

from trafficgenerator.tgn_tcl import TgnTclWrapper, tcl_list_2_py_list, py_list_to_tcl_list, is_false, is_true

config_file = path.join(path.dirname(__file__), 'TrafficGenerator.ini')


class TclTest(unittest.TestCase):

    def setUp(self):
        config = SafeConfigParser(allow_no_value=True)
        config.read(config_file)

        logger = logging.getLogger('log')
        logger.setLevel(config.get('Logging', 'level'))
        logger.addHandler(logging.FileHandler(config.get('Logging', 'file_name')))
        logger.addHandler(logging.StreamHandler(sys.stdout))

        self.tcl = TgnTclWrapper(logger)

    def tearDown(self):
        pass

    def testList(self):
        """ Test Python->Tcl and Tcl->Python list conversion. """

        py_list = ['a', 'b b']
        tcl_list_length = self.tcl.eval('llength ' + py_list_to_tcl_list(py_list))
        assert(int(tcl_list_length) == 2)

        tcl_list = '{a} {b b}'
        py_list_length = len(tcl_list_2_py_list(tcl_list))
        assert(py_list_length == 2)

    def testTrueFalse(self):
        """ Test Tcl true and false values. """

        for false_stc in ('False', 'false', '0', 'null', 'NONE', 'none', '::ixnet::obj-null'):
            assert(is_false(false_stc))
            assert(not is_true(false_stc))

        for true_str in ('True', 'TRUE', '1'):
            assert(is_true(true_str))
            assert(not is_false(true_str))