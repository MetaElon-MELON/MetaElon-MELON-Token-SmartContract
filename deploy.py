from brownie import MetaElon, network, config
from scripts.helpful_scripts import getAccount


def deploy_ME():
    account = getAccount()
    Meta_Elon = MetaElon.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )


def main():
    deploy_ME()
