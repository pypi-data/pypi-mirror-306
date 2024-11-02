import os
import pandas as pd
from numpy.testing import assert_array_equal
import pytest
import time

from sensiml.kb_dsk_basic.exceptions import *
from sensiml.tests.basetest import BaseTest
from sensiml.kb_dsk_basic.kb import KB
from pandas import DataFrame


@pytest.mark.skipif(
    pytest.config.option.django, reason="Cannot be run as standalone test."
)
class PipelineTestCase(BaseTest):
    """Unit tests for sandbox pipeline."""

    def setUp(self):
        self.dsk = KB(
            server="localhost",
            path=os.path.join(os.getenv("sensiml_ROOT"), "data", "connect.cfg"),
            username="unittest@intel.com",
            password="inteltest",
        )
        self.dsk.project = "TestProjectForPipeline"
        self.dsk.pipeline = "Sandbox"
        self.dsk.pipeline.reset()

        self.addCleanup(self.dsk_project_cleanup)

    def test_upload_dataframe(self):
        df = pd.DataFrame([range(10)])
        self.dsk.upload_dataframe("test_dataframe", df)
        self.dsk.pipeline.set_input_data("test_dataframe")
        data, stats = self.dsk.pipeline.execute()
        assert_array_equal(df.values, data.values)

    @pytest.mark.skip(reason="Cannot be run on the build server.")
    def test_pipeline_submit(self):
        time.sleep(5)  # the verification builds are running into io/erros here
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_input_data("activity_dataframe", df, force=True)
        self.dsk.pipeline.add_transform(
            "Windowing",
            params={"group_columns": ["Subject", "Class"], "input_column": "accely"},
        )
        self.dsk.pipeline.submit()
        assert self.dsk.pipeline.get_results()[0] == None
        assert self.dsk.pipeline._last_executed == "pipeline"
        r, s = self.dsk.pipeline.get_results(lock=True, wait_time=5)
        assert isinstance(r, DataFrame) == True

    @pytest.mark.skip(reason="This test is broken. Intended result not known.")
    def test_pipeline_revoke(self):
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_input_data("activity_dataframe", df, force=True)
        self.dsk.pipeline.add_transform(
            "Windowing",
            params={"group_columns": ["Subject", "Class"], "input_column": "accely"},
        )
        self.dsk.pipeline.submit()
        assert self.dsk.pipeline.get_results()[0] is None
        self.dsk.pipeline.stop_pipeline()
        assert self.dsk.pipeline.get_results()[0]["status"] == "REVOKED"

    @pytest.mark.skip(reason="Windowing is too fast now :-) for this test.")
    def test_pipeline_already_submitted(self):
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_input_data("activity_dataframe", df, force=True)
        self.dsk.pipeline.add_transform(
            "Windowing",
            params={"group_columns": ["Subject", "Class"], "input_column": "accely"},
        )
        self.dsk.pipeline.submit()
        assert self.dsk.pipeline.get_results()[0] is None
        assert self.dsk.pipeline.submit() == False
        self.dsk.pipeline.stop_pipeline()

    def test_pipeline_set_input_data_fails_if_not_first_step(self):
        with pytest.raises(PipelineOrderException):
            self.dsk.pipeline.add_transform(
                "Windowing",
                params={
                    "group_columns": ["Subject", "Class"],
                    "input_column": "accely",
                },
            )
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_input_data("activity_dataframe", df, force=True)
        with pytest.raises(PipelineOrderException):
            self.dsk.pipeline.set_input_data("activity_dataframe", df, force=True)
            self.dsk.pipeline.set_tvo()

    def test_pipeline_no_execution_type_specified(self):
        assert self.dsk.pipeline._last_executed is None
        assert self.dsk.pipeline.get_results() == (None, None)

    def test_describe_does_not_crash(self):
        self.dsk.pipeline.describe()
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_input_data("activity_dataframe", df, force=True)
        self.dsk.pipeline.add_transform(
            "Windowing",
            params={
                "group_columns": ["Subject", "Class"],
                "input_column": "accely",
            },
        )
        self.dsk.pipeline.describe()

    def test_dsk_add_columns(self):
        self.dsk.pipeline.data_columns = ["A", "B"]
        assert self.dsk.pipeline._data_columns == set(["A", "B"])
        assert self.dsk.pipeline.data_columns == ["A", "B"]
        self.dsk.pipeline.data_columns = "Red"
        assert self.dsk.pipeline.data_columns == ["A", "B"]

        self.dsk.pipeline.label_column = "Activity"
        assert self.dsk.pipeline._label_column == "Activity"
        assert self.dsk.pipeline.label_column == "Activity"

        self.dsk.pipeline.group_columns = ["A", "B"]
        assert self.dsk.pipeline._group_columns == set(["A", "B"])
        assert self.dsk.pipeline.group_columns == ["A", "B"]
        self.dsk.pipeline.data_columns = "Red"
        assert self.dsk.pipeline.group_columns == ["A", "B"]

        self.dsk.pipeline.set_columns(
            data_columns=["C", "D"], group_columns=["R", "S"], label_column="final"
        )

        assert self.dsk.pipeline.data_columns == ["C", "D"]
        assert self.dsk.pipeline.group_columns == ["R", "S"]
        assert self.dsk.pipeline.label_column == "final"
