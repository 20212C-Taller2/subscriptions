from enum import Enum

# Blockchain constants
WEB3_INFURA_PROJECT_ID = "ce58a62a06224458ad8ba3f589387e4d"
CONTRACT_DIR = "./contracts/BasicPayments.json"
CONTRACT_OWNER_ADDR = "0x5244dF2C4dF771F98C11E3c5A9813f566E9b20d9"
CONTRACT_OWNER_PK = "0x929fd836be241e4a2f4092ba525c07081f5fc50324bbdb1ca9154b4837eca74f"


class EthTxProcessResult(Enum):
    ERROR = 0
    OK = 1


# Payments constants
class PaymentStatus(str, Enum):
    PAYMENT_PENDING = "PENDING"
    PAYMENT_ACCEPTED = "ACCEPTED"


DAYS_TO_REMORSE = 1
