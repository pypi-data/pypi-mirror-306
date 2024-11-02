import os
import unittest
import warnings

from sensiml.tests.basetest import BaseTest
from sensiml.datamanager.knowledgebuilder import KnowledgeBuilder
from sensiml.method_calls.querycall import QueryCall
from sensiml.pipeline import PipelineError
from sensiml.functions import Functions


class PipelineTestCase(BaseTest):
    """Unit tests for sandbox pipeline."""

    def setUp(self):
        self.connection = self._connection
        self.kb = KnowledgeBuilder(self.connection)
        self.project_name = "TestProjectForPipeline"
        self.functions = Functions(self.connection)

        ## add cleanups
        self.addCleanup(self.project_cleanup)

        # Create new project w/ event schema
        self.new_project = self.kb.projects.new_project()
        self.new_project.name = self.project_name
        self.new_project.insert()

        # Create new sandbox
        self.new_sandbox = self.new_project.sandboxes.new_sandbox()
        self.new_sandbox.name = "name"
        self.new_sandbox.insert()

        # Create new events, eventfiles, and eventmetadata
        # Create new events and metadata
        filename = "test_data_1.csv"
        filename2 = "test_data_2.csv"
        self.new_event = self.new_project.events.create_event(
            filename,
            os.path.join(os.getenv("sensiml_ROOT"), "data", filename),
            asynchronous=False,
        )
        self.new_event2 = self.new_project.events.create_event(
            filename2,
            os.path.join(os.getenv("sensiml_ROOT"), "data", filename2),
            asynchronous=False,
        )

        self.new_event_metadata = self.new_event.metadataset.new_metadata()
        self.new_event_metadata.name = "Subject"
        self.new_event_metadata.value = 28.0
        self.new_event_metadata.insert()
        self.new_event_metadata2 = self.new_event2.metadataset.new_metadata()
        self.new_event_metadata2.name = "Subject"
        self.new_event_metadata2.value = 29.0
        self.new_event_metadata2.insert()

        self.new_project.refresh()
        self.new_project.query_optimize()

        # Create a query
        self.new_query = self.new_project.queries.new_query()
        self.new_query.name = "TestQuery"
        self.new_query.columns.add("HeadGyroscopesY", "HeadAccelerometersZ")
        self.new_query.metadata_filter = "[Subject] > [27.0]"
        self.new_query.insert()

        # Create QueryCall container
        self.qcall = QueryCall("query01")
        self.qcall.query = self.new_query
        self.qcall.outputs = ["temp.data"]

        # Create a test featurefile
        self.new_featurefile = self.new_project.featurefiles.new_featurefile()
        self._testfile_path = "test_featurefile_1.csv"
        with open(self._testfile_path, "w+") as f:
            f.write("animal,sound\ndog,bark\ncat,meow\npig,oink")

    def test_sandbox_pipeline_query(self):
        # Construct and execute a pipeline with the query and transform
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        l = self.new_sandbox.pipeline.to_list()
        self.assertEqual(["temp.data"], l[0]["outputs"])

    def test_sandbox_pipeline_query_and_transform(self):
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        self.new_sandbox.update()
        tcall = self.functions.create_function_call("Normalize")
        tcall.name = "normalize"
        tcall.outputs = ["temp.normalized"]
        tcall.input_data = "temp.data"
        tcall.passthrough_columns = []
        self.new_sandbox.add_step(tcall)
        tcall_list = self.new_sandbox.pipeline.to_list()
        self.assertEqual("transform", tcall_list[1]["type"])

    def test_sandbox_pipeline_no_last_output(self):
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        self.new_sandbox.update()
        tcall = self.functions.create_function_call("Normalize")
        tcall.name = "normalize"
        tcall.input_data = "temp.data"

        # Add the step and check that a warning was produced
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.new_sandbox.add_step(tcall)
            self.assertEqual(
                "FunctionCall normalize does not have any outputs.", str(w[-1].message)
            )

        # Check that the step was added despite the warning
        tcall_list = self.new_sandbox.pipeline.to_list()
        self.assertEqual("transform", tcall_list[1]["type"])

        # Try to add another step and check for exception
        tcall2 = self.functions.create_function_call("Normalize")
        tcall2.name = "normalize2"
        tcall2.outputs = ["temp.normalized"]
        tcall2.input_data = "temp.data"
        with self.assertRaisesRegexp(
            PipelineError, "FunctionCall normalize does not have any outputs."
        ):
            self.new_sandbox.add_step(tcall2)

    def test_query_execution(self):
        # Execute the query and inspect its output
        data, errors = self.new_query.data()
        self.assertEqual((7845, 2), data.shape)

    def test_execution_summary(self):
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        data, stats = self.new_sandbox.execute()
        self.assertEqual(len(stats["execution_summary"]), 1)

    def test_sandbox_execution_summary_cache_and_sandbox_delete_cache(self):
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        data, stats = self.new_sandbox.execute()
        self.assertEqual(stats["execution_summary"]["cached"].iloc[0], False)
        data, stats = self.new_sandbox.execute()
        self.assertEqual(stats["execution_summary"]["cached"].iloc[0], True)
        self.new_sandbox.delete_cache()
        data, stats = self.new_sandbox.execute()
        self.assertEqual(stats["execution_summary"]["cached"].iloc[0], False)

    def test_sandbox_pipeline_query_execution(self):
        # Construct and execute a pipeline with the query and transform
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        self.new_sandbox.update()
        data, stats = self.new_sandbox.execute()
        self.assertEqual((7845, 2), data.shape)

    def test_sandbox_pipeline_mismatch(self):
        """Executes a pipeline with an invalid parameter for the transform."""
        self.new_sandbox.pipeline.clear()
        # Construct and execute a pipeline with the query and transform
        self.new_sandbox.add_step(self.qcall)
        tcall = self.functions.create_function_call("Normalize")
        tcall.input_data = "temp.data"
        tcall.minBound = "-1.0"
        tcall.maxBound = 1.0
        tcall.outputs = ["temp.normalized"]
        self.new_sandbox.add_step(tcall)
        self.new_sandbox.update()

        data, stats = self.new_sandbox.execute()
        assert data["status"] == "FAILURE"

    def test_sandbox_pipeline_duplicate_output(self):
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        self.new_sandbox.update()
        tcall = self.functions.create_function_call("Normalize")
        tcall.name = "normalize"
        tcall.outputs = ["temp.data"]
        with self.assertRaisesRegexp(PipelineError, "Duplicate output:"):
            self.new_sandbox.add_step(tcall)

    def test_sandbox_pipeline_mismatched_input(self):
        self.new_sandbox.pipeline.clear()
        self.new_sandbox.add_step(self.qcall)
        self.new_sandbox.update()
        tcall = self.functions.create_function_call("Normalize")
        tcall.name = "normalize"
        tcall.outputs = ["temp.normalized"]
        tcall.input_data = "temp.mismatched"
        with self.assertRaisesRegexp(PipelineError, "Unmatched input:"):
            self.new_sandbox.add_step(tcall)

    def test_sandbox_pipeline_wrong_number(self):
        """Executes a pipeline with an extra input value. Should be removed during update because sensiml uses the input contract."""
        self.new_sandbox.pipeline.clear()
        # Construct and execute a pipeline with the query and transform
        self.new_sandbox.add_step(self.qcall)
        tcall = self.functions.create_function_call("Normalize")
        tcall.input_data = "temp.data"
        tcall.passthrough_columns = []
        tcall.spuriousInput = 0.0
        tcall.outputs = ["temp.normalized"]
        self.new_sandbox.add_step(tcall)
        self.new_sandbox.update()
        data, stats = self.new_sandbox.execute()
        self.assertEqual((7845, 2), data.shape)

    def test_sandbox_pipeline_featurefile(self):
        self.new_featurefile.filename = "NameOfFeatureFile.csv"
        self.new_featurefile.path = self._testfile_path
        self.new_featurefile.insert()
        ffcall = self.functions.create_featurefile_call("NameOfFeatureFile.csv")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("default")
            self.new_sandbox.add_step(ffcall)
            self.assertEqual(1, len(caught))
        ffcall.outputs = ["temp.ff"]
        data, stats = self.new_sandbox.execute()
        self.assertEqual("animal", data.columns[0])
        self.assertEqual("sound", data.columns[1])
        self.assertEqual({"pig", "dog", "cat"}, set(data["animal"]))
        self.assertEqual({"bark", "oink", "meow"}, set(data["sound"]))


if __name__ == "__main__":
    unittest.main()
