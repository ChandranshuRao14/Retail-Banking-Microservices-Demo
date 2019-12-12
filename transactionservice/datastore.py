import os, json
from transaction import Transaction
from google.cloud import datastore
from google.oauth2 import service_account


class datastoreHelper:
    def __init__(
        self,
        creds=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH"),
        creds_json=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"),
        project=os.getenv("PROJECT_ID"),
        kind="transaction",
    ):
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH"):
            self._creds = service_account.Credentials.from_service_account_file(creds)
        elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"):
            self._creds = service_account.Credentials.from_service_account_info(
                json.loads(creds_json)
            )
        else:
            raise Exception("No Credentials set")
        if os.getenv("PROJECT_ID") is None:
            raise Exception("No Project ID set")
        self._project = project
        self._kind = kind
        self._client = datastore.Client(project=project, credentials=self._creds)

    def putEntity(self, transaction):
        """put a new entity in datastore

        Arguments:
            transaction {[Transaction]} -- [transaction to be added to db]

        Returns:
            [string] -- [id of added entity]
        """
        transaction_entity = datastore.Entity(key=self._client.key(self._kind))
        transaction_entity.update(transaction.get_dict())
        self._client.put(transaction_entity)
        return transaction_entity.key.id

    def getEntity(self, id):
        """get an entity from db by id

        Arguments:
            id {[string]} -- [entity id]

        Returns:
            [Transaction] -- [Transaction with matching id]
        """
        transaction = Transaction(**self._client.get(self._client.key(self._kind, id)))
        transaction.transactionId = id
        return transaction

    def getEntityByFilter(self, filter):
        """get all entities matching a filter

        Arguments:
            filter {[array]} -- [filter for datastore of the form ["key","operator","val"]]

        Returns:
            [list] -- [list of matching entities]
        """
        query = self._client.query(kind=self._kind)
        query.add_filter(*filter)
        transactions_list = []
        transactions = list(query.fetch())
        for entity in transactions:
            transaction = Transaction(**entity)
            transaction.transactionId = entity.key.id
            transactions_list.append(transaction.get_dict())
        return transactions_list

    def updateEntity(self, id, updated_entity):
        """update existing entity by id

        Arguments:
            id {[string]} -- [entity id to update]
            updated_entity {[type]} -- [new transaction data]

        Returns:
            [Transaction] -- [updated Transaction]
        """
        transaction = self._client.get(self._client.key(self._kind, id))
        transaction.update(updated_entity.get_dict())
        self._client.put(transaction)
        updatedTransaction = Transaction(**transaction)
        updatedTransaction.transactionId = id
        return updatedTransaction
