import re
import sys
import unittest
from contextlib import contextmanager
from io import StringIO

from bdop_cli.commands.version import VersionCommand


@contextmanager
def captured_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


class VersionCommandTest(unittest.TestCase):
    def test_output(self):
        with captured_output() as stdout:
            VersionCommand(VersionCommand.Args()).execute()
        assert re.match(r"^bdop-cli version (?:\d+\.\d+\.\d+|UNRELEASED)\n$", stdout.getvalue())
