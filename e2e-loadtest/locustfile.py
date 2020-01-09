from locust import HttpLocust, TaskSet, task, between
from locust.clients import HttpSession
from generator import UserGenerator
import json, os


class MicroServiceHosts(HttpLocust):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(MicroServiceHosts, self).__init__(*args, **kwargs)
        self.profile_service_client = HttpSession(
            base_url=os.getenv(
        "PROFILE_SVC_URL", "http://localhost:8080"
    )
        )
        self.transaction_service_client = HttpSession(
            base_url=os.getenv(
        "TRANSACTION_SVC_URL", "http://localhost:5050"
    )
        )
        self.transfer_service_client = HttpSession(
            base_url=os.getenv(
        "TRANSFER_SVC_URL", "http://localhost:5000"
    )
        )


class UserBehavior(TaskSet):
    def __init__(self, *args, **kwargs):
        super(UserBehavior, self).__init__(*args, **kwargs)
        self.user = UserGenerator()

    def on_start(self):
        with self.locust.profile_service_client.post(
            "/user",
            data=json.dumps(self.user.profile),
            name="post-user",
            headers={
                "Content-type": "application/json",
                "Accept": "text/plain",
            },
            catch_response=True,
        ) as response:
            self.user.user_id = response.json()["UserID"]
            print(response.json())

    @task
    def get_transaction(self):
        if (transaction := self.user.get_random_transaction()):
            with self.locust.transaction_service_client.get(
                "/api/transaction/{}/{}".format(self.user.user_id,transaction["transactionId"]),
                name="get-transaction",
                catch_response=True,
            ) as response:
                print(response.json())
                if response.status_code == 200 or (
                    response.status_code == 400
                    and "error" in response.json().keys()
                ):
                    response.success()

    @task
    def get_all_transaction(self):
        with self.locust.transaction_service_client.get(
            "/api/transaction/{}".format(self.user.user_id),
            name="get-all-transactions",
            catch_response=True,
        ) as response:
            print(response.json())
            if response.status_code == 200 or (
                response.status_code == 400
                and "error" in response.json().keys()
            ):
                response.success()

    @task
    def post_debit_transaction(self):
        with self.locust.transaction_service_client.post(
            "/api/transaction/{}".format(self.user.user_id),
            data=json.dumps(self.user.generate_transaction("debit")),
            name="post-debit-transaction",
            headers={
                "Content-type": "application/json",
                "Accept": "text/plain",
            },
            catch_response=True,
        ) as response:
            print(response.json())
            if response.status_code == 201 or (
                response.status_code == 400
                and "error" in response.json().keys()
            ):
                if "transactionId" in response.json().keys():
                    self.user.transactions_from_api.append(response.json())
                response.success()

    @task
    def post_credit_transaction(self):
        with self.locust.transaction_service_client.post(
            "/api/transaction/{}".format(self.user.user_id),
            data=json.dumps(self.user.generate_transaction("credit")),
            name="post-credit-transaction",
            headers={
                "Content-type": "application/json",
                "Accept": "text/plain",
            },
            catch_response=True,
        ) as response:
            print(response.json())
            if response.status_code == 201 or (
                response.status_code == 400
                and "error" in response.json().keys()
            ):
                if "transactionId" in response.json().keys():
                    self.user.transactions_from_api.append(response.json())
                response.success()

    @task(2)
    def post_transfer(self):
        with self.locust.transfer_service_client.post(
            "/api/transfer/{}".format(self.user.user_id),
            data=json.dumps(self.user.generate_transfer()),
            name="post-transfer",
            headers={
                "Content-type": "application/json",
                "Accept": "text/plain",
            },
            catch_response=True,
        ) as response:
            print(response.json())
            if response.status_code == 201 or (
                response.status_code == 400
                and "error" in response.json().keys()
            ):
                if "transferId" in response.json().keys():
                    self.user.transfers_from_api.append(response.json())
                response.success()

    @task
    def get_tansfer(self):
        if (transfer := self.user.get_random_transfer()):
            with self.locust.transfer_service_client.get(
                "/api/transfer/{}/{}".format(self.user.user_id,transfer["transferId"]),
                name="get-transfer",
                catch_response=True,
            ) as response:
                print(response.json())
                if response.status_code == 200 or (
                    response.status_code == 400
                    and "error" in response.json().keys()
                ):
                    response.success()

    @task
    def get_all_transfer(self):
        with self.locust.transfer_service_client.get(
            "/api/transfer/{}".format(self.user.user_id),
            name="get-all-transfers",
            catch_response=True,
        ) as response:
            print(response.json())
            if response.status_code == 200 or (
                response.status_code == 400
                and "error" in response.json().keys()
            ):
                response.success()


class WebsiteUser(MicroServiceHosts):
    host = "http://localhost:8080"
    wait_time = between(2, 5)
    task_set = UserBehavior
