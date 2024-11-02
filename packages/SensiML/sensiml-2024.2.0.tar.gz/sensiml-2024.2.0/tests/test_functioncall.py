import unittest

from sensiml.tests.basetest import BaseTest
from sensiml.datamanager.knowledgebuilder import KnowledgeBuilder
from sensiml.functions import Functions


class FunctionCallTestCase(BaseTest):
    """Unit tests for FunctionCall."""

    def setUp(self):
        self.connection = self._connection
        self.kb = KnowledgeBuilder(self.connection)
        self.functions = Functions(self.connection)

        self.project_name = "TestProjectForFunctioncall"
        self.addCleanup(self.project_cleanup)

        self.new_project = self.kb.projects.new_project()
        self.new_project.name = self.project_name
        self.new_project.insert()

    def test_functioncall(self):
        trim = self.functions.get_function_by_name("Trim")
        trim_call = self.functions.create_function_call(trim, "transform")
        trim_call.num_samples = 3840
        trim_call.id_column = "Subject"
        trim_call.outputs = ["temp.trimmed"]
        trim_call.df_or_series = "temp.rawdata"
        d = trim_call._to_dict()
        self.assertEqual("Trim", d["name"])


if __name__ == "__main__":
    unittest.main()
