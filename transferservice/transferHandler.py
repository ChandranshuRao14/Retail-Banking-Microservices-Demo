import json, traceback
import connexion
from transfer import Transfer
from datastore import datastoreHelper


def postTransfer(userId):
    """add a new transfer to db

    Returns:
        [Response] -- [id of the newly inserted datastore entity,status code]
    """
    try:
        if validateTransferBody(connexion.request.json) is True:
            transferId = datastoreHelper().putEntity(
                Transfer(userId=userId, **connexion.request.json)
            )
            return {"transferId": transferId}, 201
        else:
            return validateTransferBody(connexion.request.json), 400
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400


def getAllTransfers(userId):
    """get all transfers in db

    Returns:
        [Response] -- [array transfers in db,response code]
    """
    try:
        transfers = datastoreHelper().getEntityByFilter(
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


def getTransfer(transferId, userId):
    """get transfer in db by Entity id

    Returns:
        [Response] -- [transfer with id,response code]
    """
    try:
        transfer = datastoreHelper().getEntity(transferId)
        transfer.get_dict().pop("deleted", None)
        return transfer.get_dict(), 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400


def updateTransfer(transferId, userId):
    """update transfer in db with matching Entity id

    Returns:
        [Response] -- [updated transfer,response code]
    """
    try:
        if validateTransferBody(connexion.request.json) is True:
            transfer = datastoreHelper().updateEntity(
                transferId, Transfer(userId=userId, **connexion.request.json)
            )
            transfer.get_dict().pop("deleted", None)
            return transfer.get_dict(), 200
        else:
            return validateTransferBody(connexion.request.json), 400
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def deleteTransfer(transferId, userId):
    try:
        transfer = datastoreHelper().getEntity(transferId)
        transfer.deleted = True
        datastoreHelper().updateEntity(transferId, transfer)
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

