import unittest

from requests.exceptions import HTTPError
from sensiml.tests.basetest import BaseTest
from sensiml.datamanager.knowledgebuilder import KnowledgeBuilder


class SandboxTestCase(BaseTest):
    """Unit tests for sandbox and sandboxes."""

    def setUp(self):
        self.connection = self._connection
        self.kb = KnowledgeBuilder(self.connection)

        # Add cleanup steps
        self.project_name = "TestProjectForSandbox"
        self.project_name_2 = "TestProjectForSandbox2"
        self.addCleanup(self.project_cleanup)
        self.addCleanup(self.project_2_cleanup)

        self.new_project = self.kb.projects.new_project()
        self.new_project.name = self.project_name
        self.new_project.insert()
        self.new_sandbox = self.new_project.sandboxes.new_sandbox()
        self.new_sandbox.name = "name"
        self.new_project2 = self.kb.projects.new_project()
        self.new_project2.name = self.project_name_2
        self.new_project2.insert()

    def test_sandbox_insert(self):
        # Do insert
        self.new_sandbox.insert()
        # Test that the sandbox has a database generated uuid
        self.assertNotEqual("", self.new_sandbox.uuid)

    def test_get_or_create_sandbox(self):
        sandbox1 = self.new_project.sandboxes.get_or_create_sandbox("test_sandbox")
        sandbox2 = self.new_project.sandboxes.get_sandbox_by_name("test_sandbox")

        self.assertEqual(sandbox1.name, sandbox2.name)
        self.assertEqual(sandbox1.uuid, sandbox2.uuid)

    def test_sandbox_update_and_get(self):
        # Do insert
        self.new_sandbox.insert()
        # Change values and update
        self.new_sandbox.name = "name2"
        self.new_sandbox.update()
        # Test that the new values have been stored
        self.sb2 = self.new_project.sandboxes.get_sandbox_by_name("name2")
        self.assertEqual("name2", self.sb2.name)

    def test_sandbox_refresh(self):
        # Do insert
        self.new_sandbox.insert()
        # Change values and refresh
        self.new_sandbox.name = "name2"
        self.new_sandbox.refresh()
        # Test that values have been restored
        self.assertEqual("name", self.new_sandbox.name)

    # initialize_from_dict needs to generate call objects from server's JSON
    """def test_sandbox_init_from_dict(self):
        # Set up values in a dictionary and initialize a sandbox
        test_dict = {'uuid': 'uuid2', 'name': 'name2',
                     'pipeline': '[{"pipeline_key": "pipeline_value"}]'}
        self.new_sandbox.initialize_from_dict(test_dict)
        # Test sandbox values
        self.assertEqual('uuid2', self.new_sandbox.uuid)
        self.assertEqual('name2', self.new_sandbox.name)"""

    def test_sandbox_delete_cache_empty(self):
        # Do insert
        self.new_sandbox.insert()
        # attempt to delete cache this should hit the server and return a nice
        # response
        self.new_sandbox.delete_cache()

    def test_sandbox_raise_exception_delete_cache_no_sandbox_inserted(self):
        self.assertRaises(Exception, lambda: self.new_sandbox.delete_cache())

    def test_sandbox_update_fails_when_not_insertered_yet(self):
        # Do an update before inserting, this should insert then update
        self.assertRaises(Exception, lambda: self.new_sandbox.update())

    def test_sandbox_delete_raises_exception_when_not_insertered_yet(self):
        # this should work
        self.new_sandbox.insert()
        self.assertNotEqual(self.new_sandbox.uuid, "")
        self.new_sandbox.delete()
        # the sandbox uuid should be empty now
        self.assertEqual(self.new_sandbox.uuid, "")
        # we shouldn't be able to delete the sandbox again
        # or delete the cache from a non existent sandbox
        self.assertRaises(Exception, lambda: self.new_sandbox.delete())
        self.assertRaises(Exception, lambda: self.new_sandbox.delete_cache())

    def test_get_sandboxes(self):
        # Do insert
        self.new_sandbox.insert()
        # Create another test sandbox
        self.new_sandbox2 = self.new_project.sandboxes.new_sandbox()
        self.new_sandbox2.name = "name2"
        self.new_sandbox2.insert()
        # Get sandboxes
        sb = self.new_project.sandboxes.get_sandboxes()
        names = []
        for sandbox in sb:
            names.append(sandbox.name)
        # Test that the names were retrieved
        self.assertTrue("name" in names)
        self.assertTrue("name2" in names)

    def test_sandbox_scope(self):
        # Insert sandbox
        self.new_sandbox.insert()
        sandboxes = self.new_project.sandboxes.get_sandboxes()

        # Try to insert another sandbox with the same name
        # They point to the same eventschema, so this should fail
        self.new_sandbox2 = self.new_project.sandboxes.new_sandbox()
        self.new_sandbox2.name = "name"
        self.assertRaises(HTTPError, lambda: self.new_sandbox2.insert())

        new_sandboxes = self.new_project.sandboxes.get_sandboxes()
        self.assertEqual(len(sandboxes), len(new_sandboxes))  # Insert failed

        # Now insert it under a different project - this should work
        self.new_sandbox2 = self.new_project2.sandboxes.new_sandbox()
        self.new_sandbox2.name = "name"
        self.new_sandbox2.insert()
        sandboxes_2 = self.new_project2.sandboxes.get_sandboxes()
        self.assertEqual(1, len(sandboxes_2))  # Insert succeeded
        # Sandboxes for different eventschemas can have the same name
        self.assertEqual(sandboxes[0].name, sandboxes_2[0].name)

    def test_sandbox_budget_default(self):
        platform = self.kb.platforms.get_platform_by_name("Amulet 4.1")
        self.new_sandbox.device_config.target_platform = platform.id
        self.new_sandbox.insert()

        self.assertTrue("flash" in self.new_sandbox.device_config.budget)

    def test_sandbox_budget_fail(self):
        try:
            self.new_sandbox.device_config.budget = {"flash": 5744, "sram": 1500000}
            self.assertTrue(False)
        except AssertionError:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
