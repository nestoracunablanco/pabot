import os
import unittest


class TestBase(unittest.TestCase):

    def setUp(self):
        self.tests_dir = os.path.dirname(os.path.abspath(__file__))
        self.tests_outputs_dir = os.path.join(self.tests_dir, "outputs")
        self.tests_data_dir = os.path.join(self.tests_dir, "data")
        self.tests_fixtures_dir = os.path.join(self.tests_data_dir, "fixtures")
        self.output_xml = os.path.join(self.tests_data_dir, "output.xml")
