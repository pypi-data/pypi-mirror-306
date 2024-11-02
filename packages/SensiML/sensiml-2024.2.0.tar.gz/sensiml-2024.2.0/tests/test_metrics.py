import unittest

from sensiml.tests.basetest import BaseTest
from sensiml.datamanager.knowledgebuilder import KnowledgeBuilder


class MetricsSetTestCase(BaseTest):
    """tests the ability to retrieve a metrics set from the server"""

    def setUp(self):
        self.truth_pred = {
            "y_true": [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3],
            "y_pred": [1, 1, 2, 3, 1, 2, 2, 1, 2, 3, 3, 3, 3, 3],
        }
        self.f1_score = {
            "1": 74.99999999999999,
            "3": 100.0,
            "2": 85.71428571428571,
            "average": 77.70562770562769,
        }
        self.sensitivity = {
            "1": 60.0,
            "3": 100.0,
            "2": 75.0,
            "average": 78.57142857142857,
        }
        self.precision = {
            "1": 100.0,
            "3": 100.0,
            "2": 100.0,
            "average": 77.97619047619048,
        }
        self.positive_predictive_rate = {
            "1": 60.0,
            "3": 100.0,
            "2": 75.0,
            "average": 78.33333333333333,
        }
        self.accuracy = 78.57142857142857
        self.confusion_matrix = {
            "1": {"1": 3, "2": 1, "3": 1, "UNC": 0, "UNK": 0},
            "2": {"1": 1, "2": 3, "3": 0, "UNC": 0, "UNK": 0},
            "3": {"1": 0, "2": 0, "3": 5, "UNC": 0, "UNK": 0},
            "UNC": {"1": 0, "2": 0, "3": 0, "UNC": 0, "UNK": 0},
            "UNK": {"1": 0, "2": 0, "3": 0, "UNC": 0, "UNK": 0},
        }

        self.connection = self._connection
        self.kb = KnowledgeBuilder(self.connection)
        self.project_name = "TestProjectForMetrics"
        self.new_project = self.kb.projects.new_project()
        self.new_project.name = self.project_name
        self.new_project.insert()

        self.new_sandbox = self.new_project.sandboxes.new_sandbox()
        self.new_sandbox.name = "TestSandboxForMetrics"
        self.new_sandbox.insert()

        self.addCleanup(self.cleanup)

    def test_metrics_set(self):
        """tests the ability to obtain the same metrics results as the server side unit tests on the client"""
        metrics_set = self.new_sandbox.get_metrics_set(self.truth_pred)
        for key in self.f1_score.keys():
            self.assertEqual(
                self.f1_score[key], metrics_set["results"]["f1_score"][key]
            )
        for key in self.sensitivity.keys():
            self.assertEqual(
                self.sensitivity[key], metrics_set["results"]["sensitivity"][key]
            )
        for key in self.positive_predictive_rate.keys():
            self.assertEqual(
                self.positive_predictive_rate[key],
                metrics_set["results"]["positive_predictive_rate"][key],
            )
        for key in self.precision.keys():
            self.assertEqual(
                self.precision[key], metrics_set["results"]["precision"][key]
            )
        self.assertEqual(self.accuracy, metrics_set["results"]["accuracy"])
        # self.assertIsNotNone(metrics_set['results']['specificity'])

    def cleanup(self):
        # Delete the test project
        self.new_project.delete()


if __name__ == "__main__":
    unittest.main()
