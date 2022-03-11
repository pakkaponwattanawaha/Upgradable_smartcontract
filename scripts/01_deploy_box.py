from brownie import network, Box
from scripts.utils import get_account


def deploy_box():
    account = get_account()
    print(f"Deploying on {network.show_active()}")
    box = Box.deploy({"from": account})
    print(f"box value: {box.retrieve()}")


def main():
    deploy_box()
