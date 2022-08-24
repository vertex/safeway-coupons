import configparser
import itertools
import os
from typing import List, Optional

from .account import Account


class Config:
    @classmethod
    def load_accounts(cls, config_file: Optional[str] = None) -> List[Account]:
        account = cls.load_account_from_env()
        if account:
            return [account]
        if config_file:
            accounts = cls.load_accounts_from_config(config_file)
            if accounts:
                return accounts
        return []

    @classmethod
    def load_account_from_env(cls) -> Optional[Account]:
        username = os.environ.get("SAFEWAY_COUPONS_USERNAME")
        password = os.environ.get("SAFEWAY_COUPONS_PASSWORD")
        mail_to = os.environ.get("SAFEWAY_COUPONS_MAIL_TO")
        if username and password:
            return Account(
                username=username, password=password, mail_to=mail_to
            )
        return None

    @classmethod
    def load_accounts_from_config(cls, config_file: str) -> List[Account]:
        config = configparser.ConfigParser()
        config.read_file(
            itertools.chain(["[_no_section]"], open(config_file, "r"))
        )
        accounts: List[Account] = []
        for section in config.sections():
            if section in ["_no_section", "_global"]:
                if config.has_option(section, "email_sender"):
                    email_sender = config.get(section, "email_sender")
                    print(f"EMAIL SENDER: {email_sender}")
            else:
                accounts.append(
                    Account(
                        username=str(section),
                        password=config.get(section, "password"),
                        mail_to=(
                            config.get(section, "notify")
                            if config.has_option(section, "notify")
                            else None
                        ),
                    )
                )
        return accounts
