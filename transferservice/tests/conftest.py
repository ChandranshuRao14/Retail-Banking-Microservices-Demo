import pytest
from server import createApp
import mock


@pytest.fixture
def client():
    args = mock.Mock()
    args.t = True
    flask_app = createApp(args)
    testing_client = flask_app.app.test_client()
    ctx = flask_app.app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()
