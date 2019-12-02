import json


class Transfer(object):
    def __init__(
        self, amount, routingNumber, accountNumber, transferId=None, deleted=False,
    ):
        self.transferId = transferId
        self.amount = amount
        self.routingNumber = routingNumber
        self.accountNumber = accountNumber
        self.deleted = deleted

    def get_dict(self):
        return self.__dict__
