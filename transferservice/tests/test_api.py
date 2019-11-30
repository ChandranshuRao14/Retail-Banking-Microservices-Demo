from openapi_spec_validator import validate_spec
import json, requests


VALID_TRANSFER = dict()
VALID_TRANSFER["accountNumber"] = "100"
VALID_TRANSFER["amount"] = "100"
VALID_TRANSFER["routingNumber"] = "200"

INVALID_TRANSFER_LESS_KEYS = dict()
INVALID_TRANSFER_LESS_KEYS["accountNumber"] = "100"
INVALID_TRANSFER_LESS_KEYS["amount"] = "100"

INVALID_TRANSFER_WRONG_KEYS = dict()
INVALID_TRANSFER_WRONG_KEYS["accountNumber"] = "100"
INVALID_TRANSFER_WRONG_KEYS["amount"] = "100"
INVALID_TRANSFER_WRONG_KEYS["loremipsom"] = "200"
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


def test_post_transfer(client):

    headers = {"content-type": "application/json"}
    testAPIBasePath = "/test/api"
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(VALID_TRANSFER), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transferId" in [*data]


def test_post_transfer_fail_required_keys(client):
    headers = {"content-type": "application/json"}
    testAPIBasePath = "/test/api"
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(INVALID_TRANSFER_LESS_KEYS), headers=headers
    )
    assert post_response.status_code == 400
    data = post_response.get_json()
    assert "error" in [*data]


def test_post_transfer_fail_extra_keys(client):
    headers = {"content-type": "application/json"}
    testAPIBasePath = "/test/api"
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(INVALID_TRANSFER_WRONG_KEYS), headers=headers
    )
    assert post_response.status_code == 400
    data = post_response.get_json()
    assert "error" in [*data]


"""
**************************************
Validate GET Transfer
**************************************
"""


def test_get_transfer(client):
    headers = {"content-type": "application/json"}
    testAPIBasePath = "/test/api"
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(VALID_TRANSFER), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transferId" in [*data]
    transferId = data["transferId"]
    get_response = client.get(testAPIBasePath + "/transfer/{}".format(transferId))
    data = get_response.get_json()
    assert "accountNumber" in [*data]
    assert "amount" in [*data]
    assert "routingNumber" in [*data]
    assert "transferId" in [*data]


def test_get_transfer_fail(client):
    testAPIBasePath = "/test/api"
    get_response = client.get(testAPIBasePath + "/transfer/1")
    assert get_response.status_code == 400


"""
**************************************
Validate Update Transfer
**************************************
"""


def test_update_transfer(client):
    headers = {"content-type": "application/json"}
    testAPIBasePath = "/test/api"
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(VALID_TRANSFER), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transferId" in [*data]
    transferId = data["transferId"]
    transfer = dict()
    transfer["accountNumber"] = "500"
    transfer["amount"] = "400"
    transfer["routingNumber"] = "300"
    put_response = client.put(
        testAPIBasePath + "/transfer/{}".format(transferId),
        data=json.dumps(transfer),
        headers=headers,
    )
    assert put_response.status_code == 200
    data = put_response.get_json()
    assert data["accountNumber"] == transfer["accountNumber"]
    assert data["amount"] == transfer["amount"]
    assert data["routingNumber"] == transfer["routingNumber"]
    assert data["transferId"] == transferId


def test_update_transfer_fail(client):
    headers = {"content-type": "application/json"}
    testAPIBasePath = "/test/api"
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(VALID_TRANSFER), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transferId" in [*data]
    transferId = data["transferId"]
    put_response = client.put(
        testAPIBasePath + "/transfer/{}".format(transferId),
        data=json.dumps(INVALID_TRANSFER_WRONG_KEYS),
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


def test_delete_transfer(client):
    headers = {"content-type": "application/json"}
    testAPIBasePath = "/test/api"
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(VALID_TRANSFER), headers=headers
    )
    assert post_response.status_code == 201
    data = post_response.get_json()
    assert "transferId" in [*data]
    transferId = data["transferId"]
    delete_response = client.delete(testAPIBasePath + "/transfer/{}".format(transferId))
    assert delete_response.status_code == 204


def test_delete_transfer_fail(client):
    testAPIBasePath = "/test/api"
    delete_response = client.delete(testAPIBasePath + "/transfer/1")
    assert delete_response.status_code == 400


"""
**************************************
Validate All Transfers
**************************************
"""


def test_all_transfer(client):
    testAPIBasePath = "/test/api"
    get_response = client.get(testAPIBasePath + "/transfer")
    data = get_response.get_json()
    for transfer in data:
        delete_response = client.delete(
            testAPIBasePath + "/transfer/{}".format(transfer["transferId"])
        )
        assert delete_response.status_code == 204
    headers = {"content-type": "application/json"}
    post_response = client.post(
        testAPIBasePath + "/transfer", data=json.dumps(VALID_TRANSFER), headers=headers
    )
    assert post_response.status_code == 201
    get_response = client.get(testAPIBasePath + "/transfer")
    data = get_response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1

