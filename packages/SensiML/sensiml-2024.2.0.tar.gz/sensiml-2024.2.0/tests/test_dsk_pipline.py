import os
import pytest
import time

from sensiml.tests.basetest import BaseTest
from sensiml.kb_dsk_basic.kb import KB


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

    def test_pipeline_group_column_added(self):
        time.sleep(5)  # the verification builds are running into io/erros here
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_columns(group_columns=["Subject", "Class"])
        self.dsk.pipeline.set_input_data(
            "activity_dataframe",
            df,
            force=True,
            data_columns=["accelx", "accely", "accelz"],
        )
        self.dsk.pipeline.add_transform("Windowing", {"input_column": "accely"})
        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(
            sorted(["Subject", "Class"]), sorted(pl[-1]["inputs"]["group_columns"])
        )
        self.dsk.pipeline.add_transform("Segment Filter MSE")
        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(
            sorted(["Subject", "Class", "SegmentID"]),
            sorted(pl[-1]["inputs"]["group_columns"]),
        )

    def test_pipeline_label_group_ignore_added(self):
        time.sleep(5)  # the verification builds are running into io/erros here
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_columns(
            group_columns=["Subject", "Class"], label_column="Class"
        )
        self.dsk.pipeline.set_input_data(
            "activity_dataframe",
            df,
            force=True,
            data_columns=["accelx", "accely", "accelz"],
        )
        self.dsk.pipeline.add_transform("Windowing")
        self.dsk.pipeline.add_transform(
            "Segment Filter MSE",
            params={
                "input_column": "accely",
            },
        )

        self.dsk.pipeline.add_feature_generator(
            [
                "Mean",
                "Standard Deviation",
                "Skewness",
                "Kurtosis",
                "25th Percentile",
                "75th Percentile",
                "100th Percentile",
                "Zero Crossing Rate",
            ],
            function_defaults={"columns": ["accelx", "accely", "accelz"]},
        )

        self.dsk.pipeline.add_feature_selector(
            [{"name": "Recursive Feature Elimination", "params": {"method": "Log R"}}],
            params={
                "number_of_features": 8,
            },
        )

        self.dsk.pipeline.add_transform("Min Max Scale")

        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(
            sorted(pl[-1]["inputs"]["passthrough_columns"]),
            sorted(["Class", "SegmentID", "Subject"]),
        ),

        self.dsk.pipeline.set_validation_method(
            "Stratified K-Fold Cross-Validation", params={"number_of_folds": 5}
        )

        self.dsk.pipeline.set_classifier(
            "PME", params={"classification_mode": "RBF", "distance_mode": "L1"}
        )

        self.dsk.pipeline.set_training_algorithm(
            "Hierarchical Clustering with Neuron Optimization",
            params={"number_of_neurons": 7},
        )

        self.dsk.pipeline.set_tvo({"validation_seed": 0})

        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(
            sorted(["SegmentID", "Subject"]), sorted(pl[-1]["ignore_columns"])
        )
        self.assertEqual("Class", pl[-1]["label_column"])

    def test_pipeline_reset_values(self):
        time.sleep(5)  # the verification builds are running into io/erros here
        df = self.dsk.datasets.load_activity_raw()
        self.dsk.pipeline.set_columns(group_columns=["Subject", "Class"])
        self.dsk.pipeline.set_input_data(
            "activity_dataframe",
            df,
            force=True,
            data_columns=["accelx", "accely", "accelz"],
        )
        self.dsk.pipeline.add_transform("Windowing")
        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(pl[-1]["inputs"]["delta"], 250)
        self.dsk.pipeline.add_transform("Windowing", params={"delta": 100})
        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(pl[-1]["inputs"]["delta"], 100)
        self.assertEqual(len(pl), 2)
        self.dsk.pipeline.add_transform(
            "Segment Filter MSE",
            params={
                "input_column": "accely",
            },
        )

        self.dsk.pipeline.add_feature_generator(
            [
                "Mean",
                "Standard Deviation",
                "Skewness",
                "Kurtosis",
                "25th Percentile",
                "75th Percentile",
                "100th Percentile",
                "Zero Crossing Rate",
            ],
            function_defaults={"columns": ["accelx", "accely", "accelz"]},
        )

        self.dsk.pipeline.add_feature_selector(
            [{"name": "Recursive Feature Elimination", "params": {"method": "Log R"}}],
            params={
                "number_of_features": 8,
            },
        )

        self.dsk.pipeline.add_transform("Windowing", params={"delta": 200})
        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(pl[1]["inputs"]["delta"], 200)

        self.dsk.pipeline.add_transform("Min Max Scale")

        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(
            sorted(pl[-1]["inputs"]["passthrough_columns"]),
            sorted(["Class", "SegmentID", "Subject"]),
        )

        self.dsk.pipeline.set_validation_method(
            "Stratified K-Fold Cross-Validation", params={"number_of_folds": 5}
        )

        self.dsk.pipeline.set_classifier(
            "PME", params={"classification_mode": "RBF", "distance_mode": "L1"}
        )

        self.dsk.pipeline.set_training_algorithm(
            "Hierarchical Clustering with Neuron Optimization",
            params={"number_of_neurons": 7},
        )

        self.dsk.pipeline.set_tvo({"validation_seed": 0})

        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(pl[-1]["classifiers"][0]["inputs"]["distance_mode"], "L1")

        self.dsk.pipeline.set_classifier(
            "PME", params={"classification_mode": "RBF", "distance_mode": "LSUP"}
        )
        self.dsk.pipeline.set_tvo({"validation_seed": 0})
        pl = self.dsk.pipeline._sandbox.pipeline.to_list()
        self.assertEqual(pl[-1]["classifiers"][0]["inputs"]["distance_mode"], "LSUP")
