from __future__ import annotations
import sensiml.base.utility as utility
from sensiml.datamanager.featurefile import FeatureFile
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sensiml.connection import Connection
    from sensiml.datamanager.project import Project


class FeatureFileExistsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FeatureFiles:
    """Base class for a collection of featurefiles."""

    def __init__(self, connection: Connection, project: Project):
        self._connection = connection
        self._project = project

    def create_featurefile(
        self,
        filename: str,
        path: str,
        is_features: bool = False,
        label_column: str = "",
    ) -> FeatureFile:
        """Creates a featurefile object from the filename and path.

        Args:
            filename (str): desired name of the featurefile on the server, must have a .csv or .arff extension
            path (str): full local path to the file, including the file's local name and extension

        Returns:
            featurefile object

        Raises:
            FeatureFileExistsError, if the featurefile already exists on the server
        """
        if self.build_full_list().get(filename) is not None:
            raise FeatureFileExistsError(f"featurefile {filename} already exists.")
        else:
            featurefile = self.new_featurefile()
            featurefile.name = filename
            featurefile.path = path
            featurefile.is_features = is_features
            self.label_column = label_column
            featurefile.insert()
            return featurefile

    def build_full_list(self) -> dict:
        """Populates the function_list property from the server."""
        featurefile_list = {}

        featurefile_response = self.get_featurefiles()
        for featurefile in featurefile_response:
            featurefile_list[featurefile.name] = featurefile

        return featurefile_list

    def build_featurefile_list(self) -> dict:
        """Populates the function_list property from the server."""
        featurefile_list = {}

        featurefile_response = self.get_featurefiles()
        for featurefile in featurefile_response:
            if featurefile.is_features:
                featurefile_list[featurefile.name] = featurefile

        return featurefile_list

    def build_datafile_list(self) -> dict:
        """Populates the function_list property from the server."""
        datafile_list = {}

        featurefile_response = self.get_featurefiles()
        for featurefile in featurefile_response:
            if not featurefile.is_features:
                datafile_list[featurefile.name] = featurefile

        return datafile_list

    def get_by_name(self, filename: str) -> FeatureFile:
        """Gets a featurefile or datafile from the server referenced by name.

        Args:
            filename: name of the featurefile as stored on the server

        Returns:
            featurefile object or None if it does not exist
        """
        return self.build_full_list().get(filename, None)

    def new_featurefile(self) -> FeatureFile:
        """Initializes a new featurefile object, but does not insert it."""
        featurefile = FeatureFile(self._connection, self._project)
        return featurefile

    def _new_featurefile_from_dict(self, data_dict: dict) -> FeatureFile:
        """Creates a featurefile object from a dictionary of properties.

        Args:
            dict (dict): contains featurefile's 'name' and 'uuid' properties

        Returns:
            featurefile object
        """
        featurefile = FeatureFile(self._connection, self._project)
        featurefile.initialize_from_dict(data_dict)
        return featurefile

    def get_featurefiles(self) -> list[FeatureFile]:
        """Gets a list of all featurefiles in the project.

        Returns:
            list (featurefiles)
        """
        err = False
        url = f"project/{self._project.uuid}/featurefile/"
        response = self._connection.request("get", url)
        try:
            response_data, err = utility.check_server_response(response)
        except ValueError:
            print(response)
        # Populate the retrieved featurefiles
        featurefiles = []
        if err is False:
            for featurefile_params in response_data:
                featurefiles.append(self._new_featurefile_from_dict(featurefile_params))

        return featurefiles

    def get_featurefile(self, uuid) -> FeatureFile:
        """Gets a list of all featurefiles in the project.

        Returns:
            list (featurefiles)
        """
        err = False
        url = f"project/{self._project.uuid}/featurefile/{uuid}/"
        response = self._connection.request("get", url)

        try:
            response_data, err = utility.check_server_response(response)
        except ValueError:
            print(response)

        featurefile = None
        if err is False:
            featurefile = self._new_featurefile_from_dict(response_data)

        return featurefile
