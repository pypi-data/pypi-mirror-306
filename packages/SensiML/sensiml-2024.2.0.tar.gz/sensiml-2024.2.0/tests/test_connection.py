# from mock import *
import pytest
from sensiml.connection.connection import Connection

pytestmark = [pytest.mark.live_db]


@pytest.fixture
def tmpfilename():
    """Creates tempfile and closes it without deleting

    Returns: path to file
    """
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(delete=False) as f:
        name = f.name
    yield name
    os.remove(name)


def test_init_with_url(oauth):
    conn = Connection(**oauth)
    assert conn.server_url.rstrip("/") == oauth["url"].rstrip(
        "/"
    ), "incorrect assignment of url"


def test_incorrect_password(oauth):
    oauth["password"] = "wrongpassword"
    # Connection will ask for username/password input again so IOError will be raised in pytest
    with pytest.raises(IOError):
        Connection(**oauth)


def test_incorrect_username(oauth):
    oauth["username"] = "username@not.exist"
    with pytest.raises(IOError):
        Connection(**oauth)


def test_multiple_connection(oauth, tmpfilename):
    from sensiml.connection import ConnectionConfig

    config = ConnectionConfig("localhost")
    config.update(**oauth)
    config.save(tmpfilename)

    c1 = Connection(
        "localhost",
        path=tmpfilename,
        username=config.username,
        password=config.password,
        insecure=True,
    )
    c2 = Connection(
        "localhost",
        path=tmpfilename,
        username=config.username,
        password=config.password,
        insecure=True,
    )
    response = c1.request("get", "/project/")
    assert response.status_code == 200
    response = c2.request("get", "/project/")
    assert response.status_code == 200
