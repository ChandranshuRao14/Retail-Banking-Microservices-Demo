import os
import json
from transfer import Transfer
from google.cloud import datastore
from google.oauth2 import service_account


class datastoreHelper:
    def __init__(
        self,
        creds=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH"),
        creds_json=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"),
        project=os.getenv("PROJECT_ID"),
        kind="transfer",
    ):
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH"):
            self._creds = service_account.Credentials.from_service_account_file(
                creds
            )
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
        self._client = datastore.Client(
            project=project, credentials=self._creds
        )

    def putEntity(self, transfer):
        """put a new entity in datastore

        Arguments:
            transfer {[Transfer]} -- [transfer to be added to db]

        Returns:
            [string] -- [id of added entity]
        """
        transfer_entity = datastore.Entity(key=self._client.key(self._kind))
        transfer_entity.update(transfer.get_dict())
        self._client.put(transfer_entity)
        return transfer_entity.key.id

    def getEntity(self, id):
        """get an entity from db by id

        Arguments:
            id {[string]} -- [entity id]

        Returns:
            [Transfer] -- [Transfer with matching id]
        """
        transfer = Transfer(
            **self._client.get(self._client.key(self._kind, id))
        )
        transfer.transferId = id
        return transfer

    def getEntityByFilter(self, filters):
        """get all entities matching a filter

        Arguments:
            filter {[[array of filters]]} -- [filters for datastore
                                            of the form ["key","operator","val"]]

        Returns:
            [list] -- [list of matching entities]
        """
        query = self._client.query(kind=self._kind)
        for filter in filters:
            query.add_filter(*filter)
        transfers_list = []
        transfers = list(query.fetch())
        for entity in transfers:
            transfer = Transfer(**entity)
            transfer.transferId = entity.key.id
            transfers_list.append(transfer.get_dict())
        return transfers_list

    def updateEntity(self, id, updated_entity):
        """update existing entity by id

        Arguments:
            id {[string]} -- [entity id to update]
            updated_entity {[type]} -- [new transfer data]

        Returns:
            [Transfer] -- [updated Transfer]
        """
        transfer = self._client.get(self._client.key(self._kind, id))
        transfer.update(updated_entity.get_dict())
        self._client.put(transfer)
        updatedTransfer = Transfer(**transfer)
        updatedTransfer.transferId = id
        return updatedTransfer
