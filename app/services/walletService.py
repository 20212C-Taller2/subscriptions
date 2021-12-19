import json
from decimal import Decimal

from web3 import Web3

from ..constants import WEB3_INFURA_PROJECT_ID, CONTRACT_DIR, EthTxProcessResult


class WalletService:

    @staticmethod
    def _get_infura_w3():
        url = f'https://kovan.infura.io/v3/{WEB3_INFURA_PROJECT_ID}'
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

    def get_balance(self, addr: str):
        return Web3.fromWei(self._w3.eth.get_balance(addr), 'ether')

    def deposit(self, addr: str, priv_key: str, amount: Decimal):
        tx = self._co.functions.deposit().buildTransaction({
            "value": self._w3.toWei(str(amount), 'ether'),
            "nonce": self._w3.eth.get_transaction_count(addr),
            "from": addr})

        signed_tx = self._w3.eth.account.sign_transaction(tx, priv_key)
        tx_hash = self._w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        if tx_hash is not None:
            tx_rcpt = self._w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            res = self._co.events.DepositMade().processReceipt(tx_rcpt)
            if len(res) > 0 and res[0].event == "DepositMade":
                return EthTxProcessResult.OK
            else:
                return EthTxProcessResult.ERROR
        else:
            raise ValueError("tx_hash not returned by eth api call")
