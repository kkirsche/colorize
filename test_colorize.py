#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from subprocess import Popen, PIPE

from colorize import Colors

class TestColorize(unittest.TestCase):

    def setUp(self):
        self.exe = "./colorize.py"
        self.input_lines = '\n'.join(["aaa bbb ccc ddd", "AAA BBB CCC DDD", "000 111 222 333"])
        self.proc = None

    def tearDown(self):
        self.proc.terminate()
        self.proc.wait()

    def check(self, cmdline, expected):
        self.proc = Popen(cmdline, stdin=PIPE, stdout=PIPE, universal_newlines=True)
        self.proc.stdin.write(self.input_lines)
        self.proc.stdin.close()
        self.assertEqual(self.proc.stdout.read(), expected)

    def test_default_action(self):
        expected = "".join([
            Colors.blue("aaa ") + Colors.cyan("bbb ") + Colors.green("ccc ") + Colors.grey("ddd\n"),
            Colors.blue("AAA ") + Colors.cyan("BBB ") + Colors.green("CCC ") + Colors.grey("DDD\n"),
            Colors.blue("000 ") + Colors.cyan("111 ") + Colors.green("222 ") + Colors.grey("333")
        ])
        self.check([self.exe], expected)

    def test_max_colors(self):
        expected = "".join([
            Colors.blue("aaa ") + Colors.cyan("bbb ccc ddd\n"),
            Colors.blue("AAA ") + Colors.cyan("BBB CCC DDD\n"),
            Colors.blue("000 ") + Colors.cyan("111 222 333")
        ])
        self.check([self.exe, "1"], expected)

    def test_custom_column_colors(self):
        expected = "".join([
            Colors.red("aaa ") + Colors.green("bbb ") + Colors.blue("ccc ") + Colors.red("ddd\n"),
            Colors.red("AAA ") + Colors.green("BBB ") + Colors.blue("CCC ") + Colors.red("DDD\n"),
            Colors.red("000 ") + Colors.green("111 ") + Colors.blue("222 ") + Colors.red("333")
        ])
        self.check([self.exe, "-c", "red,green,blue"], expected)

    def test_custom_column_colors_and_max_colors(self):
        expected = "".join([
            Colors.red("aaa ") + Colors.green("bbb ccc ddd\n"),
            Colors.red("AAA ") + Colors.green("BBB CCC DDD\n"),
            Colors.red("000 ") + Colors.green("111 222 333")
        ])
        self.check([self.exe, "-c", "red,green", "1"], expected)

    def test_alternate_mode(self):
        expected = "".join([
            Colors.white("aaa bbb ccc ddd\n"),
            Colors.grey("AAA BBB CCC DDD\n"),
            Colors.white("000 111 222 333")
        ])
        self.check([self.exe, "-a"], expected)

    def test_alternate_mode_custom_colors(self):
        expected = "".join([
            Colors.red("aaa bbb ccc ddd\n"),
            Colors.green("AAA BBB CCC DDD\n"),
            Colors.red("000 111 222 333")
        ])
        self.check([self.exe, "-a", "red,green"], expected)


if __name__ == '__main__':
    unittest.main()
