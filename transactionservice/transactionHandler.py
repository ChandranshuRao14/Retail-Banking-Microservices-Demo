import json, traceback, os
import connexion
from transaction import Transaction
from datastore import datastoreHelper
from requestsUtil import make_request_session

dsHelper = datastoreHelper()


def postTransaction(userId):
    """add a new transaction to db

    Returns:
        [Response] -- [id of the newly inserted datastore entity,status code]
    """
    try:
        if validateTransactionBody(connexion.request.json) is not True:
            return validateTransactionBody(connexion.request.json), 400
        userData = getUserData(userId)
        if not userData:
            return {"error": "user not found"}, 400
        if connexion.request.json["transactionType"] == "credit":
            userData["AccountBalance"] += int(connexion.request.json["amount"])
        elif connexion.request.json["transactionType"] == "debit" and (
            int(userData["AccountBalance"])
            - int(connexion.request.json["amount"])
            < 0
        ):
            return (
                {
                    "error": "user does not have enough account balance for this transaction"
                },
                400,
            )
        userData["AccountBalance"] -= int(connexion.request.json["amount"])
        updateUserData(userData)
        transactionId = dsHelper.putEntity(
            Transaction(userId=userId, **connexion.request.json)
        )
        return {"transactionId": transactionId}, 201
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400


def getAllTransactions(userId):
    """get all transactions in db

    Returns:
        [Response] -- [array transactions in db,response code]
    """
    try:
        userData = getUserData(userId)
        if not userData:
            return {"error": "user not found"}, 400
        transactions = dsHelper.getEntityByFilter(
            [["deleted", "=", False], ["userId", "=", userId]]
        )
        for transaction in transactions:
            transaction.pop("deleted")
        return transactions, 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400
    return None


def getTransaction(transactionId, userId):
    """get transaction in db by Entity id

    Returns:
        [Response] -- [transaction with id,response code]
    """
    try:
        userData = getUserData(userId)
        if not userData:
            return {"error": "user not found"}, 400
        transaction = dsHelper.getEntity(transactionId)
        transaction.get_dict().pop("deleted", None)
        return transaction.get_dict(), 200
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return False, 400


def updateTransaction(transactionId, userId):
    """update transaction in db with matching Entity id

    Returns:
        [Response] -- [updated transaction,response code]
    """
    try:
        if validateTransactionBody(connexion.request.json) is True:
            userData = getUserData(userId)
            if not userData:
                return {"error": "user not found"}, 400
            transaction = dsHelper.updateEntity(
                transactionId,
                Transaction(userId=userId, **connexion.request.json),
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


def deleteTransaction(transactionId, userId):
    try:
        userData = getUserData(userId)
        if not userData:
            return {"error": "user not found"}, 400
        transaction = dsHelper.getEntity(transactionId)
        transaction.deleted = True
        dsHelper.updateEntity(transactionId, transaction)
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


def getUserData(
    userId,
    profileServiceURL=os.getenv("PROFILE_SVC_URL", "http://localhost:8080"),
):
    try:
        session = make_request_session([200, 400])
        response = session.get(profileServiceURL + "/user/{}".format(userId))
        if response.status_code != 200:
            return False
        return response.json()
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return {"error": "unable to retrieve user"}, 400


def updateUserData(
    userData,
    profileServiceURL=os.getenv("PROFILE_SVC_URL", "http://localhost:8080"),
):
    try:
        session = make_request_session([200, 400])
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        response = session.put(
            profileServiceURL + "/user/{}".format(userData["UserID"]),
            data=json.dumps(userData),
            headers=headers,
        )
        if response.status_code != 200:
            return False
        return True
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
        return {"error": "unable to update user data"}, 400
