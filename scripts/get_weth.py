from scripts.helpful_scripts import get_account
from brownie import network, config, Contract, interface
from web3 import Web3


def main():
    get_weth()


def get_weth():
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit(
        {"from": account, "value": 0.1 * 10**18}
    )  # Deposit 0.1 ETH to get WETH
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
