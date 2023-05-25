import unittest

import pabot.pabot
from unittest.mock import MagicMock
from pabot import arguments


class SameFilenamesTests(unittest.TestCase):

    def test_hello_world(self):
        args = ["tests/fixtures/duplicate_name_check/01_folder/test.robot",
                "tests/fixtures/suite_special.robot",
                #"tests/fixtures/duplicate_name_check/02_folder/test.robot",
                ]
        #pabot.pabot._write_with_id = MagicMock()
        pabot.pabot.main_program(args)
        #print(pabot.pabot._write_with_id.call_count)
