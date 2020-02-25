import namegenerator
from random import randint, choice


class UserGenerator:
    def __init__(self):
        self.profile = {
            "Username": namegenerator.gen(),
            "Address": "",
            "Email": "",
            "Password": "",
            "PhoneNumber": 0,
            "AccountBalance": randint(100, 99999),
        }
        self.user_id = None
        self.transactions_from_api = []
        self.transactions_to_api = []
        self.transfers_from_api = []
        self.transfers_to_api = []

    def generate_transaction(self, transactionType):
        transaction = {
            "amount": str(randint(100, 9999)),
            "transactionType": transactionType,
        }
        self.transactions_to_api.append(transaction)
        return transaction

    def generate_transfer(self):
        transfer = {
            "amount": str(randint(100, 9999)),
            "routingNumber": "1",
            "accountNumber": "1",
        }
        self.transfers_to_api.append(transfer)
        return transfer

    def get_random_transaction(self):
        if len(self.transactions_from_api) > 0:
            return choice(self.transactions_from_api)
        return False

    def get_random_transfer(self):
        if len(self.transfers_from_api) > 0:
            return choice(self.transfers_from_api)
        return False
