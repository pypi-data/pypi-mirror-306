import unittest

from sensiml.tests.basetest import BaseTest
from sensiml.functions import Functions


class FunctionTestCase(BaseTest):
    """Unit tests for Function and Functions."""

    def setUp(self):
        self.connection = self._connection
        self.functions = Functions(self.connection)

    def test_function_get(self):
        function = self.functions.get_function_by_name("Mean")
        self.assertGreater(len(function.input_contract), 0)

        # Change locally
        function.name = "Not Mean"
        function.input_contract = ""

        # Refresh
        function.refresh()
        self.assertEqual("Mean", function.name)
        self.assertGreater(len(function.input_contract), 0)

    def test_functions_get(self):
        # Reconstitute functions in a list
        my_function_list = self.functions.get_functions()
        self.assertGreaterEqual(len(my_function_list), 2)
        f_names = [f.name for f in my_function_list]
        self.assertTrue("Mean" in f_names)
        self.assertTrue("Normalize" in f_names)

    def test_function_printstring(self):
        retrieved = self.functions.get_function_by_name("Mean")
        printstring = retrieved.__str__()
        self.assertTrue("TYPE: Feature Generator" in printstring)
        self.assertTrue("SUBTYPE: Statistical" in printstring)
        self.assertTrue("DESCRIPTION:" in printstring)
        # Costs are disabled in print string
        # self.assertTrue('CodeSize: 10' in printstring)
        # self.assertTrue('NumFeatures: 100' in printstring)


if __name__ == "__main__":
    unittest.main()
