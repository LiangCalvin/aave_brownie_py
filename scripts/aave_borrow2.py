from brownie import network, config, interface
from web3 import Web3
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account
import traceback

amount = Web3.to_wei(0.1, "ether")


def main():
    """
    Main function to execute the Aave borrowing script.
    """
    # Initialize the Aave contract
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # ABI
    # Address
    lending_pool = get_lending_pool()
    print(lending_pool)
    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    lending_pool.setUserUseReserveAsCollateral(erc20_address, True, {"from": account})
    print("Deposited!")
    # how much
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # borrowable_eth -> borrowable_dai * 95%
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    # amount_dai_to_borrow = 1
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    # print(f"Borrowing {Web3.to_wei(amount_dai_to_borrow, 'ether')} DAI in wei")
    # Now we will borrow
    dai_address = config["networks"][network.show_active()]["dai_token"]

    # Check available liquidity of DAI in lending pool
    dai_token = interface.IERC20(dai_address)
    available_liquidity_wei = dai_token.balanceOf(lending_pool.address)
    available_liquidity = Web3.from_wei(available_liquidity_wei, "ether")
    print(f"Available DAI liquidity in pool: {available_liquidity:.6f}")

    small_borrow_amount = Web3.to_wei(0.0001, "ether")
    if available_liquidity < 1:
        print("Not enough DAI liquidity in pool to borrow 1 DAI.")
        return

    try:
        borrow_tx = lending_pool.borrow(
            dai_address, small_borrow_amount, 1, 0, account.address, {"from": account}
        )
        borrow_tx.wait(1)
        print("Successfully borrowed 1 DAI!")
    except Exception as e:
        print(f"Borrow failed: {str(e)}")

        traceback.print_exc()
        return

    # print("We borrowed some DAI!")
    # borrow_tx = lending_pool.borrow(
    #     dai_address,
    #     Web3.to_wei(amount_dai_to_borrow, "ether"),
    #     1,
    #     0,
    #     account.address,
    #     {"from": account},
    # )
    # borrow_tx.wait(1)
    # print("We borrowed some DAI!")


def get_asset_price(price_feed_address):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.from_wei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    # 0.000279254836104738
    return float(converted_latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.from_wei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.from_wei(total_collateral_eth, "ether")
    total_debt_eth = Web3.from_wei(total_debt_eth, "ether")
    print(f"You have total collateral {total_collateral_eth} worth of ETH deposited.")
    print(f"You have total debt {total_debt_eth} worth of ETH borrowed.")
    print(f"You have available borrow {available_borrow_eth} worth of ETH.")
    print(f"Liquidity Threshold: {current_liquidation_threshold}")
    print(f"LTV: {ltv / 100}%")
    print(f"Health Factor: {health_factor / 1e18}")

    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    # ABI
    # Address
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    # ABI
    # Address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
