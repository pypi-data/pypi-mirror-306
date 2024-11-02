from __future__ import annotations
from sensiml.base import utility
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sensiml.connection import Connection


class Team(object):
    """Base class for a transform object"""

    _uuid = ""
    _name = None

    def __init__(self, connection: Connection):
        self._connection = connection

    def get_user(self):
        """Get Information about the users on your team."""

        url = "user/"
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)

        if err is False:
            return response_data

        return response

    def team_subscription(self):
        """Get Information about your teams subscription."""
        url = "team-subscription/"
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)

        if err is False:
            return response_data

        return response

    def team_info(self):
        """Get information about your specific team."""
        url = "team-info/"
        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)

        if err is False:
            return response_data

        return response
