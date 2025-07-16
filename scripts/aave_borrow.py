from brownie import network, config
from web3 import Web3
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account

def main():
    """
    Main function to execute the Aave borrowing script.
    """
    # Initialize the Aave contract
    contract = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # # Define the asset and amount to borrow
    # asset = "DAI"
    # amount = 1000  # Amount in DAI

    # # Execute the borrow operation
    # try:
    #     tx_hash = aave_contract.borrow(asset, amount)
    #     print(f"Borrow transaction successful with hash: {tx_hash}")
    # except Exception as e:
    #     print(f"An error occurred while borrowing: {e}")