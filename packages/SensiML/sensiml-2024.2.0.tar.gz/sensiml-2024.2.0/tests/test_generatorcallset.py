import unittest

from sensiml.tests.basetest import BaseTest
from sensiml.functions import Functions
from sensiml.method_calls.generatorcallset import GeneratorCallSet


class GeneratorCallSetTestCase(BaseTest):
    """Unit tests for GeneratorCallSet."""

    def setUp(self):
        self.connection = self._connection
        self.functions = Functions(self.connection)

    def test_generatorcallset(self):
        gcs = GeneratorCallSet()
        gcs.name = "GeneratorCallsSet"
        gcs.outputs = ["Col01", "Col02"]

        stat = self.functions.get_function_by_name("Trim")
        stat_call = self.functions.create_feature_generator_call(stat)
        gcs.add_generator_call(stat_call)

        spec = self.functions.get_function_by_name("Trim")
        spec_call = self.functions.create_feature_generator_call(spec)
        gcs.add_generator_call(spec_call)

        d = gcs._to_dict()
        self.assertEqual("Trim", d["set"][0]["function_name"])

    def test_generatorcallset_with_subtype(self):
        gcs = GeneratorCallSet()
        gcs.name = "GeneratorCallsSet"
        gcs.outputs = ["Col01", "Col02"]

        temp_call = self.functions.create_generator_subtype_call("Statistical")
        gcs.add_generator_call(temp_call)

        d = gcs._to_dict()
        self.assertEqual("Statistical", d["set"][0]["subtype"])

    def test_generatorcallset_without_name(self):
        """A default name is set if no name is used in the constructor"""
        gcs = self.functions.create_generator_call_set()
        self.assertEquals("GeneratorCallSet", gcs.name)


if __name__ == "__main__":
    unittest.main()
