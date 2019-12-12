import json, traceback
import connexion
from transaction import Transaction
from datastore import datastoreHelper


def postTransaction():
    """add a new transaction to db

    Returns:
        [Response] -- [id of the newly inserted datastore entity,status code]
    """
    try:
        if validateTransactionBody(connexion.request.json) is True:
            transactionId = datastoreHelper().putEntity(Transaction(**connexion.request.json))
            return {"transactionId": transactionId}, 201
        else:
            return validateTransactionBody(connexion.request.json), 400
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400


def getAllTransactions():
    """get all transactions in db

    Returns:
        [Response] -- [array transactions in db,response code]
    """
    try:
        transactions = datastoreHelper().getEntityByFilter(["deleted", "=", False])
        for transaction in transactions:
            transaction.pop("deleted")
        return transactions, 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def getTransaction(transactionId):
    """get transaction in db by Entity id

    Returns:
        [Response] -- [transaction with id,response code]
    """
    try:
        transaction = datastoreHelper().getEntity(transactionId)
        transaction.get_dict().pop("deleted", None)
        return transaction.get_dict(), 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400


def updateTransaction(transactionId):
    """update transaction in db with matching Entity id

    Returns:
        [Response] -- [updated transaction,response code]
    """
    try:
        if validateTransactionBody(connexion.request.json) is True:
            transaction = datastoreHelper().updateEntity(
                transactionId, Transaction(**connexion.request.json)
            )
            transaction.get_dict().pop("deleted", None)
            return transaction.get_dict(), 200
        else:
            return validateTransactionBody(connexion.request.json), 400
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def deleteTransaction(transactionId):
    try:
        transaction = datastoreHelper().getEntity(transactionId)
        transaction.deleted = True
        datastoreHelper().updateEntity(transactionId, transaction)
        return True, 204
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def validateTransactionBody(data):
    """Validates incoming json body

    Arguments:
        data {[dict]} -- [json body]

    Returns:
        [bool] -- [if validation passes]
        [dict] -- [if validation fails]
    """
    keys = [*data]
    allowedKeys = ["amount", "transactionType"]
    if len(keys) != 2:
        return {"error": "two keys are required in transaction body"}
    for key in keys:
        if key not in allowedKeys:
            return {
                "error": "only the following keys are allowed in transaction body:"
                + ",".join(allowedKeys)
            }

    return True

