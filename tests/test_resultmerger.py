import unittest
import os
import pabot.result_merger as result_merger
from robot.result.visitor import ResultVisitor

from test_base import TestBase


class ResultStats(ResultVisitor):
    def __init__(self):
        self.suites = []
        self.tests = []

    def end_test(self, test):
        self.tests.append(test.longname)

    def end_suite(self, suite):
        self.suites.append(suite.longname)


class ResultMergerTests(TestBase):

    def setUp(self):
        super(ResultMergerTests, self).setUp()

    def test_test_level_run_merge(self):
        result = result_merger.merge(
            [
                os.path.join(self.tests_outputs_dir, "first.xml"),
                os.path.join(self.tests_outputs_dir, "second.xml"),
                os.path.join(self.tests_outputs_dir, "third.xml"),
            ],
            {},
            "root",
            [],
        )
        visitor = ResultStats()
        result.visit(visitor)
        self.assertEqual(["Tmp.Tests", "Tmp"], visitor.suites)
        self.assertEqual(
            ["Tmp.Tests.First", "Tmp.Tests.Second", "Tmp.Tests.Third"], visitor.tests
        )

    def test_suite_level_run_merge(self):
        result = result_merger.merge(
            [os.path.join(self.tests_outputs_dir, "tests.xml"), os.path.join(self.tests_outputs_dir, "tests2.xml")], {}, "root", []
        )
        visitor = ResultStats()
        result.visit(visitor)
        self.assertEqual(
            [
                "Tmp.Tests.First",
                "Tmp.Tests.Second",
                "Tmp.Tests.Third",
                "Tmp.Tests2.First 2",
                "Tmp.Tests2.Second 2",
                "Tmp.Tests2.Third 2",
            ],
            visitor.tests,
        )
        self.assertEqual(["Tmp.Tests", "Tmp.Tests2", "Tmp"], visitor.suites)

    def test_prefixing(self):
        self.assertEqual(
            result_merger.prefix(os.path.join("foo", "bar", "zoo", "ba2r.xml")), "zoo"
        )
        self.assertEqual(
            result_merger.prefix(os.path.join("/zoo", "baa", "floo.txt")), "baa"
        )
        self.assertEqual(result_merger.prefix(os.path.join("koo", "foo.bar")), "koo")
        self.assertEqual(result_merger.prefix("hui.txt"), "")


if __name__ == "__main__":
    unittest.main()
