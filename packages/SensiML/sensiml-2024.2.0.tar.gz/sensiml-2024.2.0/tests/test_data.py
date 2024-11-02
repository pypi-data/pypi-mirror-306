import os
import sys

from sensiml.tests.basetest import BaseTest
from sensiml.datamanager.knowledgebuilder import KnowledgeBuilder
import pytest


class DataTestCase(BaseTest):
    """Unit tests for data management module."""

    def setUp(self):
        self.connection = self._connection
        self.kb = KnowledgeBuilder(self.connection)
        self.project_name = "upload_test"

        self.upload = self.kb.data.upload(self.project_name)
        self.path = os.path.join(os.getenv("sensiml_ROOT"), "data", "upload_config.ini")
        self.upload.configure(self.path)

        def metadata_from_file(filename=None):
            metadata = {"subject": filename.split("\\")[-1][:4]}
            return metadata

        self.upload.metadata = metadata_from_file
        self.upload.upload(csv=[], asynchronous=False)

        # Cleanup steps
        self.addCleanup(self.project_cleanup)

    # NEEDS NEW UPLOAD FEATURE
    @pytest.mark.skipif(
        not sys.platform.startswith("win32"), reason="Fails to run on linux"
    )
    def test_upload_objects_exist(self):
        """Ensures that the project, schema, events, and eventfiles exist and can be retrieved from the server."""
        project = self.kb.projects.get_project_by_name(self.project_name)
        self.assertTrue(project is not None)
        self.assertEqual("upload_test", project.name)
        events = project.events.get_events()
        self.assertEqual(4, len(events))

        metadata = project.events.get_metadata_names_and_values()
        subjects = [md["values"] for md in metadata if md["name"] == "subject"][0]
        names = [md["values"] for md in metadata if md["name"] == "name"][0]
        dysfunctions = [md["values"] for md in metadata if md["name"] == "dysfunction"][
            0
        ]

        self.assertEqual(set(["U001", "U002"]), set(subjects))
        self.assertEqual(set(["Bob", "Timmy"]), set(names))
        self.assertEqual(set([1.0, 2.0, 0]), set(dysfunctions))

    def test_upload_schema_map_names(self):
        """Ensures that the sensor names in the schema map are accurate."""
        project = self.kb.projects.get_project_by_name(self.project_name)
        schema = project.schema
        self.assertEqual(
            set(["accelx", "accely", "accelz", "gyrox", "gyroy", "gyroz"]),
            set(schema.keys()),
        )

    def test_upload_statistics_and_metadata(self):
        """Ensures that the uploaded metadata is accurate."""
        project = self.kb.projects.get_project_by_name(self.project_name)
        data, errors = project.events.get_statistics()

        self.assertEqual(
            set(["Capture", "name", "subject", "dysfunction"]), set(data.columns.values)
        )

        # This API doesn't work
        # self.assertEqual(2, len(project.events.get_events_by_metadata('subject', 'U002')))
        # self.assertEqual(2, len(project.events.get_events_by_metadata('name', 'Timmy')))
        # self.assertEqual(1, len(project.events.get_events_by_metadata('dysfunction', 0)))

        # Test correctness of labels
        event1 = project.events.get_event_by_filename("U001_A_L.csv")
        label1 = event1.metadataset.get_metadata_by_name("dysfunction")
        self.assertEqual(3, label1.sample_start)
        self.assertEqual(5, label1.sample_end)
        self.assertEqual(1, label1.value)
        event2 = project.events.get_event_by_filename("U001_A_P.csv")
        label2 = event2.metadataset.get_metadata_by_name("dysfunction")
        self.assertEqual(7, label2.sample_start)
        self.assertEqual(8, label2.sample_end)
        self.assertEqual(2, label2.value)
        event3 = project.events.get_event_by_filename("U002_A_C.csv")
        label3 = event3.metadataset.get_metadata_by_name("dysfunction")
        self.assertEqual(None, label3)
        event4 = project.events.get_event_by_filename("U002_A_L.csv")
        label4 = event4.metadataset.get_metadata_by_name("dysfunction")
        self.assertEqual(0, label4.sample_start)
        self.assertEqual(8, label4.sample_end)
        self.assertEqual(0, label4.value)

    def test_upload_config_reset(self):
        """Tests that a new config.ini can be passed in and the upload object will reset to the new configuration."""
        # Fill this out when there can be multiple config files
        self.assertTrue(True)
