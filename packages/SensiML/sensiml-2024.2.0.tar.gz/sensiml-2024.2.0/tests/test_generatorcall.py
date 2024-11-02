import unittest

from sensiml.tests.basetest import BaseTest
from sensiml.functions import Functions


class GeneratorCallTestCase(BaseTest):
    """Unit tests for FunctionCall."""

    def setUp(self):
        self.connection = self._connection
        self.functions = Functions(self.connection)

    def test_generatorcall_create_todict(self):
        stat = self.functions.get_function_by_name("Trim")
        stat_call = self.functions.create_feature_generator_call(stat)
        d = stat_call._to_dict()
        self.assertEqual("Trim", d["function_name"])


if __name__ == "__main__":
    unittest.main()
