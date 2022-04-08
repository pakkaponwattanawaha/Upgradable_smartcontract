from brownie import (
    Contract,
    network,
    config,
    Box,
    Box2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
)
from scripts.utils import get_account, encode_function_data, upgrade


def deploy_box():
    account = get_account()
    print(f"Deploying on {network.show_active()}")
    box = Box.deploy({"from": account})
    print(f"box value: {box.retrieve()}")

    proxy_admin = ProxyAdmin.deploy({"from": account})

    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,  # deploy with box as a implementation contract
        proxy_admin.address,  # defined proxy admin
        box_encoded_initializer_function,  # add initializer if any
        {"from": account, "gas_limit": 1000000},
    )

    print(f"Proxy deployed to {proxy}, you can now upgrade to version2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # -> proxy is already delegate to Box so using proxy address will not violate from_abi convention
    # we then give it Box.abi because we want to delegate function in box(defined by abi) but in a proxy delegate call manner
    proxy_box.store(10, {"from": account})
    print(proxy_box.retrieve())
    # we are using proxy_box address but can delegate the retrieve() call to "Box"
    try:
        # try calling increment that only exist in box2
        proxy_box.increment({"from": account})
    except Exception as e:
        print(f"Exception{e}")

    # UPGRADE!!!
    box_2 = Box2.deploy({"from": account})
    # upgrade from proxy(which is box) to => box2 with proxy_admin_contract
    upgrade_tx = upgrade(
        account,
        proxy,
        box_2.address,
        proxy_admin_contract=proxy_admin,
    )
    upgrade_tx.wait(1)
    print("Proxy has been upgraded")
    proxy_box = Contract.from_abi("Box2", proxy.address, Box2.abi)
    # we now can call increment with proxy bc it is now delegate to box2!!!!!!!!!
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())


def main():
    deploy_box()
