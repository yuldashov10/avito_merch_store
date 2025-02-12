import logging
import random
from typing import Optional

from locust import HttpUser, between, task

logging.basicConfig(level=logging.INFO)


class AvitoShopUser(HttpUser):
    wait_time = between(1, 5)
    token: Optional[str] = None
    username: Optional[str] = None

    def on_start(self):
        self.username = f"user{random.randint(1, 100000)}"
        self.authenticate_user()

    def authenticate_user(self):
        response = self.client.post(
            "/api/auth",
            json={"username": self.username, "password": "testpass"},
        )
        if response.status_code == 200:
            self.token = response.json().get("token")

    @task
    def send_coin(self):
        if not self.token:
            self.authenticate_user()
        if self.token:
            to_user = f"user{random.randint(1, 100000)}"
            self.client.post(
                "/api/auth", json={"username": to_user, "password": "testpass"}
            )

            response = self.client.post(
                "/api/sendCoin",
                json={"toUser": to_user, "amount": 100},
                headers={"Authorization": f"Bearer {self.token}"},
            )

            if response.status_code == 400:
                error_message = response.json().get("detail", "")
                if "Not enough coins" in error_message:
                    logging.warning(
                        f"User {self.username} "
                        "has not enough coins. Resetting balance."
                    )
                    self.client.post(
                        "/api/reset_coins",
                        headers={"Authorization": f"Bearer {self.token}"},
                    )
                else:
                    logging.error(
                        f"Unexpected error: {error_message}",
                    )
            elif response.status_code != 200:
                logging.error("Failed to send coins.")

    @task
    def buy_item(self):
        if not self.token:
            self.authenticate_user()
        if self.token:
            item = random.choice(
                [
                    "t-shirt",
                    "cup",
                    "book",
                    "pen",
                    "powerbank",
                    "hoody",
                    "umbrella",
                    "socks",
                    "wallet",
                    "pink-hoody",
                ]
            )
            response = self.client.get(
                f"/api/buy/{item}",
                headers={"Authorization": f"Bearer {self.token}"},
            )

            if response.status_code == 400:
                error_message = response.json().get("detail", "")
                if "Not enough coins" in error_message:
                    logging.warning(
                        f"User {self.username} "
                        "has not enough coins. Resetting balance."
                    )
                    self.client.post(
                        "/api/reset_coins",
                        headers={"Authorization": f"Bearer {self.token}"},
                    )
                else:
                    logging.error(f"Unexpected error: {error_message}")
            elif response.status_code != 200:
                logging.error("Failed to buy item.")
