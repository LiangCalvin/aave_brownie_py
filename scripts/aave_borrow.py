from brownie import network, config, interface
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
    # ABI
    # Address
    lending_pool = get_lending_pool()
    print(lending_pool)
    
def get_lending_pool():
    # ABI
    # Address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
    
    # # Define the asset and amount to borrow
    # asset = "DAI"
    # amount = 1000  # Amount in DAI

    # # Execute the borrow operation
    # try:
    #     tx_hash = aave_contract.borrow(asset, amount)
    #     print(f"Borrow transaction successful with hash: {tx_hash}")
    # except Exception as e:
    #     print(f"An error occurred while borrowing: {e}")