import json, traceback
import connexion
from transfer import Transfer
from datastore import datastoreHelper


def postTransfer():
    """add a new transfer to db

    Returns:
        [Response] -- [id of the newly inserted datastore entity,status code]
    """
    try:
        transferId = datastoreHelper().putEntity(Transfer(**connexion.request.json))
        return {"transferId": transferId}, 201
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400


def getAllTransfers():
    """get all transfers in db

    Returns:
        [Response] -- [array transfers in db,response code]
    """
    try:
        transfers = datastoreHelper().getEntityByFilter(["deleted", "=", False])
        for transfer in transfers:
            transfer.pop("deleted")
        return transfers, 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def getTransfer(transferId):
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


def updateTransfer(transferId):
    """update transfer in db with matching Entity id

    Returns:
        [Response] -- [updated transfer,response code]
    """
    try:
        transfer = datastoreHelper().updateEntity(transferId, Transfer(**connexion.request.json))
        transfer.get_dict().pop("deleted", None)
        return transfer.get_dict(), 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def deleteTransfer(transferId):
    return None
