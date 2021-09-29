import csv
import os

from email_validator import validate_email, caching_resolver, EmailSyntaxError
from requests import request


class InvalidAmountException(Exception):
    """Negative amount or can't convert to float"""
    pass

class CheckSender:
    """Capable of sending checks to physical addresses or email addresses"""

    # Authentication keys for sending messages
    api_key_env_name = "CHECKBOOK_API_KEY"
    api_secret_env_name = "CHECKBOOK_API_SECRET"

    # URLs for check sending endpoints
    digital_check_api_url = "https://demo.checkbook.io/v3/check/digital"
    physical_check_api_url = "https://demo.checkbook.io/v3/check/physical"

    def __init__(self):
        """Stores API Key"""

        for env_name, attr in [(self.api_key_env_name, "api_key"),
                               (self.api_secret_env_name, "api_secret")]:

            setattr(self, attr, os.environ.get(env_name))
            if getattr(self, attr) is None:
                raise Exception(f"Environment missing {env_name}")

        # DNS resolver to validate many email addresses
        self.dns_resolver = caching_resolver(timeout=10)

    def send_checks(self, csv_path: str, err_csv_path: str):

        err_str = "Error"

        rows_w_errs = []

        with open(csv_path, mode="r") as f:
            # CSV is fastest for plain CSV iteration
            for row in csv.DictReader(f):
                try:
                    # Email validation and normalization
                    email_addr = self._get_email(row["Address"])
                    self._send_check_to_email(row, email_addr)
                except (EmailSyntaxError, InvalidAmountException) as e:
                    row[err_str] = str(e)
                    rows_w_errs.append(row)
                # On a separate line since this should not happen
                except Exception as e:
                    # In a real application use logging
                    print(e)
                    row[err_str] = str(e)
                    rows_w_errs.append(row)

        if rows_w_errs:
            # In a full application change this to logging
            print("These are the rows that did not send and contained errors")
            print(f"This is being saved to {err_csv_path}")
            with open(err_csv_path, mode="w") as f:
                writer = csv.DictWriter(f, fieldnames=row.keys())
                writer.writeheader()
                for row in rows_w_errs:
                    writer.writerow(row)
        else:
            print("Success!")

    def _get_email(self, email: str):
        """Does email validation and normalization"""

        return validate_email(email, dns_resolver=self.dns_resolver).email

    def _send_check_to_email(self, row: dict, email: str):
        """Sends check to email"""

        self._send_check(row, self.digital_check_api_url, email)

    def _send_check(self, row, url, recipient):
        """Function that sends checks"""

        amount = self._get_amount(row)

        payload = {"recipient": recipient,
                   "amount": amount,
                   "name": row["Name"],
                   "description": row["Description"]}
        response = request("POST", url, json=payload, headers=self.headers)
        response.raise_for_status()
        assert response.status_code == 201

    def _get_amount(self, row):
        """Gets amount and validates"""

        try:
            amount = float(row["Amount"])
            assert amount > 0, "Can't send or recieve negative amounts"
        except TypeError:
            raise InvalidAmountException(f"Not a number: {amount}")
        except AssertionError:
            raise InvalidAmountException("Amount sent must be greater than 0")
        return amount

    @property
    def headers(self):
        """Gets headers for API requests"""

        return {"Accept": "application/json",
                "Content-Type": "application/json",
                # It keeps saying that I am unauthorized.
                # Maybe sandbox mode doesn't want me sending checks to random people
                # I tried sending it to myself though, and it still failed
                "Authorization": f"{self.api_key}:{self.api_secret}"}
