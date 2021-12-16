import json
import random
import string

from web3 import Web3

from ..constants import WEB3_INFURA_PROJECT_ID, CONTRACT_DIR


class WalletService:

    @staticmethod
    def _get_infura_w3():
        url = f'https://mainnet.infura.io/v3/{WEB3_INFURA_PROJECT_ID}'
        w3 = Web3(Web3.HTTPProvider(url))
        return w3

    @staticmethod
    def _get_contract_instance(w3: Web3):
        with open(CONTRACT_DIR, 'r') as read_file:
            vars = json.load(read_file)
            contract_instance = w3.eth.contract(address=vars['address'],
                                                abi=vars['abi'])
            return contract_instance

    def __init__(self):
        self._w3 = self._get_infura_w3()
        self._co = self._get_contract_instance(self._w3)

    def create_wallet(self):
        wallet = self._w3.eth.account.create()
        return {
            "private_key": wallet.privateKey.hex(),
            "address": wallet.address
        }


def create_wallet():
    # TODO Integrate with wallet
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
