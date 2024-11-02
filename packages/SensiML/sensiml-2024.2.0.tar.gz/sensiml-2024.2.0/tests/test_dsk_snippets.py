import os
import pytest

from sensiml.tests.basetest import BaseTest
from sensiml.kb_dsk_basic.kb import KB
import sensiml.kb_dsk_basic.snippets as snippets


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

    def test_snippets(self):
        windowing = (
            self.dsk.snippets.Segmenter.Windowing()
            .replace("\t", "")
            .replace("\n", "")
            .replace(" ", "")
        )
        self.assertEqual(
            windowing,
            'dsk.pipeline.add_transform("Windowing",params={"window_size":250,"delta":250,"return_segment_index":False})',
        )
        absolute_area_fg = (
            self.dsk.snippets.Feature_Generator.Absolute_Area()
            .replace("\t", "")
            .replace("\n", "")
            .replace(" ", "")
        )
        self.assertEqual(
            absolute_area_fg,
            "dsk.pipeline.add_feature_generator([{'name':'AbsoluteArea','params':{\"sample_rate\":<numeric>,\"columns\":<list>}}])",
        )
        training = (
            self.dsk.snippets.Training_Algorithm.Hierarchical_Clustering_with_Neuron_Optimization()
            .replace("\t", "")
            .replace("\n", "")
            .replace(" ", "")
        )
        self.assertEqual(
            training,
            'dsk.pipeline.set_training_algorithm("HierarchicalClusteringwithNeuronOptimization",params={"number_of_neurons":<int>,"linkage_method":<average/complete/ward/single>,"centroid_calculation":<robust/mean/median>,"flip":<int>,"cluster_method":<DHC/DLHC/kmeans>,"aif_method":<min/max/robust/mean/median>,"singleton_aif":<int>,"min_number_of_dominant_vector":<int>,"max_number_of_weak_vector":<int>})',
        )

    def test_pipeline_snippets_query_step(self):
        steps = [{"name": "query_gesture", "outputs": ["temp.raw"], "type": "query"}]
        result = snippets.build_pipeline(self.dsk.functions.function_list, steps)[1]
        expected_result = (
            'dsk.pipeline.set_input_query("query_gesture", label_column="None")'
        )
        self.assertEqual(result, expected_result)

    def test_pipeline_segmenter(self):
        steps = [
            {
                "feature_table": None,
                "inputs": {
                    "axis_of_interest": "GyroscopeY",
                    "group_columns": ["Label", "Subject"],
                    "input_data": "temp.raw",
                    "max_segment_length": 225,
                    "return_segment_index": False,
                    "warmup": False,
                },
                "name": "Double Twist Segmentation",
                "outputs": ["temp.Double_Twist_Segmentation0"],
                "type": "segmenter",
            }
        ]

        result = snippets.pipeline_function_help(
            self.dsk.functions.function_list, steps[0]
        )
        expected_result = 'dsk.pipeline.add_transform("Double Twist Segmentation", params={"axis_of_interest":"GyroscopeY", "max_segment_length":225, "warmup":False})'
        self.assertEqual(result, expected_result)
        result = snippets.build_pipeline(self.dsk.functions.function_list, steps)[1]
        self.assertEqual(result, expected_result)

    def test_pipeline_transform(self):
        steps = [
            {
                "feature_table": None,
                "inputs": {
                    "group_columns": ["Label", "SegmentID", "Subject"],
                    "input_columns": [
                        "GyroscopeY",
                        "GyroscopeX",
                        "GyroscopeZ",
                        "AccelerometerY",
                        "AccelerometerX",
                        "AccelerometerZ",
                    ],
                    "input_data": "temp.Double_Twist_Segmentation0",
                    "type": "mean",
                },
                "name": "Strip",
                "outputs": ["temp.Strip0"],
                "type": "transform",
            }
        ]

        result = snippets.pipeline_function_help(
            self.dsk.functions.function_list, steps[0]
        )
        expected_result = """dsk.pipeline.add_transform("Strip", params={"input_columns":[u'GyroscopeY', u'GyroscopeX', u'GyroscopeZ', u'AccelerometerY', u'AccelerometerX', u'AccelerometerZ'], "type":"mean"})"""
        self.assertEqual(result, expected_result)
        result = snippets.build_pipeline(self.dsk.functions.function_list, steps)[1]
        self.assertEqual(result, expected_result)

    def test_pipeline_feature_generators(self):
        steps = [
            {
                "inputs": {
                    "group_columns": ["Label", "SegmentID", "Subject"],
                    "input_data": "temp.Strip0",
                },
                "name": "generator_set",
                "outputs": ["temp.generator_set0", "temp.features.generator_set0"],
                "set": [
                    {
                        "function_name": "Downsample",
                        "inputs": {
                            "columns": [
                                "AccelerometerZ",
                                "AccelerometerX",
                                "AccelerometerY",
                            ],
                            "new_length": 12,
                        },
                    },
                    {
                        "function_name": "Mean",
                        "inputs": {
                            "columns": [
                                "AccelerometerZ",
                                "AccelerometerX",
                                "AccelerometerY",
                            ]
                        },
                    },
                ],
                "type": "generatorset",
            },
        ]

        result = snippets.pipeline_function_help(
            self.dsk.functions.function_list, steps[0]["set"][0]
        )
        expected_result = """{'name':'Downsample', 'params':{"columns":[u'AccelerometerZ', u'AccelerometerX', u'AccelerometerY'], "new_length":12}}"""
        self.assertEqual(result, expected_result)
        # expected_result  = """dsk.pipeline.add_feature_generator([{'name':'Downsample', 'params':{"columns":[u'AccelerometerZ', u'AccelerometerX', u'AccelerometerY'], "new_length":12}},
        #                                                          {'name':'Mean', 'params':{"columns":[u'AccelerometerZ', u'AccelerometerX', u'AccelerometerY']}}])"""
        result = snippets.build_pipeline(self.dsk.functions.function_list, steps)
        self.assertEqual(len(result), 2)

    def test_pipeline_feature_selectors(self):
        steps = [
            {
                "inputs": {
                    "cost_function": "sum",
                    "feature_table": "temp.features.Normalize0",
                    "input_data": "temp.Normalize0",
                    "label_column": "Label",
                    "number_of_features": "",
                    "passthrough_columns": ["Label", "SegmentID", "Subject"],
                    "remove_columns": [],
                },
                "name": "selector_set",
                "outputs": ["temp.selector_set0", "temp.features.selector_set0"],
                "refinement": {},
                "set": [
                    {
                        "function_name": "Recursive Feature Elimination",
                        "inputs": {"method": "LogR"},
                    }
                ],
                "type": "selectorset",
            },
        ]

        result = snippets.pipeline_function_help(
            self.dsk.functions.function_list, steps[0]["set"][0]
        )
        expected_result = (
            """{'name':'Recursive Feature Elimination', 'params':{"method":"LogR"}}, """
        )
        self.assertEqual(result, expected_result)
        expected_result = """dsk.pipeline.add_feature_selector([{'name':'Recursive Feature Elimination', 'params':{"method":"LogR"}}, ])"""
        result = snippets.build_pipeline(self.dsk.functions.function_list, steps)[1]
        self.assertEqual(result, expected_result)

    def test_pipeline_tvo(self):
        steps = [
            {
                "classifiers": [
                    {
                        "inputs": {"classification_mode": "RBF", "distance_mode": "L1"},
                        "name": "PME",
                    }
                ],
                "feature_table": "temp.features.Min_Max_Scale0",
                "ignore_columns": ["SegmentID", "Subject"],
                "input_data": "temp.Min_Max_Scale0",
                "label_column": "Label",
                "name": "tvo",
                "optimizers": [
                    {
                        "inputs": {"number_of_neurons": 10},
                        "name": "Hierarchical Clustering with Neuron Optimization",
                    }
                ],
                "outputs": ["temp.tvo0", "temp.features.tvo0"],
                "type": "tvo",
                "validation_methods": [
                    {
                        "inputs": {"number_of_folds": 3},
                        "name": "Stratified K-Fold Cross-Validation",
                    }
                ],
                "validation_seed": 0,
            }
        ]

        result = snippets.pipeline_function_help(
            self.dsk.functions.function_list, steps[0]["optimizers"][0]
        )
        expected_result = """dsk.pipeline.set_training_algorithm("Hierarchical Clustering with Neuron Optimization", params={"number_of_neurons":10})"""
        self.assertEqual(result, expected_result)

        result = snippets.pipeline_function_help(
            self.dsk.functions.function_list, steps[0]["validation_methods"][0]
        )
        expected_result = """dsk.pipeline.set_validation_method("Stratified K-Fold Cross-Validation", params={"number_of_folds":3})"""
        self.assertEqual(result, expected_result)

        result = snippets.pipeline_function_help(
            self.dsk.functions.function_list, steps[0]["classifiers"][0]
        )
        expected_result = """dsk.pipeline.set_classifier("PME", params={"distance_mode":"L1", "classification_mode":"RBF"})"""
        self.assertEqual(result, expected_result)

        result = snippets.build_pipeline(self.dsk.functions.function_list, steps)
        self.assertEqual(len(result), 5)
