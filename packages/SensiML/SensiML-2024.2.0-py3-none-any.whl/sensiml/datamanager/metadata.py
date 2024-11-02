from __future__ import annotations
import logging

from sensiml.datamanager.base import BaseSet
from sensiml.datamanager.label import Label


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sensiml.connection import Connection
    from sensiml.datamanager.project import Project

logger = logging.getLogger(__name__)


class Metadata(Label):
    """Base class for a label object."""

    @property
    def _label_or_metadata(self):
        return "metadata"

    @property
    def _metadata(self):
        return True

    @property
    def metadata(self):
        return True


class MetadataSet(BaseSet):
    def __init__(
        self, connection: Connection, project: Project, initialize_set: bool = True
    ):
        """Initialize a metadata object.

        Args:
            connection
            project
        """

        self._connection = connection
        self._project = project
        self._objclass = Metadata
        self._set = None
        self._attr_key = "name"
        self._data = None

        if initialize_set:
            self.refresh()

    @property
    def metadata(self):
        return self.objs

    @property
    def get_set_url(self) -> str:
        return f"project/{self._project.uuid}/metadata/"

    def __str__(self) -> str:
        s = ""
        for obj in self.objs:
            s += f"name: {obj.name} uuid {obj.uuid}\n"

        return s
