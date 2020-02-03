import pytest
from server import createApp
import mock
import requests_mock

EXAMPLE_USER_ID = "123"
EXAMPLE_USER_ID_NO_BALANCE = "1234"


@pytest.fixture
def client():
    with requests_mock.mock(real_http=True) as m:
        m.post(
            "http://localhost:5050/api/transaction/{}".format(EXAMPLE_USER_ID),
            json={"transactionId": 10},
            status_code=201,
        )
        m.post(
            "http://localhost:5050/api/transaction/{}".format(
                EXAMPLE_USER_ID_NO_BALANCE
            ),
            json={
                "error": "user does not have enough balance for this transaction"
            },
            status_code=400,
        )
        m.get(
            "http://localhost:8080/user/{}".format(EXAMPLE_USER_ID),
            json={
                "UserID": EXAMPLE_USER_ID,
                "Username": "test",
                "Address": "",
                "Email": "",
                "Password": "",
                "PhoneNumber": 0,
                "AccountBalance": 2001,
            },
        )
        m.get(
            "http://localhost:8080/user/{}".format(EXAMPLE_USER_ID_NO_BALANCE),
            json={
                "UserID": EXAMPLE_USER_ID_NO_BALANCE,
                "Username": "test",
                "Address": "",
                "Email": "",
                "Password": "",
                "PhoneNumber": 0,
                "AccountBalance": 0,
            },
        )
        args = mock.Mock()
        args.t = True
        flask_app = createApp(args)
        testing_client = flask_app.app.test_client()
        ctx = flask_app.app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()
