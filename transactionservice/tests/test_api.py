from openapi_spec_validator import validate_spec
import json, requests


VALID_TRANSACTION = dict()
VALID_TRANSACTION["amount"] = "100"
VALID_TRANSACTION["transactionType"] = "credit"

INVALID_TRANSACTION_LESS_KEYS = dict()
INVALID_TRANSACTION_LESS_KEYS["amount"] = "100"

INVALID_TRANSACTION_WRONG_KEYS = dict()
INVALID_TRANSACTION_WRONG_KEYS["transactionType"] = "credit"
INVALID_TRANSACTION_WRONG_KEYS["amount"] = "100"
INVALID_TRANSACTION_WRONG_KEYS["loremipsom"] = "200"

INVALID_TRANSACTION_WRONG_TRANSACTIONTYPE = dict()
INVALID_TRANSACTION_WRONG_TRANSACTIONTYPE["transactionType"] = "loremipsom"
INVALID_TRANSACTION_WRONG_TRANSACTIONTYPE["amount"] = "100"
"""
**************************************
Validate OpenAPI Spec
**************************************
"""


def test_validate_openapi_spec(client):
    assert validate_spec(client.get("/test/api/openapi.json").get_json()) == None


"""
**************************************
Validate POST Transfer
**************************************
"""


def test_post_transaction(client):

    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(VALID_TRANSACTION), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transactionId" in [*data]


def test_post_transaction_fail_required_keys(client):
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(INVALID_TRANSACTION_LESS_KEYS), headers=headers
    )
    assert post_response.status_code == 400
    data = post_response.get_json()
    assert "error" in [*data]


def test_post_transaction_fail_extra_keys(client):
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(INVALID_TRANSACTION_WRONG_KEYS), headers=headers
    )
    assert post_response.status_code == 400
    data = post_response.get_json()
    assert "error" in [*data]


def test_post_transaction_fail_wrong_transaction_type(client):
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction",
        data=json.dumps(INVALID_TRANSACTION_WRONG_TRANSACTIONTYPE),
        headers=headers,
    )
    assert post_response.status_code == 400


"""
**************************************
Validate GET Transfer
**************************************
"""


def test_get_transaction(client):
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(VALID_TRANSACTION), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transactionId" in [*data]
    transactionId = data["transactionId"]
    get_response = client.get("/test/api/transaction/{}".format(transactionId))
    data = get_response.get_json()
    assert "transactionType" in [*data]
    assert "amount" in [*data]


def test_get_transaction_fail(client):
    get_response = client.get("/test/api/transaction/1")
    assert get_response.status_code == 400


"""
**************************************
Validate Update Transfer
**************************************
"""


def test_update_transaction(client):
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(VALID_TRANSACTION), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transactionId" in [*data]
    transactionId = data["transactionId"]
    transaction = dict()
    transaction["transactionType"] = "debit"
    transaction["amount"] = "400"
    put_response = client.put(
        "/test/api/transaction/{}".format(transactionId),
        data=json.dumps(transaction),
        headers=headers,
    )
    assert put_response.status_code == 200
    data = put_response.get_json()
    assert data["transactionType"] == transaction["transactionType"]
    assert data["amount"] == transaction["amount"]
    assert data["transactionId"] == transactionId


def test_update_transaction_fail(client):
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(VALID_TRANSACTION), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transactionId" in [*data]
    transactionId = data["transactionId"]
    put_response = client.put(
        "/test/api/transaction/{}".format(transactionId),
        data=json.dumps(INVALID_TRANSACTION_WRONG_KEYS),
        headers=headers,
    )
    assert put_response.status_code == 400
    data = put_response.get_json()
    assert "error" in [*data]


"""
**************************************
Validate Delete Transfer
**************************************
"""


def test_delete_transaction(client):
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(VALID_TRANSACTION), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transactionId" in [*data]
    transactionId = data["transactionId"]
    delete_response = client.delete("/test/api/transaction/{}".format(transactionId))
    assert delete_response.status_code == 204


def test_delete_transaction_fail(client):
    delete_response = client.delete("/test/api/transaction/1")
    assert delete_response.status_code == 400


"""
**************************************
Validate All Transfers
**************************************
"""


def test_all_transaction(client):
    get_response = client.get("/test/api/transaction")
    data = get_response.get_json()
    for transaction in data:
        delete_response = client.delete(
            "/test/api/transaction/{}".format(transaction["transactionId"])
        )
        assert delete_response.status_code == 204
    headers = {"content-type": "application/json"}
    post_response = client.post(
        "/test/api/transaction", data=json.dumps(VALID_TRANSACTION), headers=headers
    )
    assert post_response.status_code == 201
    get_response = client.get("/test/api/transaction")
    data = get_response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1

