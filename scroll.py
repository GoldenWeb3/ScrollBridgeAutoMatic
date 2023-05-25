from os import path
from eth_utils import address
from web3 import Account, Web3
import re
import time
from eth_account.signers.local import LocalAccount

scroll_w3 = Web3(Web3.HTTPProvider(
    'https://alpha-rpc.scroll.io/l2'))
goerli_w3 = Web3(Web3.HTTPProvider(
    'https://goerli.infura.io/v3/237aa45f96ab4554ab826a0fb375a497'))

one_eth = 1000000000000000000
one_eth_gas = 1000000000

def getBalance(w3, address):
    balance = w3.eth.getBalance(address)
    return balance


#Orb池最多支持0.01
def orbiterScrolToGoerli(w3,privateKey,bridge_eth):
    account: LocalAccount = Account.from_key(privateKey)
    _address = account.address
    eth = getBalance(w3,_address)
    eth = eth/one_eth
    print(f"wallet[{_address}] eth:{eth}")
    if eth > bridge_eth:
        # gasPrice = w3.toWei(0.001, 'gwei')
        gasPrice = w3.eth.gasPrice
        value = w3.toWei(bridge_eth, 'ether')
        nonce = w3.eth.getTransactionCount(
                account.address)

        txData = {
                    "chainId": 534353,
                    "nonce": nonce,
                    "gas": 21000,
                    "gasPrice":  gasPrice,
                    "from": account.address,
                    "to": w3.toChecksumAddress("0x0043d60e87c5dd08C86C3123340705a1556C4719"),
                    "value": value
                }

        signed_txn = w3.eth.account.sign_transaction(dict(
                txData),
                account.key
            )
        result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        w3.eth.wait_for_transaction_receipt(result.hex())
        return result.hex()

def ScrolBridgeScrolToGoerli(w3,privateKey,bridge_eth):
    w3.eth.account.enable_unaudited_hdwallet_features()
    account: LocalAccount = Account.from_key(privateKey)
    _address = account.address
    eth = getBalance(w3,_address)
    eth = eth/one_eth
    print(f"wallet[{_address}] eth:{eth}")
    if eth > bridge_eth:
        # gasPrice = w3.toWei(0.001, 'gwei')
        gasPrice = w3.eth.gasPrice
        value = w3.toWei(bridge_eth, 'ether')
        nonce = w3.eth.getTransactionCount(
                account.address)
        data = "0xc7cdea37" + w3.toHex(value)[2:].zfill(64) + w3.toHex(160000)[2:].zfill(64)
        value = value + int(0.00000081885184 * one_eth)
        txData = {
                    "chainId": 534353,
                    "nonce": nonce,
                    "gas": 320304,
                    "gasPrice":  gasPrice,
                    "from": account.address,
                    "to": w3.toChecksumAddress("0x6d79Aa2e4Fbf80CF8543Ad97e294861853fb0649"),
                    "value": value,
                    "data":data
                }

        signed_txn = w3.eth.account.sign_transaction(dict(
                txData),
                account.key
            )
        result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        w3.eth.wait_for_transaction_receipt(result.hex())
        eth  = getBalance(w3,_address)
        print(f"Send transaction success,account balance:{eth/one_eth}")
        return result.hex()


#ScrolBirdge goerli 测试网转scrol测试网
def ScrolBirdgeGoerliToScrol(w3,privateKey,bridge_eth):
    w3.eth.account.enable_unaudited_hdwallet_features()
    account: LocalAccount = Account.from_key(privateKey)
    _address = account.address
    eth = getBalance(w3,_address)
    eth = eth/one_eth
    print(f"wallet[{_address}] eth:{eth} bridge_eth:{bridge_eth}" )
    if eth > bridge_eth:
        # gasPrice = w3.toWei(0.001, 'gwei')
        gasPrice = w3.eth.gasPrice
        value = w3.toWei(bridge_eth, 'ether')
        nonce = w3.eth.getTransactionCount(
                account.address)
        #data： 转账数值+gasLimit固定40000(跨链后的转账gaslimit)？
        data = "0x9f8420b3"+w3.toHex(value)[2:].zfill(64)+w3.toHex(40000)[2:].zfill(64)

        #40000:跨链后的转账gaslimit
        value = value + 40000 * one_eth_gas
        txData = {
                    "chainId": 5,
                    "nonce": nonce,
                    "gas": 303146 ,#tx gaslimit
                    "maxFeePerGas":  gasPrice, 
                    "maxPriorityFeePerGas": w3.toWei(0.00000002, 'gwei'),
                    "from": account.address,
                    "to": w3.toChecksumAddress("0xe5e30e7c24e4dfcb281a682562e53154c15d3332"),
                    "value": value,
                    "data":data,
                    "type":2
                }

        signed_txn = w3.eth.account.sign_transaction(dict(
                txData),
                account.key
            )
        result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        #不等transation状态
        # w3.eth.wait_for_transaction_receipt(result.hex())
        # eth  = getBalance(w3,_address)
        # print(f"Send transaction success,account balance:{eth/one_eth}")
        return result.hex()



#钱包私钥
privateKey = ""
#跨链金额
bridge_eth = 0.005
hash = ScrolBirdgeGoerliToScrol(goerli_w3,privateKey,bridge_eth)
print(f"跨链成功 hash:{hash}")
