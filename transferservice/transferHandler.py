import traceback, json, os
import connexion
from transfer import Transfer
from datastore import datastoreHelper
from requestsUtil import make_request_session
from decorator import decorator
from cachetools import cached, TTLCache

dsHelper = datastoreHelper()
cache = TTLCache(maxsize=100, ttl=60)

@decorator
def checkUser(
    func,
    profileServiceURL=os.getenv("PROFILE_SVC_URL", "http://localhost:8080"),
    *args,
    **kwargs
):
    session = session = make_request_session([200, 400])
    @cached(cache)
    def get_profile_wrapper(userID):
        return session.get(profileServiceURL + "/user/{}".format(userID))
    response=get_profile_wrapper(args[0])
    if response.status_code != 200:
        return {"error": "user not found"}, 400
    return func(*args, **kwargs)

@checkUser
def postTransfer(userId):
    """add a new transfer to db

    Returns:
        [Response] -- [id of the newly inserted datastore entity,status code]
    """
    try:
        if validateTransferBody(connexion.request.json) is True:
            if (transactionCheck:= makeTransaction(userId, connexion.request.json["amount"])) is not True:
                print(transactionCheck)
                return {"error": "error creating transaction: {}".format(transactionCheck["error"])}, 400
            transferId = dsHelper.putEntity(
                Transfer(userId=userId, **connexion.request.json)
            )
            return {"transferId": transferId}, 201
        return validateTransferBody(connexion.request.json), 400
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400

@checkUser
def getAllTransfers(userId):
    """get all transfers in db

    Returns:
        [Response] -- [array transfers in db,response code]
    """
    try:
        transfers = dsHelper.getEntityByFilter(
            [["deleted", "=", False], ["userId", "=", userId]]
        )
        for transfer in transfers:
            transfer.pop("deleted")
        return transfers, 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None

@checkUser
def getTransfer(userId, transferId):
    """get transfer in db by Entity id

    Returns:
        [Response] -- [transfer with id,response code]
    """
    try:
        transfer = dsHelper.getEntity(transferId)
        if transfer:
            transfer.get_dict().pop("deleted", None)
            return transfer.get_dict(), 200
        return {"error": "transfer {} not found".format(transferId)}, 400
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400

@checkUser
def updateTransfer(userId, transferId):
    """update transfer in db with matching Entity id

    Returns:
        [Response] -- [updated transfer,response code]
    """
    try:
        if validateTransferBody(connexion.request.json) is True:
            transfer = dsHelper.updateEntity(
                transferId, Transfer(userId=userId, **connexion.request.json)
            )
            transfer.get_dict().pop("deleted", None)
            return transfer.get_dict(), 200
        return validateTransferBody(connexion.request.json), 400
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None

@checkUser
def deleteTransfer(userId, transferId):
    try:
        transfer = dsHelper.getEntity(transferId)
        transfer.deleted = True
        dsHelper.updateEntity(transferId, transfer)
        return True, 204
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def validateTransferBody(data):
    """Validates incoming json body

    Arguments:
        data {[dict]} -- [json body]

    Returns:
        [bool] -- [if validation passes]
        [dict] -- [if validation fails]
    """
    keys = [*data]
    allowedKeys = ["routingNumber", "accountNumber", "amount"]
    if len(keys) != 3:
        return {"error": "three keys are required in transfer body"}
    for key in keys:
        if key not in allowedKeys:
            return {
                "error": "only the following keys are allowed in transfer body:"
                + ",".join(allowedKeys)
            }
    return True


def makeTransaction(
    userId,
    amount,
    transactionType="debit",
    transactionServiceURL=os.getenv(
        "TRANSACTION_SVC_URL", "http://localhost:5050"
    ),
):
    session = make_request_session([201, 400])
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    response = session.post(
        transactionServiceURL + "/api/transaction/{}".format(userId),
        data=json.dumps({"amount": amount, "transactionType": transactionType}),
        headers=headers,
    )
    if response.status_code != 201:
        return response.json()
    return True
