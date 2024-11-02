import unittest

from sensiml.tests.basetest import BaseTest
from sensiml.datamanager.knowledgebuilder import KnowledgeBuilder
from sensiml.method_calls.querycall import QueryCall


class QueryCallTestCase(BaseTest):
    """Unit tests for QueryCall object."""

    def setUp(self):
        self.connection = self._connection
        self.kb = KnowledgeBuilder(self.connection)
        self.project_name = "TestProjectForQuery"
        self.addCleanup(self.project_cleanup)

        self.new_project = self.kb.projects.new_project()
        self.new_project.name = self.project_name
        self.new_project.insert()
        self.new_query = self.new_project.queries.new_query()
        self.new_query.name = "name"
        self.new_query.columns.add("columns")
        self.new_query.metadata_columns.add("metadata_columns")
        self.new_query.metadata_filter = "metadata_filter"
        self.new_sandbox = self.new_project.sandboxes.new_sandbox()
        self.new_sandbox.name = "name"
        self.new_sandbox.insert()

    def test_querycall_add(self):
        # Do insert
        qcall = QueryCall("query01")
        qcall.query = self.new_query
        qcall.outputs = "temp.data"
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(qcall)
        l = self.new_sandbox.pipeline.to_list()
        q = l[0]["type"]
        self.assertEqual("query", q)


if __name__ == "__main__":
    unittest.main()
