# -*- coding:UTF-8 -*-
"""
单测case config parser
"""
import unittest
import configparser

from halring.caseconfig.halring_parser import IniConfigParser


class TestCaseConfigParser(unittest.TestCase):

    def test_windows_os_util_001_file_exists(self):
        parser = IniConfigParser()
        parser_ori = configparser.ConfigParser()

        parser.read('test_case_config_parser.ini')
        parser_ori.read('test_case_config_parser.ini')
        options = parser.options('bitbucket.org')
        options_ori = parser_ori.options('bitbucket.org')
        # options大写
        print(options)
        # optoins原库小写
        print(options_ori)
