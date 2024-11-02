import unittest

from sensiml.tests.basetest import BaseTest
from sensiml.functions import Functions


class TrainAndValidationCallTestCase(BaseTest):
    """Unit tests for FunctionCall."""

    def setUp(self):
        self.connection = self._connection
        self.functions = Functions(self.connection)

    def test_train_and_validation_call(self):
        tvo = self.functions.create_train_and_validation_call("tvo")
        tvo.data_in = "data.frame"
        tvo.label_column = "label"
        tvo.group_columns = ["group_col1", "group_col2"]
        tvo.ignore_columns = ["nf_col1", "nf_col2"]

        self.assertEqual("label", tvo.label_column)
        self.assertEqual(["group_col1", "group_col2"], tvo.group_columns)
        self.assertEqual(["nf_col1", "nf_col2"], tvo.ignore_columns)


if __name__ == "__main__":
    unittest.main()
