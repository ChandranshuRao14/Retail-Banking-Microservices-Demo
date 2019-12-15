import json
from enum import Enum


class Transaction(object):
    def __init__(
        self, amount, transactionType, userId, transactionId=None, deleted=False,
    ):
        self.transactionId = transactionId
        self.userId = userId
        self.amount = amount
        self.transactionType = transactionType
        self.deleted = deleted

    def get_dict(self):
        return self.__dict__

