import os
import shutil
import tempfile
import unittest
import random
from pabot import pabot, arguments
import pabot.execution_items as execution_items

s = execution_items.SuiteItem
t = execution_items.TestItem


class ParallelExecutionTests(unittest.TestCase):

    def setUp(self):
        self._options, self._datasources, self._pabot_args, _ = arguments.parse_args(
            [
                "--pabotlib",
                "--verbose",
                "--argumentfile1",
                "tests/passingarg.txt",
                "--argumentfile2",
                "tests/failingarg.txt",
                "--resourcefile",
                "tests/valueset.dat",
                "tests/fixtures",
            ]
        )
        self._outs_dir = pabot._output_dir(self._options)
        self._all_suites = [
            "Fixtures.Suite One",
            "Fixtures.Suite Second",
            "Fixtures.Suite Special",
            "Fixtures.Suite With Valueset Tags",
            "Fixtures.Test Copy Artifacts.Suite 1",
            "Fixtures.Test Copy Artifacts.Suite 2",
        ]
        self._all_with_suites = ["--suite " + s for s in self._all_suites]
        self._all_tests = [
            "Fixtures.Suite One.1.1 Test Case One",
            "Fixtures.Suite One.1.2 Test Case Two",
            "Fixtures.Suite One.1.3 Test Value Set",
            "Fixtures.Suite One.1.4 Testing arg file",
            "Fixtures.Suite Second.Testing Case One of Second with Scändic Chör",
            "Fixtures.Suite Second.Testing Case One and a half Of Second",
            "Fixtures.Suite Second.Testing Case Two of Second",
            "Fixtures.Suite Second.Testing 1",
            "Fixtures.Suite Second.Testing 2",
            "Fixtures.Suite Special.Passing test Case",
            "Fixtures.Suite With Valueset Tags.Laser value set",
            "Fixtures.Suite With Valueset Tags.Tachyon value set",
            "Fixtures.Suite With Valueset Tags.Common value set",
            "Fixtures.Suite With Valueset Tags.None existing",
            "Fixtures.Suite With Valueset Tags.Add value to set",
            "Fixtures.Test Copy Artifacts.Suite 1.Links to screenshot directly in output_dir",
            "Fixtures.Test Copy Artifacts.Suite 1.Links to screenshots in subfolder",
            "Fixtures.Test Copy Artifacts.Suite 1.Links to other file in subfolder",
            "Fixtures.Test Copy Artifacts.Suite 2.Links to screenshot directly in output_dir",
            "Fixtures.Test Copy Artifacts.Suite 2.Links to screenshots in subfolder",
            "Fixtures.Test Copy Artifacts.Suite 2.Links to other file in subfolder",
        ]
        self._all_with_tests = ["--test " + _t for _t in self._all_tests]

    def test_parallel_execution(self):
        dtemp = tempfile.mkdtemp()
        outs_dir = os.path.join(dtemp, "pabot_results")
        self._options["outputdir"] = dtemp
        self._pabot_args["pabotlibport"] = 4000 + random.randint(0, 1000)
        self._pabot_args["testlevelsplit"] = False
        lib_process = pabot._start_remote_library(self._pabot_args)
        pabot._initialize_queue_index()
        try:
            suite_names = [s(_s) for _s in self._all_suites]
            items = [
                pabot.QueueItem(
                    self._datasources,
                    outs_dir,
                    self._options,
                    suite,
                    self._pabot_args["command"],
                    self._pabot_args["verbose"],
                    argfile,
                )
                for suite in suite_names
                for argfile in self._pabot_args["argumentfiles"] or [("", None)]
            ]
            pabot._parallel_execute(
                items,
                self._pabot_args["processes"],
                self._datasources,
                outs_dir,
                self._options,
                self._pabot_args,
            )
            result_code = pabot._report_results(
                outs_dir,
                self._pabot_args,
                self._options,
                pabot._now(),
                pabot._get_suite_root_name([suite_names]),
            )
            self.assertEqual(10, result_code)
        finally:
            pabot._stop_remote_library(lib_process)
            shutil.rmtree(dtemp)

    def test_parallel_execution_with_testlevelsplit(self):
        dtemp = tempfile.mkdtemp()
        outs_dir = os.path.join(dtemp, "pabot_results")
        self._options["outputdir"] = dtemp
        self._pabot_args["pabotlibport"] = 4000 + random.randint(0, 1000)
        self._pabot_args["testlevelsplit"] = True
        lib_process = pabot._start_remote_library(self._pabot_args)
        pabot._initialize_queue_index()
        try:
            test_names = [t(_t) for _t in self._all_tests]
            items = [
                pabot.QueueItem(
                    self._datasources,
                    outs_dir,
                    self._options,
                    test,
                    self._pabot_args["command"],
                    self._pabot_args["verbose"],
                    argfile,
                )
                for test in test_names
                for argfile in self._pabot_args["argumentfiles"] or [("", None)]
            ]
            pabot._parallel_execute(
                items,
                self._pabot_args["processes"],
                self._datasources,
                outs_dir,
                self._options,
                self._pabot_args,
            )
            result_code = pabot._report_results(
                outs_dir,
                self._pabot_args,
                self._options,
                pabot._now(),
                pabot._get_suite_root_name([test_names]),
            )
            self.assertEqual(12, result_code)
        finally:
            pabot._stop_remote_library(lib_process)
            shutil.rmtree(dtemp)


if __name__ == '__main__':
    unittest.main()
