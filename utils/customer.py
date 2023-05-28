import re
from dataclasses import dataclass, field
import logging

EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

logger = logging.getLogger(__name__)


@dataclass
class Customer:
    name: str
    email: str
    address: str
    items: list = field(default_factory=list)

    def __post_init__(self):
        _is_valid = {}
        _is_valid["name"] = self.validate_name(self.name)
        _is_valid["email"] = self.validate_customer_email(self.email)
        _is_valid["address"] = self.validate_address(self.address)

        _not_valid = dict(filter(lambda kv_pair: not kv_pair[1], _is_valid.items()))
        if _not_valid:
            message = f"{31*'='} Validation failed for the following args {31*'='} \n"
            for k in _not_valid.keys():
                message += f"{k} \n"

            raise ValueError(message)

    @staticmethod
    def validate_name(name: str):
        if not isinstance(name, str):
            logger.info("name provided is invalid")
            return False
        return True

    @staticmethod
    def validate_customer_email(email: str):
        if not EMAIL_REGEX.match(email):
            logger.info("email provided is invalid")
            return False
        return True

    @staticmethod
    def validate_address(address: str):
        if not isinstance(address, str):
            logger.info("address provided is invalid")
            return False
        return True
