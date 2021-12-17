# Blockchain
from enum import Enum

WEB3_INFURA_PROJECT_ID = "ce58a62a06224458ad8ba3f589387e4d"
CONTRACT_DIR = "./contracts/BasicPayments.json"


class EthTxProcessResult(Enum):
    ERROR = 0
    OK = 1
